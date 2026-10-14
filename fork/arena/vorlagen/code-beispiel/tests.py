from solution import ist_palindrom


def test_einfach():
    assert ist_palindrom("Anna")


def test_satz():
    assert ist_palindrom("Eine güldne, gute Tugend: Lüge nie!") is True


def test_kein_palindrom():
    assert not ist_palindrom("Hallo")


def test_leer():
    assert ist_palindrom("")


def test_umlaute():
    assert ist_palindrom("Ä, ä!") and not ist_palindrom("Äa")
