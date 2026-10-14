# KI-Prüfstand

Eigene Aufgaben, die auf allen lokal getesteten Modellen laufen. Pro Modell und Aufgabe wird festgehalten, ob die
Aufgabe gelöst wurde, die Zeit, die Erzeugungsgeschwindigkeit (tok/s) und die Zahl der erzeugten Tokens.
Daraus entsteht eine einzelne HTML-Seite (`site/index.html`).

## Einrichten

```bash
cd fork/arena
uv venv .venv && uv pip install --python .venv/bin/python -r requirements.txt
```

`bwrap` (bubblewrap) muss installiert sein: Programmieraufgaben laufen darin ohne Netz und mit nur lesendem Zugriff
auf `/usr`.

## Ablauf

```bash
.venv/bin/python -m arena.check                         # neue Aufgaben gegen ihre Musterlösung prüfen
.venv/bin/python -m arena.run --model all               # jedes Modell aus models.toml starten und testen
.venv/bin/python -m arena.run --model qwen3-vl-8b --task meine-aufgabe
.venv/bin/python -m arena.run --url http://127.0.0.1:1919/v1 --name mein-server --caps vision
.venv/bin/python -m arena.build_site                    # site/index.html neu bauen
```

`arena.run` startet pro Modell `ft serve` mit den Flags aus `models.toml`, wartet auf `/health`, schickt die
Aufgaben nacheinander (Temperatur 0, gestreamt) und beendet den Server wieder. Ergebnisse werden an
`results/runs.jsonl` angehängt, das Server-Log steht in `results/logs/<modell>.log`. Aufgaben mit aktuellem
Ergebnis werden übersprungen. Eine neue Aufgabe läuft also nur dort, wo sie noch fehlt. `--force` wiederholt alles.

Jede Aufgabe bekommt einen Fingerabdruck aus allen ihren Dateien (außer `musterloesung.md`). Wird eine Aufgabe
geändert, gelten ihre alten Ergebnisse als veraltet: Sie zählen nicht mehr in der Rangliste und `arena.run` führt
sie beim nächsten Lauf neu aus.

## Eine Aufgabe anlegen

Ein Ordner unter `aufgaben/` ist eine Aufgabe, der Ordnername ist ihre id. Am einfachsten kopierst du eine Vorlage:

```bash
cp -r vorlagen/code-beispiel aufgaben/code-json-parser
```

| Vorlage | Kategorie | Prüfung |
|---|---|---|
| `vorlagen/code-beispiel` | Programmieren | `python_tests`: Code aus der Antwort gegen `tests.py` |
| `vorlagen/svg-beispiel` | Bild | `svg_reference`: SVG rendern, Pixel mit `reference.svg` vergleichen |
| `vorlagen/bild-lesen-beispiel` | Bild | `answer`: Bild als Eingabe, nur für Modelle mit `vision` |
| `vorlagen/text-beispiel` | Textverständnis | `answer`: Dokument im Prompt, Begriffe in der `ANTWORT:`-Zeile |

### task.toml

```toml
title = "Kurzer Name"              # erscheint auf der Seite
category = "code"                  # code | image | text
level = "mittel"                   # leicht | mittel | schwer (nur Anzeige)
summary = "Ein Satz, was geprüft wird."
max_tokens = 8192                  # Obergrenze für die Antwort inkl. Denkphase
prompt = """..."""                 # oder prompt_file = "prompt.md"
attach = ["dokument.md"]           # optional: {{dokument.md}} im Prompt wird durch die Datei ersetzt
images = ["bild.png"]              # optional: Bilder vor dem Text, macht die Aufgabe zu needs = ["vision"]
needs = ["vision"]                 # optional: nur Modelle mit diesen caps (models.toml)

[check]
type = "..."                       # siehe unten
```

### Prüfungen

