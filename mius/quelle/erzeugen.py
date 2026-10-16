#!/usr/bin/env python3
"""
Erzeugt das Logo-Paket von MIUS aus einer einzigen Quelle.

  python mius/quelle/erzeugen.py

Schreibt nach mius/01_Logo, 02_Schriften, 03_Vorlagen, 04_Farben und
05_Druckdaten. Der Aufruf ist wiederholbar; alle Ausgaben werden
ueberschrieben. Quelle sind dieses Skript, die Schriften unter
02_Schriften/quelle/ und die Farbwerte in 04_Farben/tokens.css.
Websites holen sich die fertigen Dateien von hier.

Braucht: fonttools, uharfbuzz, shapely, Pillow, python-pptx,
python-docx und playwright mit Chromium.
"""
import io
import json
import math
import shutil
import struct
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HIER = Path(__file__).resolve().parent
MARKE = HIER.parent
LOGO = MARKE / '01_Logo'
WEB = LOGO / 'web'
SCHRIFT = MARKE / '02_Schriften'
QUELLE = SCHRIFT / 'quelle'
VORLAGE = MARKE / '03_Vorlagen'
FARBE = MARKE / '04_Farben'
DRUCK = MARKE / '05_Druckdaten'
TUNNEL_PNG = LOGO / 'png' / 'mius_tunnel-rahmen_300px.png'

# --------------------------------------------------------------------------
# Das Signet. Nachgezeichnet aus dem freigestellten Original: elf Flaechen,
# ausschliesslich gerade Kanten. Koordinaten im Raster 1060 x 912.
# Der dunkle Rahmen ist der Tunnel ("Rahmen und Fokus"), kein Buchstabe.
# --------------------------------------------------------------------------
B, H = 1060, 912
TUNNEL = [(0, 112), (286, 1), (286, 75), (69, 159), (69, 753), (286, 837), (286, 911), (0, 799)]
VERBINDER_GRUEN = [[(354, 65), (403, 46), (403, 121), (354, 140)],
                   [(472, 112), (520, 93), (520, 167), (472, 186)]]
VERBINDER_TEAL = [[(589, 158), (637, 140), (637, 213), (589, 231)],
                  [(706, 203), (755, 184), (755, 259), (706, 277)],
                  [(824, 248), (871, 229), (871, 303), (824, 321)]]
M_BALKEN = [[(286, 1), (354, 27), (354, 885), (286, 911)],
            [(403, 46), (472, 73), (472, 838), (403, 865)]]
I_BALKEN = [(520, 93), (589, 119), (589, 792), (520, 819)]
U = [(637, 140), (706, 166), (706, 678), (755, 659), (755, 184), (824, 211), (824, 702), (637, 773)]
S = [(871, 229), (1059, 301), (1059, 371), (941, 326), (941, 411), (1059, 411), (1059, 609),
     (871, 681), (871, 609), (990, 564), (990, 479), (871, 479)]

POSITIV = dict(tunnel='#141E00', v_teal='#001313', m='#117011', i='#2B8F2B', us='#003D3D')
NEGATIV = dict(tunnel='#3F5F00', v_teal='#206B6B', m='#2B8F2B', i='#36B436', us='#298888')
TEXT_HELL, TEXT_DUNKEL = '#141A15', '#E3EBE6'
TIEFTON = '#001313'

CLAIM = 'Medien | Informatik | Unterricht | Schule'
NEIGUNG = 20.9          # Grad, abgelesen an den Balkenunterkanten
CLAIM_START = (312, 952)
CLAIM_LAENGE = 800
CLAIM_GROESSE = 46

# QR-Code fuer https://mius.ch (Version 2, Fehlerkorrektur M), Zeile fuer Zeile.
QR = ['1111111011011010001111111', '1000001011101100001000001', '1011101011111001001011101',
      '1011101010111100001011101', '1011101011000100101011101', '1000001000111011001000001',
      '1111111010101010101111111', '0000000011100001000000000', '0110101101000000101011111',
      '1101000000100101011000001', '0110011110110010100110111', '0111000010010111000010010',
      '1010111011100011111001011', '0010100111110110101001001', '1000001011011110011100111',
      '0100010010010000000010010', '1010101001101010111111000', '0000000010100011100011011',
      '1111111010101001101011011', '1000001001101110100011001', '1011101011111000111111010',
      '1011101000100111100111110', '1011101011111111010010001', '1000001010011001110011010',
      '1111111000101010110100011']


def d(*polygone):
    return ' '.join('M' + ' '.join('%g %g' % p for p in poly) + 'Z' for poly in polygone)


def signet_pfade(f):
    return (f'<path fill="{f["tunnel"]}" d="{d(TUNNEL, *VERBINDER_GRUEN)}"/>'
            f'<path fill="{f["v_teal"]}" d="{d(*VERBINDER_TEAL)}"/>'
            f'<path fill="{f["m"]}" d="{d(*M_BALKEN)}"/>'
            f'<path fill="{f["i"]}" d="{d(I_BALKEN)}"/>'
            f'<path fill="{f["us"]}" d="{d(U, S)}"/>')


