# qwen3-30b-a3b - delphi-result-init (2026-10-17T19:21:08)

## Antwort (4166 Tokens, 15.166 s, Ende: stop)

### Denkphase


Okay, I need to figure out what's wrong with this Delphi function. Let me start by looking at the code provided.

The function is called CreateStringFromStringlist and takes a TStringList and an optional separator, defaulting to #13#10 (which is a carriage return and line feed, so a line break). The goal seems to be to concatenate all the strings in the StringList with the specified separator. 

The code uses a for loop: for s in aStringList do Result := ConcatStrings(Result, s, aSeperator); 

Wait, in Delphi, when you loop through a TStringList using for...in, it iterates over each string in the list. But the problem here is that the function is supposed to return a single string, but the loop is assigning to Result each time. However, the ConcatStrings function is being used here. Let me recall what ConcatStrings does. 

From what I remember, ConcatStrings is a function in the SysUtils unit that takes a list of strings and concatenates them. But the parameters here are Result, s, and aSeperator. Wait, the function signature of ConcatStrings is usually something like ConcatStrings(const Strings: array of string) or maybe it's a different function. Wait, maybe I'm confusing it with something else. Let me check.

Actually, in Delphi, there's a function called ConcatStrings which is in the System.SysUtils unit. Its declaration is:

function ConcatStrings(const Separator: string; const Strings: array of string): string;

So it takes a separator and an array of strings, and returns the concatenated result. But in the code given, the function is using ConcatStrings(Result, s, aSeperator). Wait, that would mean the first parameter is Result, which is a string, then s, which is a string, and aSeperator, which is the separator. But that doesn't match the function's parameters. The correct usage should be ConcatStrings(Separator, [s1, s2, s3...]).

Wait, the code is using ConcatStrings(Result, s, aSeperator). That would be passing the first parameter as Result (a string), then s (another string), and then aSeperator (a string). But according to the function's parameters, the first is the separator, then the array of strings. So the code is using the function incorrectly. 

Wait, but maybe the user is using a different function? Or perhaps there's a misunderstanding here. Because the way it's written, the parameters are in the wrong order. So the code is trying to call ConcatStrings with the first parameter as Result, which is a string, but the function expects the first parameter to be the separator. So this is a mistake. 

Another thing: the function is using a for loop to iterate through the StringList, but in Delphi, when you loop through a TStringList with for...in, it's not the same as looping through an array. So the loop is getting each string in the list, but then using ConcatStrings which expects an array of strings. However, the code is passing Result (which is initially empty) and then s and aSeperator. That doesn't make sense. 

Wait, maybe the intention was to use the + operator or something else. Because if you just do Result := Result + s + aSeperator, that would concatenate each string with the separator. But the code is using ConcatStrings, which is not the right approach here. 

Alternatively, maybe the user intended to use the Concat function, but that's not the case. Let me think: the original code is using ConcatStrings, which is for concatenating an array of strings with a separator. But in the loop, each iteration is passing Result (which is a string) as the first parameter, then s (a single string), and aSeperator. That would be incorrect because the function expects the separator as the first parameter and the array of strings as the second. 

So the code is using the function in the wrong way. Instead of using ConcatStrings, the user might have intended to use a loop that appends each string with the separator. But the way it's written, the parameters are mixed up. 

Another possible issue is that the initial value of Result is not set. In Delphi, the function's Result variable is initialized to an empty string. So the first iteration would take Result (empty) and s, and then add aSeperator. But that's not correct. Because if you have multiple strings, each time you add a separator, you end up with extra separators at the end. For example, if the list has two strings, "a" and "b", the code would do:

Result starts as empty. First iteration: ConcatStrings(Result, s, aSeperator) would be ConcatStrings('', 'a', #13#10). But the ConcatStrings function's first parameter is the separator, and the second is the array. So the code is passing the separator as the first parameter, but in the code, the first parameter is Result, which is a string. So the parameters are swapped. 

Wait, no. The user's code is using ConcatStrings(Result, s, aSeperator). But according to the function's parameters, the first is the separator, the second is the array. So the code is passing the separator as the first parameter, but in the code, it's passing Result (which is the function's result variable) as the first parameter, which is wrong. 

So the correct way would be to call ConcatStrings with the separator as the first parameter and the array of strings as the second. But in the code, the loop is trying to use ConcatStrings in a way that's not matching. 

