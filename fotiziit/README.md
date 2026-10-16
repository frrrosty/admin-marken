# Fotiziit – Markenhandbuch

Stand 15. Oktober 2026. Übernommen aus dem Design System «Fotiziit»
(claude.ai/artifact/R2dKNAWRtjyFYJEuNhAh8S). Die Reinzeichnungen der Logos
stammen von dort und werden hier nicht verändert.

## Dateien

```
logos/        Wortbild FOTI / ZIIT, gestapelt und einzeilig, als SVG (Schrift in Kurven)
bildzeichen/  Blende mit Pausenbalken, Favicon
exporte/      fertige PNG: Logos 2000 px, Favicon, App-Symbol, Profilbild, Wasserzeichen
schriften/    Instrument Serif, Inter, JetBrains Mono mit Lizenz (OFL)
tokens.json   Farben, Schrift, Abstände, Radien (Quelle)
tokens.css    dieselben Werte als CSS-Variablen; Papier-Thema über .papier
anwendungen.md  Visitenkarte, Social Media, Website, Fine Art Print, Wasserzeichen
```

Archivo ist nur im Logo verwendet und dort bereits in Kurven umgewandelt;
deshalb liegt die Schrift hier nicht bei.

FOTIZIIT ist das Foto-Portfolio von Samuel Müller: Landschafts-, Nacht- und Luftaufnahmen vom Untersee, aus dem Thurgau, vom Bodensee und aus den Alpen. Dazu kommen Aufträge für Immobilien und Architektur, Workshops und Fine Art Prints. Der Name ist Schweizerdeutsch für «Fotozeit» und meint: sich Zeit nehmen fürs Fotografieren. Leitsatz: «Nimm dir Fotiziit.»

## Haltung und Sprache

- Schreibe ruhig, handwerklich und persönlich. Keine Superlative, kein Werbeton, «kein kitschiger Schnickschnack, sondern zeitlose Ästhetik».
- Schreibe in Schweizer Rechtschreibung: immer «ss», nie «ß». Anführungszeichen «so».
- Schreibe die Marke im Fliesstext «Fotiziit», im Logo und in Überschriften aus Versalien «FOTIZIIT». Die Adresse ist fotiziit.ch.
- Nutze Kameradaten als Beschriftung, nicht als Dekoration: echte Werte wie `f/11 · 1/60 s · ISO 200` oder Ortsangaben wie `47.66° N 9.08° E`.
- Keine Emojis in Drucksachen und auf der Website. In Social-Media-Texten höchstens eines, wenn es passt.
- Beispiele für den Ton: «Momente festhalten, die Geschichten erzählen.» · «Zeit fürs Bild.» · «Mal Pause. Mal Foti.»

## Logo

Das Logo ist das gestapelte Wortbild FOTI / ZIIT in Archivo Extra Bold. Das O ist eine Blende. Die Dateien liegen unter **Logos**; nutze immer diese Dateien und setze das Logo nie neu aus der Schrift.

- **Standard:** `fotiziit-gestapelt_blende-messing_*`. Das Wort steht in `ink`, nur die Blende in `brass`. Auf dunklem Grund die Datei `_auf-dunkel`, auf Papier die Datei `_auf-hell`.
- **Grosser Auftritt:** `fotiziit-gestapelt_ziit-messing_*` nur für Plakat, Ausstellung und die Startseite, nie neben der Standardfassung.
- **Schmale Formate:** `fotiziit-einzeilig_*` für Kopfzeilen, Fusszeilen und Wasserzeichen.
- **Einfarbig:** `_einfarbig_schwarz` und `_einfarbig_weiss` für Stempel, Gravur, Prägung und Einfarbendruck.
- **Schutzraum:** rundum mindestens die Höhe der Blende (x). In diesem Raum steht nichts, auch keine Bildkante. Masse und Linien zeigt `fotiziit-konstruktion`.
- **Aufbau:** Archivo, Breite 108, Gewicht 800, Laufweite −25/1000 em plus optischer Ausgleich. Lücke zwischen den Zeilen 0,31 x. ZIIT steht linksbündig unter FOTI und wird nicht auf gleiche Breite ausgetrieben.
- **Mindestgrösse:** gestapelt 14 mm oder 56 px breit, einzeilig 30 mm oder 120 px breit.
- **Nie:** verzerren, drehen, umfärben, mit Schatten oder Kontur versehen, die Messingfarbe in die Wortmitte setzen (etwa nur das «II»), auf unruhige Bildstellen legen.

