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
01_Logo/        8 Fassungen als SVG, PNG und PDF
  web/          Favicon, App-Symbol, Link-Vorschau
02_Schriften/   10 statische Schnitte mit Lizenz (OFL)
03_Vorlagen/    Folienmaster, Word-Vorlagen, E-Mail-Signatur, Social Media
04_Farben/      Farbfelder als ASE, GPL, JSON und CSS
05_Druckdaten/  Visitenkarte, Sticker, Namensschilder (RGB, mit Beschnitt)
```

Dateinamen folgen dem Muster `mius_fassung_farbe.format`.

## Herkunft und Aktualisierung

Alle Dateien erzeugt `marke/erzeugen.py` im Repository
[frrrosty/mius-website](https://github.com/frrrosty/mius-website). Dort steht
die Geometrie des Signets als Quelle. Nach einer Änderung dort neu erzeugen
und den Ordner `marke/` hierher kopieren, damit beide Stände gleich bleiben.

## Hinweise

- Office-Vorlagen brauchen Archivo und Instrument Sans auf dem Rechner. Für
  die Weitergabe an Schulen als PDF exportieren.
- Die Rechnungsvorlage hält unten 105 mm für den QR-Zahlteil frei. Der
  Zahlteil ist genormt und kommt aus dem Bank- oder Buchhaltungsprogramm.
- Druckdaten sind RGB. Vor dem ersten Druck einen Andruck machen und die
  CMYK-Werte mit der Druckerei festlegen.
