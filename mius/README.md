# MIUS – Markenhandbuch

MIUS steht für Medien, Informatik, Unterricht, Schule: das Einzelunternehmen
von Samuel Müller, Ermatingen. Das vollständige Regelwerk steht in
[erscheinungsbild.html](erscheinungsbild.html) (im Browser öffnen).

## Das Wichtigste in Kürze

- **Signet:** Der dunkle Rahmen ist ein Tunnel und steht für «Rahmen und Fokus».
  Die zwei dunkelgrünen Balken sind das M, der hellgrüne das I, dahinter U und S
  in Teal. Grün steht für das Fach, Teal für den Ort. Das Signet wird nie
  verändert, gedreht, umgefärbt oder überdeckt.
- **Fassungen:** Hauptlogo mit Claim ab 50 mm bzw. 180 px; Signet allein ab
  8 mm bzw. 24 px; Absenderzeile (Signet und «mius.ch») für Kopfzeilen, Folien
  und Social Media; einfarbig für Stempel und Gravur. Schutzraum ringsum eine
  Balkenbreite.
- **Farben:** Tunnel `#141E00`, Balken `#117011`, Gelenk `#2B8F2B`,
  Fundament `#003D3D`, Tiefton `#001313`. Text auf Weiss in `#117011` oder
  dunkler, nie in `#2B8F2B`. Werbemittel im Tiefton.
- **Schrift:** Josefin Sans nur für Claim und Domain, Archivo für Titel,
  Instrument Sans für Text, JetBrains Mono für Daten und Kennzeilen.
- **Neigung:** 20,9°, abgelesen an den Balkenunterkanten. Eine einzige Schräge
  für Claim, Bildbalken und Kennbalken.
- **Sprache:** Ich und Du, Schweizer Rechtschreibung, Claim immer
  «Medien | Informatik | Unterricht | Schule».

## Dateien

```
00_Original/    alte Logodateien als Beleg, nicht verwenden
01_Logo/        8 Fassungen als SVG, PNG und PDF
  web/          Favicon, App-Symbol, Link-Vorschau, Signaturbild
02_Schriften/   10 statische Schnitte mit Lizenz (OFL)
  quelle/       variable Originale von Google Fonts (Quelle)
03_Vorlagen/    Folienmaster, Word-Vorlagen, E-Mail-Signatur, Social Media
04_Farben/      tokens.css (Quelle), Farbfelder als ASE, GPL und JSON
05_Druckdaten/  Visitenkarte, Sticker, Namensschilder (RGB, mit Beschnitt)
quelle/         erzeugen.py und requirements.txt
```

Dateinamen folgen dem Muster `mius_fassung_farbe.format`.

## Quelle und erzeugte Dateien

Dieser Ordner ist die einzige Quelle der Marke MIUS. Von Hand gepflegt werden
nur drei Dinge:

- `quelle/erzeugen.py` mit der Geometrie des Signets, den Fassungen und Vorlagen
- `02_Schriften/quelle/` mit den Schriftdateien von Google Fonts
- `04_Farben/tokens.css` mit allen Farb- und Masswerten

Alles andere erzeugt das Skript:

```
pip install -r mius/quelle/requirements.txt
python -m playwright install chromium
python mius/quelle/erzeugen.py
```

Die erzeugten Dateien sind bewusst eingecheckt, damit sie ohne Skript bereitstehen.
Bei jedem Push prüft eine GitHub Action, ob SVG, Schriften und Farbfelder zur
Quelle passen. Eine von Hand geänderte Datei lässt die Prüfung fehlschlagen.

Die Website mius.ch (Repository frrrosty/mius-website) bindet dieses
Repository als Git-Submodul ein und kopiert Signet, Favicon, Link-Vorschau und
`tokens.css` beim Bauen. Dort liegen keine eigenen Markendateien.

## Hinweise

- Office-Vorlagen brauchen Archivo und Instrument Sans auf dem Rechner. Für
  die Weitergabe an Schulen als PDF exportieren.
- Die Rechnungsvorlage hält unten 105 mm für den QR-Zahlteil frei. Der
  Zahlteil ist genormt und kommt aus dem Bank- oder Buchhaltungsprogramm.
- Druckdaten sind RGB. Vor dem ersten Druck einen Andruck machen und die
  CMYK-Werte mit der Druckerei festlegen.