**`python_tests`**: Der längste ```python-Block der Antwort wird als Modul `solution` geladen, danach läuft jede
Funktion `test_*` aus `tests.py` einzeln (ein Fehler oder Timeout betrifft nur diesen Test). Punkte = Anteil
bestandener Tests, gelöst = alle bestanden.

```toml
[check]
type = "python_tests"
tests = "tests.py"                 # Standard
forbidden = ['\beval\s*\(']        # Regex-Muster, die im Code nicht vorkommen dürfen
per_test_seconds = 5
```

**`pascal_tests`**: Der Delphi-/Pascal-Codeblock der Antwort wird mit Free Pascal im Delphi-Modus (`fpc -Mdelphi`)
zusammen mit den Prozeduren `Test_*` aus `tests.pas` zu einem Programm kompiliert. Die Antwort darf eine nackte
Funktion, eine Unit oder ein Konsolenprogramm sein. `uses`-Klauseln werden zusammengeführt, `System.`-Präfixe entfernt,
VCL-/Windows-Units verworfen. In `tests.pas` stehen `Check(Bedingung, 'Text')` und
`CheckNear(Ist, Soll, Toleranz, 'Text')` zur Verfügung. Braucht das Paket `fp-compiler`.

```toml
[check]
type = "pascal_tests"
tests = "tests.pas"
forbidden = ['\bWindows\b']      # optional, Regex ohne Groß-/Kleinschreibung
```

**`svg_reference`**: Das letzte `<svg>...</svg>` der Antwort wird in `width` x `height` gerendert und mit der
Referenz verglichen. Kanten (2 px um jeden Farbwechsel der Referenz) zählen nicht, damit Kantenglättung und
gleichwertige Formen keine Rolle spielen. Punkte = Anteil übereinstimmender Flächenpixel.

```toml
[check]
type = "svg_reference"
reference = "reference.svg"
width = 200
height = 200
min_match = 0.98                   # ab diesem Anteil gilt die Aufgabe als gelöst
color_tolerance = 48               # erlaubte Abweichung pro Farbkanal (0-255)
```

**`answer`**: Geprüft wird die letzte Zeile `ANTWORT: ...` (fehlt sie, die ganze Antwort). Groß-/Kleinschreibung
ist egal, Tausenderpunkte werden ignoriert (`4.850` = `4850`). Bitte im Prompt um diese Zeile.

```toml
[check]
type = "answer"
all = ["apr", "71"]                # muss alles enthalten
any = ["0,38", "38 cent"]          # mindestens eins davon
none = ["0,30"]                    # darf nichts davon enthalten
regex = "0[,.]38"                  # optional
final_line = true                  # false = ganze Antwort prüfen
```

Für Freitext-Antworten (z. B. Code-Review: "Welche Fehler enthält der Code?") gibt es Gruppen. Jede Gruppe ist ein
Punkt, den die Antwort irgendwo nennen muss, als Regex mit Alternativen für verschiedene Formulierungen. Mit Gruppen
wird standardmäßig die ganze Antwort geprüft. Die Antwort ist vorher kleingeschrieben und Zeilenumbrüche sind
Leerzeichen. Punkte = Anteil gefundener Gruppen. Beispiel: `aufgaben/delphi-code-review`.

```toml
[[check.groups]]
name = "StringList wird nicht freigegeben"
regex = '''speicherleck|memory[ -]?leak|(nicht|nie)[^.]{0,60}?freigegeben|\.free\b'''
```

Eine Gruppe mit `must_not = true` bestraft eine falsche Aussage: Trifft ihr Regex, fällt dieser Punkt durch.
`unless_before` entschuldigt Treffer mit einer Verneinung im Treffer selbst oder davor im selben Teilsatz
("liefert nicht etwa einen leeren String, sondern ..."):

```toml
[[check.groups]]
name = "behauptet, die Funktion liefere einen leeren String"
must_not = true
regex = '''(liefert|gibt|returns?)[^.,]{0,40}?(leere[nrs]?\s+string|empty\s+string)'''
unless_before = '''\b(nicht|kein\w*|nie|not|statt)\b'''
```

### Nachfrage

Nennt ein Modell nur einen Teil der Antwort, kann es sich in einer zweiten Runde erklären. Die Nachfrage wird im
selben Gespräch gestellt, wenn nach der ersten Antwort alle `when_missing`-Gruppen fehlen und alle
`when_found`-Gruppen gefunden wurden (Gruppennamen aus `[[check.groups]]`). Geprüft wird danach erste Antwort plus
Erklärung, Strafgruppen gelten also auch für die Erklärung. Zeit und Tokens beider Runden zählen zusammen. Auf der
Seite steht so ein Ergebnis als "gelöst nach Nachfrage" (✓<sup>N</sup>). Die Punkte werden mit `score_factor`
multipliziert (Standard 0.75): gelöst nach Nachfrage zählt in der Rangliste 0,75 statt 1. Beispiel:
`aufgaben/delphi-result-init`.

```toml
[[followups]]
when_found = ["Result wird vor der Schleife nicht mit '' initialisiert"]
when_missing = ["Folge: an den alten Wert der Zielvariable wird angehängt"]
prompt = "Warum führt das in diesem Fall zu einem Fehler? Erkläre, was dabei in Delphi intern passiert."
# score_factor = 0.75
```

### Musterlösung

Leg zu jeder Aufgabe eine `musterloesung.md` ab, also so, wie eine perfekte Modellantwort aussähe. `arena.check`
schickt sie durch die Prüfung. Damit merkst du Fehler in Tests oder Referenz, bevor ein Modell daran scheitert.

## Modelle

`models.toml` hat einen Abschnitt pro Modell: `path` (Glob unter `~/.cache/huggingface/hub`), `flags` (zusätzliche
`ft serve`-Flags), `caps` (z. B. `["vision"]`), `label`, `group`, optional `worktree` (Standard
`~/claude/ft-speed-wt`, also Branch `next-speed`) und `skip = true`, um ein Modell aus `--model all` herauszunehmen.

## Ohne GPU testen

`arena.fake_server` beantwortet jede Aufgabe mit ihrer Musterlösung (`--wrong` mit verfälschten Antworten):

```bash
ARENA_RESULTS=/tmp/demo.jsonl .venv/bin/python -m arena.fake_server --tasks-dir vorlagen --port 19199 &
ARENA_RESULTS=/tmp/demo.jsonl .venv/bin/python -m arena.run --tasks-dir vorlagen --url http://127.0.0.1:19199/v1 --name demo --caps vision
ARENA_RESULTS=/tmp/demo.jsonl .venv/bin/python -m arena.build_site --tasks-dir vorlagen --out /tmp/demo.html
```
