**CreateStringFromStringlist**
- Der Rückgabewert wird nie gesetzt: `Antwort` wird zusammengebaut, aber nicht `Result` zugewiesen. Es fehlt
  `Result := Antwort;`. Weil `Result` bei Strings ein versteckter var-Parameter des Aufrufers ist und nicht mit `''`
  initialisiert wird, liefert die Funktion den alten Inhalt der Zielvariable des Aufrufers zurück.
- Kleinigkeiten: Tippfehler `aSeperator`, `aStringList` sollte `const` sein. (`Antwort` selbst ist als lokaler String
  mit `''` initialisiert.)

**CountLinesWithOccurences**
- Speicherleck: Die von `CreateStringListFromString` erzeugte `TStringList` wird nie freigegeben. Richtig wäre
  `try ... finally SL.Free; end;`.