def signet_mono_pfad():
    """Einfarbig: Ohne Farbstufen verschmelzen Balken und Verbinder. Eine
    Fuge von 8 Einheiten trennt sie, als echte Aussparung (kein Maskentrick),
    damit Stempel- und Gravurbetriebe die Datei direkt verwenden koennen."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    vorn = unary_union([Polygon(p) for p in M_BALKEN + [I_BALKEN, U, S]])
    hinten = unary_union([Polygon(p) for p in [TUNNEL] + VERBINDER_GRUEN + VERBINDER_TEAL])
    hinten = hinten.difference(vorn.buffer(8, join_style='mitre', mitre_limit=4))
    teile = []
    for geo in (hinten, vorn):
        for poly in getattr(geo, 'geoms', [geo]):
            if poly.area < 40:
                continue
            for ring in [poly.exterior, *poly.interiors]:
                pts = list(ring.coords)[:-1]
                teile.append('M' + ' '.join('%.1f %.1f' % p for p in pts) + 'Z')
    return ' '.join(teile)


# --------------------------------------------------------------------------
# Schrift als Kontur. Claim und Domain stehen in Josefin Sans; in den
# Logodateien werden sie in Pfade umgewandelt, damit niemand die Schrift
# installiert haben muss.
# --------------------------------------------------------------------------
STATISCH = [
    # Datei, Quelle, Achsen, Familie, Schnitt
    ('JosefinSans-ExtraLight.ttf', 'JosefinSans-variabel.ttf', {'wght': 200}),
    ('JosefinSans-Light.ttf', 'JosefinSans-variabel.ttf', {'wght': 300}),
    ('JosefinSans-Regular.ttf', 'JosefinSans-variabel.ttf', {'wght': 400}),
    ('Archivo-SemiBold.ttf', 'Archivo-variabel.ttf', {'wdth': 100, 'wght': 600}),
    ('Archivo-Bold.ttf', 'Archivo-variabel.ttf', {'wdth': 100, 'wght': 700}),
    ('Archivo-ExtraBold.ttf', 'Archivo-variabel.ttf', {'wdth': 100, 'wght': 800}),
    ('InstrumentSans-Regular.ttf', 'InstrumentSans-variabel.ttf', {'wdth': 100, 'wght': 400}),
    ('InstrumentSans-Medium.ttf', 'InstrumentSans-variabel.ttf', {'wdth': 100, 'wght': 500}),
    ('InstrumentSans-SemiBold.ttf', 'InstrumentSans-variabel.ttf', {'wdth': 100, 'wght': 600}),
    ('JetBrainsMono-Regular.ttf', 'JetBrainsMono-variabel.ttf', {'wght': 400}),
]


def schriften():
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    for datei, quelle, achsen in STATISCH:
        # Ohne neuen Zeitstempel, damit ein erneuter Lauf dieselben Bytes schreibt
        f = TTFont(QUELLE / quelle, recalcTimestamp=False)
        inst = instancer.instantiateVariableFont(f, achsen, updateFontNames=True)
        inst.save(SCHRIFT / datei)
    for lizenz in QUELLE.glob('OFL-*.txt'):
        shutil.copy(lizenz, SCHRIFT / lizenz.name)
    print('Schriften:', len(STATISCH), 'statische Schnitte')


def kontur(text, datei, groesse, sperrung=0.0):
    """Liefert (Pfaddaten, Breite, (ymin, ymax)) fuer eine Zeile Text.
    y nach unten, Grundlinie bei 0."""
    import uharfbuzz as hb
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.ttLib import TTFont
    pfad = str(SCHRIFT / datei)
    tt = TTFont(pfad)
    upm = tt['head'].unitsPerEm
    glyphen = tt.getGlyphSet()
    ordnung = tt.getGlyphOrder()
    font = hb.Font(hb.Face(hb.Blob.from_file_path(pfad)))
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': False})
    k = groesse / upm
    x = 0.0
    teile, ymin, ymax = [], 0.0, 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = ordnung[info.codepoint]
        stift = SVGPathPen(glyphen)
        glyphen[name].draw(TransformPen(stift, (k, 0, 0, -k, x + pos.x_offset * k, -pos.y_offset * k)))
        teile.append(stift.getCommands())
        bp = BoundsPen(glyphen)
        glyphen[name].draw(bp)
        if bp.bounds:
            ymin = min(ymin, -bp.bounds[3] * k)
            ymax = max(ymax, -bp.bounds[1] * k)
        x += pos.x_advance * k + sperrung
    return ' '.join(t for t in teile if t), x - sperrung, (ymin, ymax)


def claim_gruppe(farbe, schnitt):
    datei = 'JosefinSans-ExtraLight.ttf' if schnitt == 200 else 'JosefinSans-Light.ttf'
    _, breite, _ = kontur(CLAIM, datei, CLAIM_GROESSE)
    sperrung = (CLAIM_LAENGE - breite) / (len(CLAIM) - 1)
    pfad, _, _ = kontur(CLAIM, datei, CLAIM_GROESSE, sperrung)
    x, y = CLAIM_START
    return (f'<g transform="translate({x} {y}) rotate(-{NEIGUNG})">'
            f'<path fill="{farbe}" d="{pfad}"/></g>')


def svg(viewbox, inhalt, titel):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" '
            f'aria-label="{titel}">{inhalt}</svg>\n')


def logos():
    """Alle Logofassungen als SVG. Gibt ein Verzeichnis Name -> (SVG, Breite, Hoehe) zurueck."""
    titel = 'MIUS – Medien, Informatik, Unterricht, Schule'
    aus = {}
    hb_w, hb_h = 1080, 980
    aus['mius_hauptlogo_positiv'] = svg(f'0 0 {hb_w} {hb_h}', signet_pfade(POSITIV) + claim_gruppe(TEXT_HELL, 200), titel)
    aus['mius_hauptlogo_negativ'] = svg(f'0 0 {hb_w} {hb_h}', signet_pfade(NEGATIV) + claim_gruppe('#D9E3DD', 300), titel)
    aus['mius_signet_positiv'] = svg(f'0 0 {B} {H}', signet_pfade(POSITIV), titel)
    aus['mius_signet_negativ'] = svg(f'0 0 {B} {H}', signet_pfade(NEGATIV), titel)
    mono = signet_mono_pfad()
    aus['mius_signet_mono_schwarz'] = svg(f'0 0 {B} {H}', f'<path fill="#000000" fill-rule="evenodd" d="{mono}"/>', titel)
    aus['mius_signet_mono_weiss'] = svg(f'0 0 {B} {H}', f'<path fill="#FFFFFF" fill-rule="evenodd" d="{mono}"/>', titel)

    # Absenderzeile: Signet anderthalbmal so hoch wie die Schriftgroesse,
    # Abstand 0,55 em, Schrift optisch auf die Mitte des Signets gesetzt.
    groesse = H / 1.5
    luecke = 0.55 * groesse
    pfad, breite, (ymin, ymax) = kontur('mius.ch', 'JosefinSans-Light.ttf', groesse, 0.02 * groesse)
    grund = H / 2 - (ymin + ymax) / 2
    a_w = math.ceil(B + luecke + breite + 8)
    for name, farben, tf in (('positiv', POSITIV, TEXT_HELL), ('negativ', NEGATIV, TEXT_DUNKEL)):
        aus[f'mius_absender_{name}'] = svg(
            f'0 0 {a_w} {H}',
            signet_pfade(farben) + f'<path fill="{tf}" transform="translate({B + luecke:.1f} {grund:.1f})" d="{pfad}"/>',
            'mius.ch')
    for name, inhalt in aus.items():
        (LOGO / 'svg' / f'{name}.svg').write_text(inhalt, encoding='utf-8')
    print('Logos:', len(aus), 'SVG')
    return aus


def masse(svgtext):
    vb = svgtext.split('viewBox="')[1].split('"')[0].split()
    return float(vb[2]), float(vb[3])


# --------------------------------------------------------------------------
# Rendern ueber Chromium: PNG mit Transparenz, PDF als Vektor.
# --------------------------------------------------------------------------
class Werkstatt:
    def __init__(self):
        from playwright.sync_api import sync_playwright
        import os
        self._pw = sync_playwright().start()
        # MIUS_CHROMIUM zeigt auf ein vorhandenes Chromium, falls Playwright
        # keinen passenden Browser heruntergeladen hat.
        pfad = os.environ.get('MIUS_CHROMIUM')
        self.browser = self._pw.chromium.launch(executable_path=pfad) if pfad else self._pw.chromium.launch()
        self.tmp = Path(tempfile.mkdtemp(prefix='mius-'))

    def schliessen(self):
        self.browser.close()
        self._pw.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _seite(self, html, w, h, dpr=1):
        p = self.browser.new_page(viewport={'width': int(w), 'height': int(h)}, device_scale_factor=dpr)
        datei = self.tmp / 'seite.html'
        datei.write_text(html, encoding='utf-8')
        p.goto(datei.as_uri())
        p.wait_for_load_state('networkidle')
        p.evaluate('document.fonts.ready')
        return p

    def png(self, html, ziel, w, h, transparent=True):
        p = self._seite(html, w, h)
        p.screenshot(path=str(ziel), omit_background=transparent)
        p.close()

    def pdf(self, html, ziel, w_mm, h_mm):
        p = self._seite(html, w_mm * 3.78, h_mm * 3.78)
        p.pdf(path=str(ziel), width=f'{w_mm}mm', height=f'{h_mm}mm', print_background=True,
              margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}, prefer_css_page_size=True)
        p.close()


def schriftschnitte_css():
    regeln = []
    for datei, familie, gewicht in [
        ('JosefinSans-ExtraLight.ttf', 'Josefin Sans', 200), ('JosefinSans-Light.ttf', 'Josefin Sans', 300),
        ('Archivo-SemiBold.ttf', 'Archivo', 600), ('Archivo-Bold.ttf', 'Archivo', 700),
        ('Archivo-ExtraBold.ttf', 'Archivo', 800), ('InstrumentSans-Regular.ttf', 'Instrument Sans', 400),
        ('InstrumentSans-Medium.ttf', 'Instrument Sans', 500), ('InstrumentSans-SemiBold.ttf', 'Instrument Sans', 600),
        ('JetBrainsMono-Regular.ttf', 'JetBrains Mono', 400)]:
        regeln.append(f"@font-face{{font-family:'{familie}';font-weight:{gewicht};"
                      f"src:url('{(SCHRIFT / datei).as_uri()}') format('truetype')}}")
    return '\n'.join(regeln)


def html_rahmen(inhalt, extra_css='', hintergrund='transparent'):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{schriftschnitte_css()}'
            f'html,body{{margin:0;padding:0;background:{hintergrund}}} svg{{display:block}}{extra_css}</style>'
            f'</head><body>{inhalt}</body></html>')


def svg_in_groesse(svgtext, w, h):
    return svgtext.replace('<svg ', f'<svg width="{w}" height="{h}" ', 1)


def rastern(ws, logos_svg):
    breiten = {'mius_hauptlogo': 2000, 'mius_signet': 1000, 'mius_absender': 1200}
    for name, inhalt in logos_svg.items():
        vb_w, vb_h = masse(inhalt)
        basis = next(v for k, v in breiten.items() if name.startswith(k))
        w = basis
        h = round(basis * vb_h / vb_w)
        ws.png(html_rahmen(svg_in_groesse(inhalt, w, h)), LOGO / 'png' / f'{name}_{w}px.png', w, h)
        # Vektor-PDF, 100 mm breit (Absender 80 mm), fuer Druckereien und Office
        mm_w = 80 if name.startswith('mius_absender') else 100
        mm_h = round(mm_w * vb_h / vb_w, 2)
        seite = html_rahmen(svg_in_groesse(inhalt, f'{mm_w}mm', f'{mm_h}mm'),
                            f'@page{{size:{mm_w}mm {mm_h}mm;margin:0}}')
        ws.pdf(seite, LOGO / 'pdf' / f'{name}.pdf', mm_w, mm_h)
    print('Logos: PNG und PDF')


# --------------------------------------------------------------------------
# Web: Favicon, App-Symbol, Link-Vorschau, Signaturbild. Websites
# kopieren diese Dateien beim Bauen aus 01_Logo/web und 01_Logo/svg.
# --------------------------------------------------------------------------
def web(ws, logos_svg):
    from PIL import Image

    rand = 0.11
    innen = B * (1 + 2 * rand)
    oy = (innen - H) / 2
    icon = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {innen:.0f} {innen:.0f}">'
            f'<rect width="{innen:.0f}" height="{innen:.0f}" fill="{TIEFTON}"/>'
            f'<g transform="translate({B * rand:.0f} {oy:.0f})">{signet_pfade(NEGATIV)}</g></svg>\n')
    (WEB / 'favicon.svg').write_text(icon, encoding='utf-8')
    for groesse, datei in ((32, 'icon-32.png'), (180, 'apple-touch-icon.png'), (512, 'icon-512.png')):
        ws.png(html_rahmen(svg_in_groesse(icon, groesse, groesse)), WEB / datei, groesse, groesse, False)
    gross = Image.open(WEB / 'icon-512.png').convert('RGBA')
    gross.save(WEB / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])

    # Signaturbild: Signet 88 px breit, Anzeige mit 44 px
    sig = logos_svg['mius_signet_positiv']
    ws.png(html_rahmen(svg_in_groesse(sig, 88, 76)), WEB / 'mius-signatur.png', 88, 76)
    shutil.copy(WEB / 'mius-signatur.png', VORLAGE / 'mius_signatur.png')

    # Link-Vorschau fuer alle Seiten
    absender = svg_in_groesse(logos_svg['mius_absender_negativ'], 'auto', 64)
    og = html_rahmen(f'''<div class="og">{absender}
      <h1>Material, das den Schulalltag übersteht.</h1>
      <p>Weiterbildung, Beratung und Unterrichtsmaterial für Medien und Informatik</p>
      <span class="claim">Medien | Informatik | Unterricht | Schule</span></div>''', f'''
      .og{{width:1200px;height:630px;box-sizing:border-box;background:{TIEFTON};padding:84px 96px;
           display:flex;flex-direction:column;justify-content:space-between;color:{TEXT_DUNKEL};position:relative}}
      .og svg{{height:64px;width:auto}}
      h1{{font-family:'Archivo';font-weight:800;font-size:76px;letter-spacing:-2.4px;line-height:1.02;margin:0;max-width:860px}}
      p{{font-family:'Instrument Sans';font-size:28px;margin:-40px 0 0;color:#C9D3CC;max-width:820px}}
      .claim{{font-family:'Josefin Sans';font-weight:300;font-size:24px;letter-spacing:1px;color:#93A9A0}}''')
    ws.png(og, WEB / 'og-image.png', 1200, 630, False)
    print('Web: Favicon, App-Symbol, Link-Vorschau, Signaturbild')


# --------------------------------------------------------------------------
# Druckdaten (RGB, Endformat plus Beschnitt). CMYK erst nach dem Andruck.
# --------------------------------------------------------------------------
def qr_svg():
    teile = []
    for y, zeile in enumerate(QR):
        x = 0
        while x < len(zeile):
            if zeile[x] == '1':
                s = x
                while x < len(zeile) and zeile[x] == '1':
                    x += 1
                teile.append(f'M{s} {y}h{x - s}v1h-{x - s}z')
            else:
                x += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 29 29" shape-rendering="crispEdges">'
            f'<rect x="-2" y="-2" width="29" height="29" fill="#fff"/><path fill="#0B0F0B" d="{"".join(teile)}"/></svg>')


def druck(ws, logos_svg):
    sig = logos_svg['mius_signet_positiv']
    hl_neg = logos_svg['mius_hauptlogo_negativ']
    hl_pos = logos_svg['mius_hauptlogo_positiv']
    abs_neg = logos_svg['mius_absender_negativ']
    basis = "*{box-sizing:border-box} body{font-family:'Instrument Sans';color:#141A15}"

    # Visitenkarte 85 x 55 mm, 3 mm Beschnitt
    vorn = html_rahmen(f'''<div class="k">{svg_in_groesse(sig, '14mm', 'auto')}
      <div><div class="n">Samuel Müller</div><div class="r">Medien und Informatik für die Volksschule</div>
      <div class="c">Hauptstrasse 14, 8272 Ermatingen<br>info@mius.ch · mius.ch</div></div></div>''',
        basis + '''@page{size:91mm 61mm;margin:0}
        .k{width:91mm;height:61mm;padding:9mm 9mm 8mm;background:#FCFDFC;display:flex;flex-direction:column;justify-content:space-between}
        .n{font-family:'Archivo';font-weight:700;font-size:12pt;letter-spacing:-.2pt}
        .r{font-size:7.5pt;color:#526053;margin-top:1mm}
        .c{font-family:'JetBrains Mono';font-size:6.2pt;line-height:1.6;color:#3A453B;margin-top:3mm}''')
    ws.pdf(vorn, DRUCK / 'visitenkarte_vorderseite_91x61mm.pdf', 91, 61)
    hinten = html_rahmen(f'<div class="k">{svg_in_groesse(hl_neg, "54mm", "auto")}</div>',
                         basis + f'@page{{size:91mm 61mm;margin:0}} .k{{width:91mm;height:61mm;background:{TIEFTON};display:grid;place-items:center}}')
    ws.pdf(hinten, DRUCK / 'visitenkarte_rueckseite_91x61mm.pdf', 91, 61)

    # Sticker rund, 50 mm, 2 mm Beschnitt
    rund = html_rahmen(f'<div class="s"><div class="kreis">{svg_in_groesse(hl_pos, "36mm", "auto")}</div></div>',
                       basis + '@page{size:54mm 54mm;margin:0} .s{width:54mm;height:54mm;background:#fff;display:grid;place-items:center}'
                       '.kreis{width:50mm;height:50mm;border-radius:50%;display:grid;place-items:center}'
                       '.kreis svg{margin-left:1mm}')
    ws.pdf(rund, DRUCK / 'sticker_rund_50mm.pdf', 54, 54)
    qrs = html_rahmen(f'''<div class="s"><div class="kreis">{svg_in_groesse(sig, '10mm', 'auto')}
        {svg_in_groesse(qr_svg(), '21mm', '21mm')}<span>mius.ch</span></div></div>''',
                      basis + '@page{size:54mm 54mm;margin:0} .s{width:54mm;height:54mm;background:#fff;display:grid;place-items:center}'
                      '.kreis{width:50mm;height:50mm;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.8mm}'
                      "span{font-family:'Josefin Sans';font-weight:300;font-size:10pt;line-height:1;letter-spacing:.2pt}")
    ws.pdf(qrs, DRUCK / 'sticker_qr_50mm.pdf', 54, 54)

    # Namensschilder: zehn Stueck 86 x 54 mm auf A4, mit Schnittlinien
    schild = f'''<div class="b"><div class="band">{svg_in_groesse(abs_neg, 'auto', '5mm')}</div>
      <div class="h">Hallo, ich bin</div><div class="l"></div></div>'''
    bogen = html_rahmen(f'<div class="a4">{schild * 10}</div>', basis + f'''@page{{size:210mm 297mm;margin:0}}
      .a4{{width:210mm;height:297mm;padding:13.5mm 19mm;display:grid;grid-template-columns:86mm 86mm;grid-auto-rows:54mm;gap:0}}
      .b{{position:relative;background:#fff;outline:.15mm dashed #BBC3BC}}
      .band{{height:12mm;background:{TIEFTON};display:flex;align-items:center;padding-left:6mm}}
      .h{{font-family:'Josefin Sans';font-weight:300;font-size:13pt;margin:5mm 6mm 0}}
      .l{{position:absolute;left:6mm;right:6mm;bottom:9mm;height:.3mm;background:#BBC3BC}}''')
    ws.pdf(bogen, DRUCK / 'namensschilder_10x_86x54mm_A4.pdf', 210, 297)
    print('Druckdaten: Visitenkarte, Sticker, Namensschilder')


def social(ws, logos_svg):
    """Fertige Bilder fuer LinkedIn und leere Vorlagen fuer Beitraege und Stories."""
    abs_neg = logos_svg['mius_absender_negativ']
    stil = f"*{{box-sizing:border-box}} .f{{background:{TIEFTON};color:{TEXT_DUNKEL};position:relative;overflow:hidden}}"
    banner = html_rahmen(f'''<div class="f" style="width:1584px;height:396px">
      <div style="position:absolute;left:640px;top:50%;transform:translateY(-50%);width:820px">
        <div style="font-family:'Josefin Sans';font-weight:300;font-size:26px;letter-spacing:1px;color:#93A9A0">Medien | Informatik | Unterricht | Schule</div>
        <div style="font-family:'Archivo';font-weight:800;font-size:52px;letter-spacing:-1.4px;line-height:1.08;margin-top:18px">Weiterbildung, Beratung und Projekte für die Volksschule</div>
      </div></div>''', stil)
    ws.png(banner, VORLAGE / 'social' / 'linkedin_banner_1584x396.png', 1584, 396, False)
    for w, h, name in ((1080, 1080, 'beitrag_1080x1080'), (1080, 1350, 'beitrag_1080x1350'), (1080, 1920, 'story_1080x1920')):
        unten = 340 + 60 if h == 1920 else 76
        leer = html_rahmen(f'''<div class="f" style="width:{w}px;height:{h}px">
          <div style="position:absolute;left:76px;bottom:{unten}px">{svg_in_groesse(abs_neg, 'auto', 46)}</div></div>''', stil)
        ws.png(leer, VORLAGE / 'social' / f'{name}_leer.png', w, h, False)
    print('Social Media: Banner und Vorlagen')


# --------------------------------------------------------------------------
# Office-Vorlagen
# --------------------------------------------------------------------------
def folienmaster():
    from pptx import Presentation
    from pptx.util import Emu, Mm, Pt
    from pptx.dml.color import RGBColor
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.oxml.ns import qn
    from lxml import etree

    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    master = prs.slide_master

    # Theme: Farben und Schriften, damit neue Folien die Marke erben
    teil = master.part.part_related_by(RT.THEME)
    baum = etree.fromstring(teil.blob)
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    schema = {'dk1': '141A15', 'lt1': 'FFFFFF', 'dk2': '001313', 'lt2': 'ECEEEC', 'accent1': '117011',
              'accent2': '206B6B', 'accent3': '2B8F2B', 'accent4': '003D3D', 'accent5': '80A732',
              'accent6': '526053', 'hlink': '117011', 'folHlink': '206B6B'}
    cs = baum.find('.//a:clrScheme', ns)
    cs.set('name', 'MIUS')
    for k, v in schema.items():
        el = cs.find(f'a:{k}', ns)
        for c in list(el):
            el.remove(c)
        etree.SubElement(el, qn('a:srgbClr')).set('val', v)
    fs = baum.find('.//a:fontScheme', ns)
    fs.set('name', 'MIUS')
    fs.find('a:majorFont/a:latin', ns).set('typeface', 'Archivo')
    fs.find('a:minorFont/a:latin', ns).set('typeface', 'Instrument Sans')
    teil._blob = etree.tostring(baum, xml_declaration=True, encoding='UTF-8', standalone=True)

    titelstil = master._element.find(qn('p:txStyles')).find(qn('p:titleStyle'))
    titelstil.find(qn('a:lvl1pPr')).find(qn('a:defRPr')).set('b', '1')

    # Absenderzeile im Master, unten links; Seitenzahl bleibt Platzhalter
    # python-pptx kann Bilder nur auf Folien setzen: auf einer Hilfsfolie
    # einfuegen, ins Master-Gerüst verschieben, Bildbezug neu verknuepfen.
    bildpfad = str(LOGO / 'png' / 'mius_absender_positiv_1200px.png')
    hilfe = prs.slides.add_slide(prs.slide_layouts[6])
    pic = hilfe.shapes.add_picture(bildpfad, Mm(32), Mm(176), height=Mm(7))._element
    _, rid = master.part.get_or_add_image_part(bildpfad)
    pic.find('.//' + qn('a:blip')).set(qn('r:embed'), rid)
    master.shapes._spTree.append(pic)
    folien = prs.slides._sldIdLst
    prs.part.drop_rel(folien[-1].rId)
    folien.remove(folien[-1])

    # Layout "Titelfolie": Tiefton, ohne Master-Elemente, heller Text
    titel_layout = prs.slide_layouts[0]
    titel_layout._element.set('showMasterSp', '0')
    titel_layout.background.fill.solid()
    titel_layout.background.fill.fore_color.rgb = RGBColor(0x00, 0x13, 0x13)
    for ph in titel_layout.placeholders:
        tx = ph._element.find(qn('p:txBody'))
        lst = tx.find(qn('a:lstStyle'))
        for c in list(lst):
            lst.remove(c)
        lvl = etree.SubElement(lst, qn('a:lvl1pPr'))
        rpr = etree.SubElement(lvl, qn('a:defRPr'))
        fill = etree.SubElement(rpr, qn('a:solidFill'))
        etree.SubElement(fill, qn('a:srgbClr')).set('val', 'E3EBE6')

    rand = Mm(32)

    def text(folie, x, y, w, h, inhalt, groesse, farbe='141A15', schrift='Instrument Sans', fett=False, sperr=0):
        box = folie.shapes.add_textbox(x, y, w, h)
        tf = box.text_frame
        tf.word_wrap = True
        for i, zeile in enumerate(inhalt.split('\n')):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = zeile
            r.font.size = Pt(groesse)
            r.font.name = schrift
            r.font.bold = fett
            r.font.color.rgb = RGBColor.from_string(farbe)
            if sperr:
                r.font._element.set('spc', str(sperr))
        return box

    leer = prs.slide_layouts[6]

    # 1 Titelfolie
    f = prs.slides.add_slide(titel_layout)
    for ph in list(f.placeholders):
        ph._element.getparent().remove(ph._element)
    f.background.fill.solid()
    f.background.fill.fore_color.rgb = RGBColor(0x00, 0x13, 0x13)
    text(f, rand, Mm(34), Mm(170), Mm(10), 'WEITERBILDUNG', 12, '93A9A0', 'JetBrains Mono', sperr=300)
    text(f, rand, Mm(46), Mm(190), Mm(50), 'Titel der Veranstaltung', 54, 'E3EBE6', 'Archivo', True)
    text(f, rand, Mm(98), Mm(170), Mm(20), 'Untertitel, Zielgruppe und Datum', 18, 'C9D3CC')
    f.shapes.add_picture(str(LOGO / 'png' / 'mius_absender_negativ_1200px.png'), rand, Mm(176), height=Mm(7))

    # 2 Kapiteltrenner
    f = prs.slides.add_slide(leer)
    f.background.fill.solid()
    f.background.fill.fore_color.rgb = RGBColor(0xEC, 0xEE, 0xEC)
    text(f, rand, Mm(60), Mm(60), Mm(14), 'TEIL 2', 12, '117011', 'JetBrains Mono', sperr=300)
    text(f, rand, Mm(72), Mm(250), Mm(40), 'Kapiteltitel', 48, '141A15', 'Archivo', True)

    # 3 Inhaltsfolie
    f = prs.slides.add_slide(leer)
    text(f, rand, Mm(24), Mm(200), Mm(8), 'TEIL 2 · EINSTIEG', 12, '526053', 'JetBrains Mono', sperr=300)
    text(f, rand, Mm(33), Mm(270), Mm(20), 'Eine Aussage pro Folie', 36, '141A15', 'Archivo', True)
    text(f, rand, Mm(62), Mm(200), Mm(80),
         'Erster Punkt in einem kurzen Satz\nZweiter Punkt in einem kurzen Satz\nDritter Punkt in einem kurzen Satz',
         22, '141A15')

    # 4 Zitat mit Rahmen und Fokus
    f = prs.slides.add_slide(leer)
    f.shapes.add_picture(str(TUNNEL_PNG), rand, Mm(48), height=Mm(80))
    text(f, Mm(62), Mm(62), Mm(240), Mm(50), '«Ein Zitat oder eine Kernaussage, höchstens zwei Zeilen.»', 36, '141A15', 'Archivo', True)
    text(f, Mm(62), Mm(112), Mm(200), Mm(10), 'Name, Funktion', 16, '526053')

    # 5 Schlussfolie, ohne die helle Absenderzeile aus dem Master
    f = prs.slides.add_slide(leer)
    f._element.set('showMasterSp', '0')
    f.background.fill.solid()
    f.background.fill.fore_color.rgb = RGBColor(0x00, 0x13, 0x13)
    f.shapes.add_picture(str(LOGO / 'png' / 'mius_hauptlogo_negativ_2000px.png'), rand, Mm(40), height=Mm(80))
    text(f, Mm(190), Mm(70), Mm(120), Mm(40), 'Samuel Müller\ninfo@mius.ch\nmius.ch', 22, 'E3EBE6')

    prs.save(VORLAGE / 'mius_folienmaster.pptx')
    print('Vorlage: Folienmaster')


def word_vorlagen():
    from docx import Document
    from docx.enum.section import WD_SECTION
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_TAB_ALIGNMENT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Mm, Pt, RGBColor

    absender = str(LOGO / 'png' / 'mius_absender_positiv_1200px.png')

    def schrift(stil, name, groesse, fett=False, farbe='141A15'):
        stil.font.name = name
        stil.font.size = Pt(groesse)
        stil.font.bold = fett
        stil.font.color.rgb = RGBColor.from_string(farbe)
        rpr = stil.element.get_or_add_rPr()
        rf = rpr.find(qn('w:rFonts'))
        if rf is None:
            rf = OxmlElement('w:rFonts')
            rpr.append(rf)
        for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            rf.set(qn(a), name)

    def feldseite(absatz):
        for typ, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
            r = absatz.add_run()
            if typ:
                fc = OxmlElement('w:fldChar')
                fc.set(qn('w:fldCharType'), typ)
                r._r.append(fc)
            else:
                it = OxmlElement('w:instrText')
                it.text = txt
                r._r.append(it)

    def grundgeruest(kennung, fusstext):
        doc = Document()
        st = doc.styles
        schrift(st['Normal'], 'Instrument Sans', 10.5)
        st['Normal'].paragraph_format.space_after = Pt(6)
        st['Normal'].paragraph_format.line_spacing = 1.25
        schrift(st['Title'], 'Archivo', 24, True)
        schrift(st['Heading 1'], 'Archivo', 16, True)
        schrift(st['Heading 2'], 'Archivo', 12.5, True)
        st['Title'].element.get_or_add_pPr()
        for name in ('Title', 'Heading 1', 'Heading 2'):
            st[name].paragraph_format.space_before = Pt(12 if name != 'Title' else 0)
            st[name].paragraph_format.space_after = Pt(6)
        # Titel ohne die blaue Linie der Standardvorlage
        pbdr = st['Title'].element.pPr.find(qn('w:pBdr'))
        if pbdr is not None:
            st['Title'].element.pPr.remove(pbdr)
        s = doc.sections[0]
        s.page_width, s.page_height = Mm(210), Mm(297)
        s.top_margin, s.bottom_margin = Mm(26), Mm(24)
        s.left_margin = s.right_margin = Mm(18)
        s.header_distance, s.footer_distance = Mm(10), Mm(10)
        kopf = s.header.paragraphs[0]
        # Die Standard-Tabulatoren der Kopf- und Fusszeile (Mitte, rechts) loeschen
        for absatz in (kopf, s.footer.paragraphs[0]):
            for pos in (Inches(3.25), Inches(6.5)):
                absatz.paragraph_format.tab_stops.add_tab_stop(pos, WD_TAB_ALIGNMENT.CLEAR)
        kopf.paragraph_format.tab_stops.add_tab_stop(Mm(174), WD_TAB_ALIGNMENT.RIGHT)
        kopf.add_run().add_picture(absender, height=Mm(6))
        r = kopf.add_run('\t' + kennung)
        r.font.name, r.font.size = 'JetBrains Mono', Pt(7.5)
        r.font.color.rgb = RGBColor(0x52, 0x60, 0x53)
        fuss = s.footer.paragraphs[0]
        fuss.paragraph_format.tab_stops.add_tab_stop(Mm(174), WD_TAB_ALIGNMENT.RIGHT)
        r = fuss.add_run(fusstext + '\t')
        r.font.name, r.font.size = 'JetBrains Mono', Pt(7)
        r.font.color.rgb = RGBColor(0x52, 0x60, 0x53)
        feldseite(fuss)
        return doc

    def schattierte_box(doc, kennzeile, text):
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        zelle = t.cell(0, 0)
        tcpr = zelle._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear'), shd.set(qn('w:fill'), 'F1F4F1')
        tcpr.append(shd)
        rand = OxmlElement('w:tcBorders')
        links = OxmlElement('w:left')
        for k, v in (('w:val', 'single'), ('w:sz', '24'), ('w:color', '117011')):
            links.set(qn(k), v)
        rand.append(links)
        tcpr.append(rand)
        p = zelle.paragraphs[0]
        r = p.add_run(kennzeile)
        r.font.name, r.font.size, r.font.color.rgb = 'JetBrains Mono', Pt(8), RGBColor(0x11, 0x70, 0x11)
        zelle.add_paragraph(text)
        doc.add_paragraph()

    # Arbeitsblatt
    doc = grundgeruest('ARBEITSBLATT', 'mius.ch · CC BY-SA 4.0')
    doc.add_paragraph('Titel des Arbeitsblatts', style='Title')
    doc.add_paragraph('Kurze Einleitung: worum es geht und was die Lernenden am Ende können.')
    schattierte_box(doc, 'AUFTRAG', 'Formuliere den Auftrag in ganzen Sätzen und in der Du-Form.')
    doc.add_paragraph('Zwischentitel', style='Heading 1')
    doc.add_paragraph('Text, Material oder Platz für Antworten.')
    doc.save(VORLAGE / 'mius_arbeitsblatt.docx')

    # Brief und Offerte
    doc = grundgeruest('SAMUEL MÜLLER', 'MIUS · Hauptstrasse 14 · 8272 Ermatingen · info@mius.ch · mius.ch')
    adresse = doc.add_paragraph()
    adresse.paragraph_format.left_indent = Mm(100)
    adresse.paragraph_format.space_before = Mm(14)
    r = adresse.add_run('MIUS, Hauptstrasse 14, 8272 Ermatingen\n')
    r.font.size, r.font.color.rgb = Pt(7), RGBColor(0x52, 0x60, 0x53)
    r.font.underline = True
    adresse.add_run('Schule\nVorname Nachname\nStrasse Nummer\nPLZ Ort')
    datum = doc.add_paragraph('Ermatingen, Datum')
    datum.paragraph_format.space_before = Mm(16)
    doc.add_paragraph('Betreff in einer Zeile', style='Heading 1')
    doc.add_paragraph('Guten Tag Vorname Nachname')
    doc.add_paragraph('Text des Briefs. In der Schweiz steht nach der Anrede kein Komma, der erste Satz beginnt gross.')
    doc.add_paragraph('Freundliche Grüsse\n\n\nSamuel Müller')
    doc.save(VORLAGE / 'mius_brief_offerte.docx')

    # Rechnung (oberer Teil; der QR-Zahlteil kommt aus dem Bank- oder Buchhaltungsprogramm)
    doc = grundgeruest('RECHNUNG', 'MIUS · Hauptstrasse 14 · 8272 Ermatingen · info@mius.ch · mius.ch')
    adresse = doc.add_paragraph()
    adresse.paragraph_format.left_indent = Mm(100)
    adresse.paragraph_format.space_before = Mm(14)
    adresse.add_run('Schule\nVorname Nachname\nStrasse Nummer\nPLZ Ort')
    doc.add_paragraph('Rechnung Nr. JJJJ-000', style='Heading 1').paragraph_format.space_before = Mm(14)
    doc.add_paragraph('Ermatingen, Datum · zahlbar innert 30 Tagen')
    t = doc.add_table(rows=4, cols=2)
    for i, (a, b) in enumerate((('Leistung', 'CHF'), ('Workshop, Anzahl Lektionen', '0.00'),
                                ('Material', '0.00'), ('Total', '0.00'))):
        t.cell(i, 0).text, t.cell(i, 1).text = a, b
        t.cell(i, 1).paragraphs[0].alignment = 2
        if i in (0, 3):
            for c in (t.cell(i, 0), t.cell(i, 1)):
                c.paragraphs[0].runs[0].font.bold = True
    hinweis = doc.add_paragraph('Unten bleiben 105 mm frei für den QR-Zahlteil aus dem Bank- oder Buchhaltungsprogramm. '
                                'Der Zahlteil ist genormt und wird nicht gestaltet.')
    hinweis.paragraph_format.space_before = Mm(10)
    hinweis.runs[0].font.size = Pt(8)
    hinweis.runs[0].font.color.rgb = RGBColor(0x52, 0x60, 0x53)
    doc.save(VORLAGE / 'mius_rechnung.docx')

    # Kursbestaetigung
    doc = grundgeruest('KURSBESTÄTIGUNG', 'MIUS · Hauptstrasse 14 · 8272 Ermatingen · mius.ch')
    p = doc.add_paragraph('Hiermit wird bestätigt, dass')
    p.paragraph_format.space_before = Mm(20)
    t = doc.add_table(rows=1, cols=2)
    t.autofit = False
    t.columns[0].width = t.cell(0, 0).width = Mm(16)
    t.columns[1].width = t.cell(0, 1).width = Mm(158)
    t.cell(0, 0).paragraphs[0].add_run().add_picture(str(TUNNEL_PNG), height=Mm(30))
    zelle = t.cell(0, 1)
    zelle.vertical_alignment = 1
    r = zelle.paragraphs[0].add_run('«Vorname Nachname»')
    r.font.name, r.font.size, r.font.bold = 'Archivo', Pt(26), True
    doc.add_paragraph('an der Weiterbildung teilgenommen hat:').paragraph_format.space_before = Mm(6)
    doc.add_paragraph('Titel der Weiterbildung', style='Title')
    doc.add_paragraph('Anzahl Lektionen · Datum · Ort')
    doc.add_paragraph('Inhalte: kurze Aufzählung der Themen in ein bis zwei Sätzen.')
    u = doc.add_paragraph('\n\n______________________________\nSamuel Müller, Kursleitung')
    u.paragraph_format.space_before = Mm(20)
    doc.save(VORLAGE / 'mius_kursbestaetigung.docx')
    print('Vorlagen: Arbeitsblatt, Brief, Rechnung, Kursbestätigung')


def tunnel_png(ws):
    pfad = d(TUNNEL)
    svgt = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 286 912"><path fill="{POSITIV["tunnel"]}" d="{pfad}"/></svg>'
    ws.png(html_rahmen(svg_in_groesse(svgt, 94, 300)), TUNNEL_PNG, 94, 300)


def signatur_html():
    html = '''<!-- E-Mail-Signatur MIUS. In Outlook oder Apple Mail als HTML-Signatur einfuegen.
     Das Bild liegt auf der Website, damit es nicht als Anhang mitgeschickt wird. -->
<table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:1.45;color:#141A15">
  <tr>
    <td style="padding:10px 14px 0 0;vertical-align:top;border-top:1px solid #D9DDDA">
      <img src="https://mius.ch/marke/mius-signatur.png" width="44" height="38" alt="MIUS" style="display:block">
    </td>
    <td style="padding:10px 0 0;vertical-align:top;border-top:1px solid #D9DDDA">
      <strong>Samuel Müller</strong><br>
      <span style="color:#3A453B">MIUS · Medien | Informatik | Unterricht | Schule</span><br>
      <span style="color:#526053;font-size:12px">Hauptstrasse 14, 8272 Ermatingen ·
      <a href="https://mius.ch" style="color:#117011;text-decoration:none">mius.ch</a></span>
    </td>
  </tr>
</table>
'''
    (VORLAGE / 'mius_email_signatur.html').write_text(html, encoding='utf-8')


# --------------------------------------------------------------------------
# Farbfelder fuer Grafikprogramme
# --------------------------------------------------------------------------
FARBEN = [
    ('Tunnel', '141E00', 'Logo'), ('Balken', '117011', 'Logo'), ('Gelenk', '2B8F2B', 'Logo'),
    ('Fundament', '003D3D', 'Logo'), ('Tiefton', '001313', 'Logo'),
    ('Gruen hell (negativ)', '36B436', 'Erweiterung'), ('Teal hell (negativ)', '298888', 'Erweiterung'),
    ('Teal', '206B6B', 'Erweiterung'), ('Tunnel negativ', '3F5F00', 'Erweiterung'),
    ('Oliv Markierfarbe', '80A732', 'Erweiterung'),
    ('Grund hell', 'FCFDFC', 'Neutral'), ('Flaeche', 'ECEEEC', 'Neutral'), ('Linie', 'D9DDDA', 'Neutral'),
    ('Text leise', '526053', 'Neutral'), ('Text', '141A15', 'Neutral'), ('Grund dunkel', '0B0F0B', 'Neutral'),
]


def farben():
    def rgb(h):
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    # Adobe Swatch Exchange
    bloecke = b''
    for name, hexw, _ in FARBEN:
        n = (name + '\0').encode('utf-16-be')
        inhalt = struct.pack('>H', len(n) // 2) + n + b'RGB ' + struct.pack('>fff', *[c / 255 for c in rgb(hexw)]) + struct.pack('>H', 2)
        bloecke += struct.pack('>HI', 1, len(inhalt)) + inhalt
    (FARBE / 'mius.ase').write_bytes(b'ASEF' + struct.pack('>HHI', 1, 0, len(FARBEN)) + bloecke)
    # GIMP, Inkscape, Krita
    zeilen = ['GIMP Palette', 'Name: MIUS', 'Columns: 5', '#']
    zeilen += ['%3d %3d %3d\t%s' % (*rgb(h), n) for n, h, _ in FARBEN]
    (FARBE / 'mius.gpl').write_text('\n'.join(zeilen) + '\n', encoding='utf-8')
    (FARBE / 'mius_farben.json').write_text(json.dumps(
        [{'name': n, 'hex': '#' + h, 'rgb': rgb(h), 'gruppe': g} for n, h, g in FARBEN],
        ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Farben: ASE, GPL, JSON (tokens.css ist Quelle, bleibt unberuehrt)')


def main():
    for ordner in (LOGO / 'svg', LOGO / 'png', LOGO / 'pdf', WEB, VORLAGE / 'social', FARBE, DRUCK):
        ordner.mkdir(parents=True, exist_ok=True)
    schriften()
    logos_svg = logos()
    ws = Werkstatt()
    try:
        rastern(ws, logos_svg)
        tunnel_png(ws)
        web(ws, logos_svg)
        druck(ws, logos_svg)
        social(ws, logos_svg)
    finally:
        ws.schliessen()
    folienmaster()
    word_vorlagen()
    signatur_html()
    farben()
    print('Fertig.')


if __name__ == '__main__':
    main()
