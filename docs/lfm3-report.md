# LFM3: Abschlussbericht der Teile 1-5

Stand: 2026-11-06. LFM3-1.7B läuft in bf16, FP8 und NVFP4 auf der RTX 4090.
Teil 5 behebt die Scale-Übersetzung im Gewichtsloader; die Modellarithmetik
und die Architekturregistrierung aus den vorherigen Teilen bleiben erhalten.
Detaillierte Messprotokolle und Befehle stehen in [lfm3.md](lfm3.md), die
Nutzeranleitung und Checkpoint-Tabelle in [models.md](models.md#lfm3-text).

## Korrekturen am ursprünglichen Plan

1. Die vorhandenen Conv-Kernels unterstützten nur Breite 2-4; der Dispatcher
   verdrahtete SiLU fest. Teil 1 ergänzt einen separaten Triton-Pfad für
   Breite 7 ohne Aktivierung, einschließlich kurzer Chunks und Graph-Replay.
2. `SlotStateSpec` erzeugte keinen eigenständigen Pool. `LinearStatePool`
   benötigte zuvor eine GDN-artige Gruppe. `ShortConvGroupConfig` beschreibt
   jetzt ausschließlich die Conv-Historie; es gibt keine künstliche
   GDN-Rekurrenz und keinen zweiten redundanten State-Pool.
3. SWA-Pool und Hybrid-Radix waren nicht kombinierbar. Umgesetzt ist
   **Variante A**: alle 11 Attention-Layer im Full-KV-Pool, auf den fünf
   Sliding-Layern eine Fenstermaske von 256 einschließlich des aktuellen
   Tokens. Das spart keinen SWA-Speicher. **Variante B** bleibt Folgearbeit.
4. Ein wiederverwendbares skalares Per-Head-Gate war in FreeToken nicht
   vorhanden; Qwen3.5 hat ein elementweises Gate. LFM3 selbst besitzt das
   Per-Head-Gate nachweislich. Es wird separat als `sigmoid(gate_proj(x))`
   vor `o_proj` angewandt, nicht aus dem Modell entfernt.
5. Zero-Tail-RoPE existierte bereits als `rope_type='proportional'`.
   Zusätzlich müssen cos/sin vor der Rotation wie bei Liquid auf den
   Aktivierungsdatentyp gerundet werden. Full- und Sliding-Layer haben
   getrennte Frequenzen; normale Partial-RoPE wäre falsch.
6. `_DENSE_PACKED` passt nicht zu `feed_forward.w1/w3`. Die Registrierung
   braucht eigene w1/w3- und w2-Abbildungen. Teil 5 zeigt außerdem: die
   generische QuantConfig ersetzt nicht die Scale-Übersetzung im Loader.
7. Die Parser-Autoauswahl kannte `lfm` nicht. LFM3 nutzt nun `qwen3` für
   Reasoning und `qwen3_coder` für XML-artige Tool-Aufrufe.
8. Transformers 5.18 hat keine eingebaute LFM3-Klasse. Der Snapshot funktioniert
   mit `trust_remote_code=True`; eine neue Transformers-Installation war
   nicht nötig. Ohne `auto_map` genügt für FreeToken der RawConfigShim.
9. Liquid rundet auch RMSNorm vor der Gewichtsmultiplikation und SiLU vor
   dem Gate-Up-Produkt. Außerdem brauchen normalisiertes K und V gleiche
   Zeilenstrides für den KV-Store. Teil 3 korrigiert beides.
10. Modellregistrierung allein genügt nicht: `kernel/aot_models.py` benötigt
    die Checkpoint-Geometrie. Die bestehende Registry-Suite fand die Lücke.
11. Dieser Fork quantisiert standardmäßig online nach FP8. Für echte bf16-
    Parität ist `--online-quant none` nötig. Die Messungen hier behalten
    auch bei quantisierten Snapshots deren gespeicherte Präzision bei.
12. NVFP4 auf sm_89 ist im automatisch gewählten Triton-Backend **W4A16**,
    nicht W4A4-Emulation. `input_scale` wird geladen, aber dort nicht benutzt.
13. Der aktuelle Tasks-Board-Auftrag ersetzt die Branch-Anweisung des alten
    Plans: gearbeitet wurde auf dem vorgegebenen Arbeitsbranch von
    `next-speed`, nicht auf einem neu erzeugten `feat/lfm3`. Kein eigener
    Merge/Push, kein Branchwechsel, keine Änderung an `main`, `ft-next-wt`
    oder `ft-speed-wt`.

## Umsetzung und Design

Teil 1 liefert die aktivierungsfreie kausale Faltung. Teil 2 integriert die
sechs letzten B*x-Werte pro Kanal in den bestehenden Pool-Lebenszyklus:
Slots, Fresh-State, Copy-on-write, Graph-Indizes, Hybrid-Radix-Snapshots und
Rebuild. 13 x 2048 x 6 bf16-Werte kosten 319488 Bytes pro physischem Slot
bei TP=1. Nur Triton erfüllt aktuell die erforderliche Attention-Kombination.

Teil 3 liefert Config, Conv, Attention, Sandwich-Normen, MLP, gebundene
Embeddings/LM-Head, Gewichte und Registrierung. Die 286 bf16-Quelltensoren
werden auf 240 fusionierte Namen abgebildet. Der unabhängige Torch-Vergleich
prüft volle und gechunkte Prefills, Decode, CUDA-Graphs samt Padding,
ungleiche Request-Längen, Slot-Wiederverwendung und echte Radix-Treffer.

Teil 4 validiert den echten bf16-Checkpoint gegen Liquid/HF und die HTTP-APIs:
Thinking, Streaming, Tools mit Folgeantwort, lange Eingabe, Prefix-Hits,
vier parallele Requests und Cache-Rebuild. Teil 5 übersetzt FP8-Blockscales
und NVFP4-Globalskalen vor Fusion/Sharding, erhält unterschiedliche w1/w3-
Globalskalen in fp32 und führt beide echten Quant-Checkpoints aus.

## Messungen und Vergleiche

Hardware: RTX 4090, 24 GB, sm_89; NVIDIA 595.99.02, PyTorch 2.14.1+cu130,
Transformers 5.18.0. Befehle/Revisionen sind in der Validierungsnotiz fixiert.
Die Werte sind Einzelbeobachtungen, keine kontrollierten A/B-Speedups.

| Checkpoint | Gewichte laden | API bereit | KV-Tokens | Prefill tok/s | Decode tok/s |
| --- | ---: | ---: | ---: | ---: | ---: |
| bf16, Teil 4 | 1.73 s | ca. 9 s | 769988 | 35190.20 | 192.90 |
| FP8, Teil 5 | 1.19 s | ca. 11 s | 828635 | 34433.93 | 163.07 |
| NVFP4, Teil 5 | 1.92 s | ca. 15 s | 851863 | 32708.10 | 193.62 |

Prefill: kalte Eingabe mit 8347 Tokens; Decode: Batch 1, bei bf16 219,
bei Quantisierung 50 generierte Tokens. bf16 erreichte im gemessenen
Vier-Request-Decode-Intervall 515.61 aggregierte tok/s.

HF-bf16 gegen FreeToken-bf16, je 50 Greedy-Tokens: Himmel 50/50, Python
50/50, lange Code-Retrieval-Eingabe 50/50. Tomaten divergiert an Position
30 (einsbasiert): HF bevorzugt Token 900 ` &` mit 23.375 gegen Token 207
Newline mit 23.250; FreeToken hat beide bei 23.375 und wählt 207.
Das ist ein exakter Tie auf FT-Seite und eine bf16-ULP auf HF-Seite.
Auch die beiden batchabhängigen Divergenzen aus Teil 4 sind so dokumentiert;
eine allgemeine bitweise Batch-Invarianz wird nicht behauptet.

Quantisierung gegen den gespeicherten kalten bf16-FreeToken-Lauf:

| Prompt | FP8 gleicher Präfix / Divergenzposition | NVFP4 gleicher Präfix / Divergenzposition |
| --- | --- | --- |
| Himmel | 15 / 16 | 11 / 12 |
| Python | 28 / 29 | 0 / 1 |
| Tomaten | 50 / keine innerhalb 50 | 29 / 30 |
| Lange Eingabe, zusätzlich | 12 / 13 | 8 / 9 |

Die Antworten sind verständlich. NVFP4 beginnt die Python-Antwort mit einer
anderen Überschrift; der vollständige Funktionsblock liefert bei Ausführung
`[3, 1, 2]` für `[3, 1, 3, 2, 1]`. Beide Quantisierungen nennen 391 für
17 x 23 mit und ohne Thinking. Einschränkung: NVFP4 schreibt ohne Thinking
zunächst eine falsche Zwischenzeile der schriftlichen Multiplikation,
erklärt danach aber korrekt 340 + 51 = 391. Die lange Eingabe kann trotz
deaktiviertem Thinking Reasoning-Prosa enthalten, auch schon in bf16/HF.
Frühe Quant-Divergenzen sind keine behaupteten bf16-Near-Ties.

FP8: 116 quantisierte lineare Projektionen, 37 bf16. Block-128-Gewichte,
Gruppen-128-Aktivierungen bei GEMM, W8A16 bei einer Zeile. NVFP4: nur die
72 MLP-Projektionen quantisiert, 81 bf16; Triton W4A16. Ignore-Listen und
fusionierte Namen wurden gegen alle entsprechenden Checkpoint-Tensoren geprüft.
GGUF: Header der offiziellen Revision `cd0c74c575b5c416f3011b5b4c298077f26ca8c2`
bestätigt Architektur `lfm3`. Kein Adapter implementiert; das ist wegen
neuer Metadaten-, Tensor- und Paritätsarbeit bewusst zurückgestellt.

## Tests

- Teil 1: 12 sm_89-Kernelvarianten kompiliert, 40 CPU-Triton-Interpreter-
  Vergleiche erfolgreich; damaliger Pytest-Lauf 1 bestanden / 33 übersprungen
  wegen fehlendem CUDA-Zugriff. Spätere GPU-Suites decken die Kernels mit ab.
- Teil 2: 1371 bestanden / 234 übersprungen / 5 abgewählt; gezielt 81 bestanden.
- Teil 3: 15 Modellparitäten; abschließend 2580 bestanden / 252 übersprungen /
  5 abgewählt. Fehlender AOT-Eintrag vorher gefunden und korrigiert.
- Teil 4: 1419 bestanden / 214 übersprungen / 5 abgewählt; echter Cache-Rebuild
  zusätzlich 1 bestanden in 19.20 s.
- Teil 5: eigenständige LFM3-Suite 17 bestanden in 9.19 s. Zwei neue Fälle
  prüfen unabhängige FP8/NVFP4-Dequantisierung mit verschiedenen Globalskalen
  und getrennten Shards. Eine Mutation aller Globals auf 1 scheitert an der
  numerischen Assertion (relative Abweichung 3); danach wiederhergestellt.

Die Laufzahlen gehören zu unterschiedlichen Suite-Umfängen und werden nicht
addiert. Die vollständige Abschlusssuite samt Bereinigung wird unten festgehalten.

## Commits

Alle folgenden Commits sind in der Historie des aktuellen Arbeitsbranches
enthalten; es gibt hier keine neu erstellten Commits auf `feat/lfm3`.

| Commit | Inhalt |
| --- | --- |
| `147cfed5` | Breite-7-Conv ohne Aktivierung; ursprüngliche Plan-Korrekturen |
| `a2a46857` | Short-Conv-State, Full-KV-Fenster, Backend und Forecast |
| `cd8cb0c8` | LFM3-Config, Registrierung und Parser |
| `82911d65` | Attention-Gate und zustandsbehaftete Conv |
| `728771ce` | Liquid-Gewichte und Sharding |
| `865ab931` | Liquid-Rundung und KV-Strides |
| `efc33cf5` | AOT-Geometrie |
| `7063d0be` | Logitparität, Chunks, Graphs und Radix |
| `47334d40`, `c47175e2` | Damals blockierte Checkpoint-Zugriffe dokumentiert |
| `a2166909` | Erfolgreiche bf16-GPU-, HF- und Serving-Validierung |

## Geänderte Dateien

Teil 5 ändert `python/freetoken/models/lfm3/weight.py`,
`tests/models/lfm3/test_parity.py`, `docs/models.md`, `docs/lfm3.md` und diesen
Bericht. Die Validierung aus Teil 4 und Teil 5 ist in `docs/lfm3.md`
konsolidiert. Infrastruktur- und Modellnotizen bleiben als historische
Designnachweise erhalten.

Dateien der Teile 1-4 (aus `git diff --name-only f78731cf..a2166909`):

```text
docs/lfm3-infrastructure.md
docs/lfm3-model.md
docs/lfm3.md
python/freetoken/attention/linear.py
python/freetoken/engine/engine.py
python/freetoken/engine/forecast.py
python/freetoken/kernel/aot_models.py
python/freetoken/kernel/causal_conv1d.py
python/freetoken/kernel/triton/short_conv_triton.py
python/freetoken/kvcache/linear_state_pool.py
python/freetoken/models/__init__.py
python/freetoken/models/config.py
python/freetoken/models/lfm3/__init__.py
python/freetoken/models/lfm3/attention.py
python/freetoken/models/lfm3/config.py
python/freetoken/models/lfm3/conv.py
python/freetoken/models/lfm3/model.py
python/freetoken/models/lfm3/weight.py
python/freetoken/models/register.py
python/freetoken/server/args.py
tests/attention/test_capture_rows_per_req.py
tests/engine/test_attention_backend_matrix.py
tests/engine/test_forecast.py
tests/kernels/test_causal_conv1d_capture.py
tests/kvcache/test_linear_state_pool_alloc.py
tests/models/lfm3/__init__.py
tests/models/lfm3/common.py
tests/models/lfm3/conftest.py
tests/models/lfm3/lfm3_hf_ref.py
tests/models/lfm3/test_parity.py
tests/server/test_streaming_model_matrix.py
```

## Offene Punkte

- Variante B: echter SWA-Pool zusammen mit Hybrid-Radix, einschließlich
  Eviction, Snapshot-Wiederherstellung und eigenständiger Paritätsprüfung.
- Speculative Decoding einschließlich Verify/Replay bleibt explizit gesperrt.
- LFM3-VL, Omni und Audio sind nicht implementiert; nur das Textmodell.
- GGUF benötigt einen eigenen LFM3-Adapter und Parität; LFM2-Mapping genügt nicht.
- Base hat dieselbe unterstützte Architektur, wurde aber nicht selbst ausgeführt.
- Kein nativer NVFP4-W4A4-Hardwaretest, kein realer Multi-GPU-TP-Test und kein
  Nachweis für maximale 262144-Token-Kontexte; Serving hier auf 16384 begrenzt.
- Numerische Near-Ties, Thinking-Ausgaben trotz Template-Deaktivierung und
  die beobachtete NVFP4-Zwischenrechnung bleiben dokumentierte Grenzen.

## Abschlusssuite, Commit und Bereinigung

Der vollständige angeforderte Lauf (einschließlich `tests/kernels` und aller
17 LFM3-Fälle) ist grün: **3266 bestanden, 317 übersprungen, 10 abgewählt**,
13 Warnungen in **463.14 Sekunden**. Exakter Befehl und Umgebung stehen am
Ende von [lfm3.md](lfm3.md). Der Lauf enthält den erstmaligen GGML-CUDA-JIT-Bau;
C++-Quellen wurden nicht verändert. `git diff --check` ist erfolgreich.

Teil-5-Codecommit: **`44fc2665`**, `fix(lfm3): translate fp8 and nvfp4 checkpoint scales`.
Die abschließende Dokumentation folgt als eigener Commit
`docs(lfm3): document quantized validation and completion report`.
Beide tragen `Assisted-by: Claude Opus 5.5`; Autor ist der konfigurierte
Git-Nutzer KarrAcaRn. Kein Push oder Merge wurde ausgeführt.

Alle eigenen Server wurden über ihre aufgezeichneten PIDs beendet; pytest
ist beendet. `~/.cache/ft-pytest/lfm3` ist entfernt. Die abschließende Abfrage
`nvidia-smi --query-compute-apps=pid --format=csv,noheader` zeigt weiterhin
**235776** (GNOME Remote Desktop) und **236743** (Ptyxis), beide bereits vor
Taskbeginn vorhanden. Es läuft **kein eigener GPU-Prozess** mehr. Die
wörtliche Forderung einer global leeren Liste ist damit nicht erfüllt;
fremde Desktop-Sitzungen wurden nicht beendet.