Alternatively, maybe the user is trying to use a different function, or there's a misunderstanding. 

Another problem is that the loop is using a for...in loop on aStringList, which is a TStringList. But in Delphi, the for...in loop for a TStringList would iterate over the strings in the list. So for each string s in aStringList, it's trying to concatenate it with the separator. But the way ConcatStrings is being used is incorrect. 

Wait, perhaps the user intended to use the Concat function, which is in the SysUtils unit. But Concat is for concatenating two strings. However, in the code, it's using ConcatStrings, which is for concatenating an array of strings. 

So the code is trying to use ConcatStrings in a loop, but the parameters are incorrect. The correct approach would be to collect all the strings from the StringList into an array, then call ConcatStrings with the separator and the array. 

Alternatively, if the user is using a loop, they might be trying to build the result string by appending each element with the separator. But the code is using ConcatStrings in a way that's not correct. 

Let me think of an example. Suppose aStringList has three elements: 'a', 'b', 'c'. The default separator is #13#10. The function is supposed to return 'a' + #13#10 + 'b' + #13#10 + 'c'. But the code is using ConcatStrings(Result, s, aSeperator). Let's see what that does. 

If ConcatStrings is called with the first parameter as Result (which is initially empty), the second parameter as s (the first string), and the third as aSeperator. Wait, but the function's parameters are (Separator: string; Strings: array of string). So the code is passing the first parameter as the result (which is the accumulated string), then s (a single string), and then aSeperator. That's not correct. 

Wait, maybe the user confused the parameters. The correct call would be ConcatStrings(aSeperator, [s1, s2, s3...]). But in the loop, they are passing Result as the first parameter, which is not the separator. 

So the code is using ConcatStrings incorrectly. The parameters are swapped. Instead of passing the separator first, they're passing the accumulated result as the first parameter, which is wrong. 

Another possible issue is that the function is not initializing the Result. Because in the loop, the first iteration would take the initial empty Result and concatenate it with s and aSeperator. But ConcatStrings expects the second parameter to be an array of strings. So the code is passing a single string (s) instead of an array. 

Wait, but the way the code is written, the loop is for s in aStringList do Result := ConcatStrings(Result, s, aSeperator); So each time, it's taking the current Result, then passing it as the first parameter to ConcatStrings, along with s and aSeperator. But ConcatStrings is supposed to take the separator as the first parameter and the array of strings as the second. So the code is using the function in the wrong order. 

So the first mistake is the parameters of ConcatStrings are in the wrong order. Instead of ConcatStrings(Separator, Strings), the code is passing Result as the first parameter, which is the accumulated string, and then s and aSeperator. That's not correct. 

Another problem is that ConcatStrings is not designed to be used in a loop like this. Because ConcatStrings takes an array of strings. So if you have a loop where you're adding one string at a time, you need to collect all the strings into an array first. 

Alternatively, the user might have intended to use the + operator to concatenate each string with the separator. But the code is using ConcatStrings, which is not the right approach. 

So the function is not working as intended because of incorrect usage of ConcatStrings. Also, the loop is not building the result properly. Because each time, it's using ConcatStrings with the current Result, s, and aSeperator, but the function is designed to take a separator and an array of strings, not to append a single string. 

Wait, let me check the actual implementation of ConcatStrings. Suppose the function is defined as:

function ConcatStrings(const Separator: string; const Strings: array of string): string;

Then, if you call it with Separator = aSeperator, and Strings as an array containing s. But in the code, the user is passing Result as the first parameter, which is a string, then s, then aSeperator. So the parameters are in the wrong order. 

So the correct code would be to collect all the strings from aStringList into an array, then call ConcatStrings with the separator and the array. But the current code is trying to do that in a loop, which is not the right approach. 

Another possible mistake is that the function is not handling the separator correctly. For example, if the list is empty, the function would return an empty string, which is correct. But when there are elements, the code is using ConcatStrings in a way that's not appropriate. 

So the main issues are:

1. The parameters to ConcatStrings are in the wrong order. The first parameter should be the separator, but the code is passing Result (which is a string) as the first parameter, and then s and aSeperator as the other parameters. That's not matching the function's signature.

2. The loop is not correctly accumulating the strings. Because ConcatStrings is not designed to be used in a loop like that. It's meant to take an array of strings and a separator. So using it in a loop would not work as intended.

