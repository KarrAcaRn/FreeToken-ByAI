```python
def ist_palindrom(text: str) -> bool:
    s = [c for c in text.casefold() if c.isalnum()]
    return s == s[::-1]
```
