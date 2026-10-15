`Result` wird vor der Schleife nicht mit `''` initialisiert. Bei Strings ist `Result` ein versteckter var-Parameter
des Aufrufers und enthält dessen bisherigen Wert. `ConcatStrings(Result, ...)` hängt die Einträge deshalb an den
alten Inhalt der Zielvariable an: Aus `str := 'Hallo'; str := CreateStringFromStringlist(sl, '<>');` wird
`'Hallo<>TestA<>TestB'` statt `'TestA<>TestB'`. Lösung: `Result := '';` vor der Schleife.