So the correct way would be to collect all the strings from the StringList into an array, then call ConcatStrings with the separator and the array. Alternatively, use a loop that builds the result by adding each string with the separator, but that's not using ConcatStrings correctly.

Another possible mistake: the function is named CreateStringFromStringlist, but the code is using ConcatStrings. Maybe the user intended to create a single string by joining the elements of the StringList with the separator. So the correct approach would be to collect the strings into an array, then call ConcatStrings with the separator and the array.

But in the current code, the loop is trying to use ConcatStrings in a way that's not correct. So the function is not working as intended.

Additionally, the function is declared with aSeperator as a default parameter. But in the code, the separator is being passed as the third parameter to ConcatStrings, which is not correct.

So the user's code is trying to use ConcatStrings in a loop, but the parameters are not properly set. The function is not designed for that. So the code is incorrect.

Another thing: in Delphi, the for s in aStringList loop would iterate over each string in the list. So for each s, the code is doing Result := ConcatStrings(Result, s, aSeperator). But ConcatStrings is not a function that appends a single string. It's supposed to take an array of strings. So if you pass a single string, it's not correct. 

Wait, but maybe the user is using a different function. For example, maybe they have a custom ConcatStrings function. But according to standard Delphi, ConcatStrings is as I mentioned. So the code is using the standard function incorrectly.

So the function's code is flawed because it's using ConcatStrings with the wrong parameters. The correct approach would be to collect all the strings from the StringList into an array, then call ConcatStrings with the separator and the array. 

Alternatively, if the user intended to use a loop to build the result, they should use something like:

Result := '';
for s in aStringList do
  Result := Result + s + aSeperator;

But that would add the separator after each string, leading to an extra separator at the end. So maybe they should handle that case.

But the original code is using ConcatStrings in a loop, which is not the correct usage. So the function is not working as expected. The main error is the incorrect parameters passed to ConcatStrings.

Another possible error is that the function is not initializing Result. But in Delphi, the Result variable is initialized to an empty string, so that's not a problem. However, the way it's using ConcatStrings is wrong.

So the conclusion is that the code is using the ConcatStrings function incorrectly. The parameters are swapped. The first parameter should be the separator, but the code is passing the accumulated result (which is a string) as the first parameter. The second parameter should be an array of strings, but the code is passing a single string (s) and then the separator as the third parameter. 

Therefore, the correct code would be to collect all the strings into an array and then call ConcatStrings once. For example:

function CreateStringFromStringlist(aStringList: TStringList; aSeperator: String = #13#10): String;
var
  Strings: array of string;
  i: Integer;
begin
  SetLength(Strings, aStringList.Count);
  for i := 0 to aStringList.Count - 1 do
    Strings[i] := aStringList[i];
  Result := ConcatStrings(aSeperator, Strings);
end;

But the original code is using a loop with ConcatStrings in a way that's not correct. So the main issue is the misuse of the ConcatStrings function with incorrect parameters.


### Antwort



Die Funktion `CreateStringFromStringlist` enthält mehrere Fehler, die die korrekte Funktionalität verhindern:

### **1. Falsche Parameterreihenfolge bei `ConcatStrings`**
Die Funktion `ConcatStrings` (aus `SysUtils`) hat die Signatur:
```delphi
function ConcatStrings(const Separator: string; const Strings: array of string): string;
```
Sie erwartet **zuerst den Trennzeichen-String** und **dann ein Array von Zeichenketten**.  
In der gegebenen Funktion wird jedoch:
```delphi
ConcatStrings(Result, s, aSeperator)
```
aufgerufen, wobei `Result` (ein String) als erster Parameter und `s` (ein einzelner String) als zweiter übergeben wird. Dies ist **nicht kompatibel** mit der erwarteten Signatur der Funktion.

### **2. Falsche Verwendung von `ConcatStrings` in einer Schleife**
`ConcatStrings` ist nicht dafür konzipiert, in einer Schleife verwendet zu werden, um Zeichenketten schrittweise zu verketten. Es ist eine **Einzelaufruf-Funktion**, die ein Array von Strings mit einem Trennzeichen verknüpft.  
Die Schleife `for s in aStringList do Result := ConcatStrings(Result, s, aSeperator)` ist **nicht logisch**, da `ConcatStrings` nicht mit einem einzelnen String arbeitet, sondern ein Array von Strings erwartet.

### **3. Überflüssige Trennzeichen am Ende**
Wenn man `ConcatStrings` falsch verwendet, z. B. mit `Result` als ersten Parameter, dann wird die Verkettung nicht korrekt durchgeführt. Zudem würde eine Schleife, die `Result + s + aSeperator` durchführt, ein **überflüssiges Trennzeichen am Ende** der Ergebniszeichenkette erzeugen (z. B. "a\nb\nc\n" bei drei Elementen).

---

### **Korrekte Implementierung**
Um die Zeichenketten aus einem `TStringList` mit einem Trennzeichen zu verknüpfen, ist eine andere Herangehensweise notwendig. Hier ist ein **korrekter Code**:

```delphi
function CreateStringFromStringlist(aStringList: TStringList; aSeparator: String = #13#10): String;
var
  i: Integer;
begin
  Result := '';
  for i := 0 to aStringList.Count - 1 do
  begin
    if i > 0 then
      Result := Result + aSeparator;
    Result := Result + aStringList[i];
  end;
end;
```

### **Erklärung:**
- **Initialisierung**: `Result` wird mit leerem String begonnen.
- **Schleife**: Jeder String aus `aStringList` wird mit dem Trennzeichen verknüpft, **außer der erste**.
- **Ergebnis**: "a\nb\nc" (ohne überflüssiges Trennzeichen am Ende).

---

### **Alternativ: Verwendung von `StringList.Text`**
Wenn das Ziel ist, die Zeichenketten mit einem Trennzeichen zu kombinieren, kann man auch direkt `aStringList.Text` verwenden. Dieser String enthält alle Elemente des `TStringList`, getrennt durch `\r\n` (standardmäßig).  
Für andere Trennzeichen:
```delphi
function CreateStringFromStringlist(aStringList: TStringList; aSeparator: String = #13#10): String;
begin
  Result := aStringList.Text;
  if aSeparator <> #13#10 then
    Result := StringReplace(Result, #13#10, aSeparator, [rfReplaceAll]);
end;
```

---

### **Zusammenfassung der Fehler**
1. **Falsche Parameterreihenfolge** in `ConcatStrings`.
2. **Falsche Verwendung** von `ConcatStrings` in einer Schleife (wird nicht für iterative Verkettung genutzt).
3. **Überflüssiges Trennzeichen am Ende**, wenn `ConcatStrings` nicht korrekt genutzt wird.

Die Funktion sollte stattdessen die Strings direkt mit einem Schleifen-Algorithmus verknüpfen oder `aStringList.Text` verwenden.

## Nachfrage (2653 Tokens, 9.753 s, Ende: stop)

### Denkphase


Okay, let me try to figure out why the original function is wrong and what happens internally in Delphi. The user provided the function:

function CreateStringFromStringlist(aStringList :TStringList; aSeperator : String = #13#10) : String;
var
  s : String;
begin
  for s in aStringList
    do Result := ConcatStrings(Result, s, aSeperator);
end;

First, I remember that ConcatStrings is a function from SysUtils. Let me check its parameters. The correct signature is function ConcatStrings(const Separator: string; const Strings: array of string): string;. So it takes a separator first, then an array of strings. But in the code, they're using it as ConcatStrings(Result, s, aSeperator). That would mean the first parameter is Result (a string), the second is s (a string), and the third is aSeperator (a string). Wait, but the function expects the second parameter to be an array of strings. So passing a single string instead of an array is incorrect.

So the first mistake is that the user is passing three parameters where the function expects two. The function ConcatStrings is designed to take a separator and an array of strings. But here, they're using a loop where each iteration takes one string and tries to concatenate it with the previous result and the separator. That's not how ConcatStrings works. It's not meant for iterative appending; it's for concatenating an entire array at once.

Another issue is that in Delphi, when you use a for...in loop on a TStringList, it iterates over the strings in the list. But the loop variable 's' is a String, so each iteration gets one string from the list. However, the code is trying to use ConcatStrings in a way that's not appropriate. The ConcatStrings function would expect the second parameter to be an array, but here they're passing a single string. So the parameters are mismatched.

Wait, but in Delphi, when you pass a single string where an array is expected, does it automatically convert it? Or is that a compiler error? I think that would be a compiler error because the function expects an array of strings as the second parameter, but the code is passing a single string. So the line "ConcatStrings(Result, s, aSeperator)" would be invalid because the second parameter is not an array.

But maybe the user tried to use ConcatStrings in a different way. Let me think. If they mistakenly thought that ConcatStrings can take a string and another string to append, that's not the case. The function is for joining multiple strings with a separator. So if you have an array of strings, it joins them with the separator. But here, they're trying to use it in a loop, which is not the intended use.

Another problem is that in the loop, they're using Result as the first parameter. So the first time, Result is empty (since it's a function variable, initialized to empty string). Then ConcatStrings is called with Result (empty), s (first string), and aSeperator. But ConcatStrings expects the second parameter to be an array. So passing a single string instead of an array would cause a compiler error.

Wait, but in Delphi, when you pass a single string where an array is expected, it's not allowed. So the code as written would not compile. The user might have intended to use something like Join, but ConcatStrings isn't the right function for that. Maybe they confused ConcatStrings with a function that appends a string to another, but that's not what it does.

So the main issues are the incorrect parameters to ConcatStrings and the fact that the loop is trying to use it in a way that's not intended. The function is being called with three parameters, but it only takes two. That's a clear syntax error.

Additionally, even if they tried to use ConcatStrings correctly, the loop approach is not suitable. Because ConcatStrings is for joining multiple strings at once, not for building up a string step by step. So the original code is not just incorrect in parameters but also in logic.

So the user's code would not compile because of the parameter mismatch. The function ConcatStrings requires the second parameter to be an array of strings, but in the loop, they're passing a single string each time. Therefore, the code is invalid and would result in a compiler error.


### Antwort



Die Funktion `CreateStringFromStringlist` enthält **mehrfach Fehler**, die zu **Kompilierungsfehlern** oder **falschem Verhalten** führen. Hier ist eine detaillierte Erklärung, was in Delphi intern passiert und warum der Code nicht funktioniert:

---

### **1. Falsche Parameterreihenfolge und -typen bei `ConcatStrings`**
Die Funktion `ConcatStrings` (aus `SysUtils`) hat die folgende Signatur:
```delphi
function ConcatStrings(const Separator: string; const Strings: array of string): string;
```
- **Erster Parameter**: Ein Trennzeichen (`Separator`).
- **Zweiter Parameter**: Ein **Array** von Zeichenketten (`Strings`).

**Fehler im Code**:  
Die Zeile  
```delphi
Result := ConcatStrings(Result, s, aSeperator);
```  
übermittelt **drei Parameter**, obwohl `ConcatStrings` **nur zwei Parameter** erwartet.  
- `Result` ist ein `String` (erster Parameter, korrekt).
- `s` ist ein `String` (zweiter Parameter, **falsch**, da `ConcatStrings` einen **Array** erwartet).
- `aSeperator` ist ein `String` (dritter Parameter, **nicht vorhanden**, da `ConcatStrings` nur zwei Parameter akzeptiert).

**Internes Verhalten**:  
Delphi erwartet, dass der zweite Parameter ein **Array** ist. Wenn stattdessen ein einzelner String übergeben wird, führt das zu einem **Kompilierungsfehler**, da die Typen nicht übereinstimmen. Der Compiler meldet z. B.:
```
E2010 Incompatible types: 'String' and 'array of string'
```

---

### **2. Falsche Logik: `ConcatStrings` ist nicht für iterative Verkettung gedacht**
`ConcatStrings` ist **nicht für Schleifen** konzipiert. Sie ist dafür gedacht, **mehrere Strings in einem einzigen Aufruf** mit einem Trennzeichen zu verknüpfen.  
Beispiel:
```delphi
ConcatStrings(', ', ['a', 'b', 'c']); // Liefert "a, b, c"
```

**Probleme im Code**:
- Die Schleife iteriert über jeden String in `aStringList`, aber `ConcatStrings` wird **jeweils mit einem einzelnen String** aufgerufen. Das ist **nicht möglich**, da `ConcatStrings` ein Array erwartet.
- Die Logik `Result := ConcatStrings(Result, s, aSeperator)` ist **verkehrt**, da `ConcatStrings` **keinen String** mit einem anderen String verknüpfen kann, sondern nur **mehrere Strings in einem Array**.

**Internes Verhalten**:  
Wenn der Code kompiliert wird (was er nicht tut), würde `ConcatStrings` versuchen, den `Result`-String als **Array** zu interpretieren. Da `Result` ein `String` ist und kein Array, führt das zu einem **Typenfehler**.

---

### **3. Falsche Verwendung von `for s in aStringList`**
In Delphi ist die Syntax `for s in aStringList` **nicht direkt möglich**. `TStringList` ist **kein iterierbares Array** im Sinne von `for...in`.  
Um `TStringList` mit `for...in` zu durchlaufen, müsste man `aStringList.Strings` verwenden, z. B.:
```delphi
for s in aStringList.Strings do
```
Aber selbst dann wäre die Logik **falsch**, da `ConcatStrings` nicht für Schleifen gedacht ist.

**Internes Verhalten**:  
Delphi erlaubt `for...in` nur für Typen, die die `IEnumerator`-Schnittstelle implementieren (z. B. `TStringList` ist **kein Enumerator**). Ohne `Strings`-Eigenschaft oder eine explizite Schleife über `Count` und `Strings[i]` ist der Code **nicht kompilierbar**.

---

### **4. Fehlende Initialisierung von `Result`**
`Result` ist ein `String`, der standardmäßig auf `''` (leerer String) initialisiert wird.  
Allerdings wird in der Schleife `Result` in jedem Iterationsschritt mit `ConcatStrings` überschrieben. Da `ConcatStrings` aber nicht für diesen Zweck gedacht ist, ist das Ergebnis **nicht vorhersehbar**.

---

### **5. Überflüssiges Trennzeichen am Ende**
Selbst wenn der Code kompiliert würde (z. B. mit einem falschen `ConcatStrings`), würde das **überflüssige Trennzeichen** am Ende der Zeichenkette entstehen.  
Beispiel:  
Bei `aStringList` mit `[ 'a', 'b', 'c' ]` und `aSeperator = #13#10` würde der Code:
```
Result = 'a' + #13#10 + 'b' + #13#10 + 'c' + #13#10
```
Erzeugt also `"a\r\nb\r\nc\r\n"` (mit einem Trennzeichen am Ende), was nicht gewünscht ist.

---

### **Zusammenfassung der Fehler**
| Fehler | Erklärung |
|--------|-----------|
| **Parameterfehler** | `ConcatStrings` erwartet ein Array als zweiten Parameter, nicht einen einzelnen String. |
| **Kompilierungsfehler** | `for s in aStringList` ist nicht zulässig, da `TStringList` kein Enumerator ist. |
| **Logikfehler** | `ConcatStrings` ist nicht für Schleifen gedacht. Es wird falsch verwendet. |
| **Überflüssiges Trennzeichen** | Der Code fügt ein Trennzeichen nach jedem Element hinzu, auch nach dem letzten. |

---

### **Korrekte Alternative**
Um die Zeichenketten aus einem `TStringList` mit einem Trennzeichen zu verknüpfen, sollte man stattdessen eine Schleife mit `Strings[i]` und explizitem Trennzeichen verwenden:
```delphi
function CreateStringFromStringlist(aStringList: TStringList; aSeparator: String = #13#10): String;
var
  i: Integer;
begin
  Result := '';
  for i := 0 to aStringList.Count - 1 do
  begin
    if i > 0 then
      Result := Result + aSeparator;
    Result := Result + aStringList[i];
  end;
end;
```

**Erklärung**:
- `aStringList.Count` gibt die Anzahl der Elemente zurück.
- `if i > 0` verhindert, dass das Trennzeichen vor dem ersten Element hinzugefügt wird.
- `Result + aStringList[i]` fügt jedes Element direkt an den String an.

---

### **Zusammenfassung**
Die ursprüngliche Funktion ist **nicht kompilierbar**, da:
1. `ConcatStrings` mit falschen Parametern aufgerufen wird.
2. `for s in aStringList` nicht für `TStringList` funktioniert.
3. Das Trennzeichen nach jedem Element hinzugefügt wird, was zu einem **überflüssigen Trennzeichen am Ende** führt.

Die korrekte Implementierung verwendet eine **explizite Schleife** mit `Strings[i]` und fügt das Trennzeichen **nur zwischen den Elementen** hinzu.
