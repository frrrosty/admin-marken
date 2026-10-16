# Marken-Repository

Hier liegen die Erscheinungsbilder von Samuel Müller. Wird in einem anderen
Projekt eine dieser Marken gebraucht, gelten die Dateien hier als Quelle.

- `mius/` – MIUS. Einstieg `mius/README.md`, vollständiges Regelwerk
  `mius/erscheinungsbild.html`. Farben in `mius/04_Farben/tokens.css` und
  `mius_farben.json`, Logos in `mius/01_Logo/`. Quelle sind
  `mius/quelle/erzeugen.py`, `mius/02_Schriften/quelle/` und
  `mius/04_Farben/tokens.css`; alles andere erzeugt das Skript. Erzeugte Dateien
  nie von Hand ändern, sondern die Quelle anpassen und neu erzeugen.
- `fotiziit/` – Fotiziit. Einstieg `fotiziit/README.md`, Werte in
  `fotiziit/tokens.json` und `tokens.css`, Logos in `fotiziit/logos/`.
  Dunkel ist das Grundthema. Die SVG-Dateien sind selbst die Quelle;
  `tokens.css` wird aus `tokens.json` abgeleitet.

Dieses Repository ist die einzige Quelle. Websites und andere Projekte binden
es als Git-Submodul ein (mius-website unter `marken/`) und kopieren beim Bauen,
was sie brauchen. Das Design System «Fotiziit» und das MIUS-Handbuch auf
claude.ai sind nur Ansichten; Änderungen gehören hierher.

Regeln für alle Marken: Logos nie neu setzen oder verändern, nur die Dateien
verwenden. Texte in Schweizer Rechtschreibung (ss, keine ß), Anführungszeichen
«so». Keine Farben ausserhalb der jeweiligen Palette.
