# Marken

Die Erscheinungsbilder von Samuel Müller an einem Ort. Jede Marke hat einen
eigenen Ordner mit Handbuch, Logos, Schriften, Farben und Vorlagen.

| Marke | Wofür | Einstieg |
|---|---|---|
| [MIUS](mius/README.md) | Medien, Informatik, Unterricht, Schule: Weiterbildung, Beratung, Unterrichtsmaterial | [mius/erscheinungsbild.html](mius/erscheinungsbild.html) |
| [Fotiziit](fotiziit/README.md) | Foto-Portfolio: Landschaft, Nacht, Luft, Aufträge, Prints | [fotiziit/README.md](fotiziit/README.md) |

## So holst du eine Marke in ein Projekt

**Einzelne Dateien:** direkt aus dem Ordner kopieren, zum Beispiel
`mius/01_Logo/svg/mius_signet_positiv.svg` oder `fotiziit/tokens.css`.

**Ganzes Repository als Unterordner** in einem anderen Projekt:

```
git submodule add https://github.com/frrrosty/admin-marken marken
git submodule update --remote marken   # später: neuesten Stand holen
```

**Mit Claude:** im neuen Projekt sagen, welche Marke gilt, zum Beispiel
«Verwende das Erscheinungsbild von MIUS aus frrrosty/admin-marken». Die Datei
`CLAUDE.md` in diesem Repository sagt, wo was liegt.

## Quelle

Dieses Repository ist die einzige Quelle beider Marken. Die Seiten auf
claude.ai (Fotiziit-Design-System, MIUS-Handbuch) sind Ansichten und werden
hier nicht nachgeführt, sondern bei Bedarf von hier aus neu veröffentlicht.

## Regeln für dieses Repository

- Pro Marke ein Ordner in Kleinbuchstaben, ohne Umlaute.
- Jede Marke hat eine `README.md` als Einstieg und ihre Farbwerte maschinenlesbar
  (`tokens.json` oder `04_Farben/`).
- Logos werden nie neu aus der Schrift gesetzt, immer die Dateien verwenden.
- Schriften liegen nur bei, wenn die Lizenz die Weitergabe erlaubt (hier alle OFL).