## Bildzeichen

Das Bildzeichen ist die Blende mit zwei Pausenbalken im Zentrum. Die Pause steht für die Auszeit vom Alltag, die Blende für die Fotografie. Die Dateien liegen unter **Bildzeichen**.

- Nutze `signet-blende-pause_kachel` für App-Symbol und Präsentationen, `_rund` für Profilbilder, `_auf-dunkel` und `_auf-hell` für Prints und Passepartouts.
- Unter 32 px verschwinden die Pausenbalken. Nutze dort `favicon-blende` (Blende ohne Pause, Lamellen in `brass` auf `surface-raised`).
- Die Pausenbalken allein sind kein Logo. Sie dürfen als Gestaltungselement auftreten: als Trenner zwischen Textblöcken oder als Ladeanzeige auf der Website.

## Farbe

Fotiziit ist dunkel zuerst: Bilder wirken auf warmem Schwarz am besten. Das Papier-Thema gilt für Drucksachen, Offerten und Dokumente.

- Setze Seiten auf `ground`, Flächen auf `surface` und `surface-raised`, Text in `ink`, Nebentext in `ink-muted`.
- `brass` ist der einzige Akzent: Logo-Blende, Links, eine Hervorhebung pro Ansicht. Auf Papier ist `brass` nur für Flächen, Logo und Schrift ab 24 px zugelassen; für kleinen Akzenttext nutze `brass-text`.
- `ink-dim` und `line` tragen keinen Lesetext, nur Linien, Rahmen und Sucherecken.
- Keine weiteren Farben. Farbe kommt aus den Fotos.

## Schrift

- **Titel:** Instrument Serif (`display`), Stile `display-xl`, `display-l`, `display-m`. Sparsam, eine Titelgrösse pro Ansicht.
- **Text:** Inter (`sans`), Stile `lead`, `body`, `small`.
- **Daten:** JetBrains Mono (`mono`), Stil `data`, in Versalien mit 0,08 em Laufweite. Für Kameradaten, Orte, Beschriftungen und Etiketten.
- **Logo:** Archivo nur im Logo. Setze damit keinen Text.

## Gestaltungselemente

- **Sucherecken:** vier Winkel in `brass` oder `line` rahmen ein Bild oder einen Titel. Strichstärke 2 px, Schenkel ein Viertel der Höhe.
- **Kameradaten-Zeile:** Mono in `ink-muted` über oder unter dem Bild.
- **Filmkorn:** feines Rauschen über dunklen Flächen, höchstens 6 % Deckkraft.
- **Belichtungsskala:** feine Teilstriche als Trenner, in `line`.
- Ecken: Bilder und Abzüge `radius-sm`, Karten und Bögen `radius-md`, App-Symbol `radius-signet`. Keine Schatten.

## Exporte

Fertige PNG-Dateien unter **Exporte**: `favicon-32`, `apple-touch-icon-180`, `favicon-512` und `app-symbol-512` für Website und App, `profilbild-1080` für Social Media, `wasserzeichen-weiss` für Lightroom, das Logo in 2000 px Breite auf dunkel und hell, das Konstruktionsblatt. Für Druck immer die SVG-Dateien verwenden.

## Bildsprache

- Natürliche Farben, ruhige Kompositionen, viel Himmel und Wasser. Blaue Stunde, Nacht, Nebel, Vogelperspektive.
- Keine übersättigten HDR-Looks, keine Filter-Trends.
- Wasserzeichen: einzeiliges Logo, unten rechts, Abstand mindestens die Blendenhöhe vom Rand, 70 bis 80 % Deckkraft, auf dunkel `_einfarbig_weiss`.

## Offen

Spacing- und Radius-Werte sowie das Papier-Thema stammen aus den Entwürfen, nicht aus dem Code der Website. CMYK- und Pantone-Werte für `brass` und `ground` werden nach einem Probedruck ergänzt. Die Logos sind reingezeichnet (Schrift in Kurven, Blende aus echten Kreisbögen). Vor dem ersten Druck braucht es eine Sichtkontrolle in Affinity Designer und einen Probedruck bei Mindestgrösse.
