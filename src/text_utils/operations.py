"""Funciones puras para manipular cadenas Unicode."""

import unicodedata


def _require_string(value: object, parameter: str) -> None:
    """Rechaza entradas que no sean cadenas, sin convertirlas implícitamente."""
    if not isinstance(value, str):
        raise TypeError(f"{parameter} debe ser una cadena (str)")


def reverse(s: str) -> str:
    """Invierte los puntos de código de s; una cadena vacía sigue vacía.

    No agrupa grafemas: una marca combinada se invierte como un carácter más.
    Lanza TypeError si s no es str.
    """
    _require_string(s, "s")
    return s[::-1]


def count_vowels(s: str) -> int:
    """Cuenta vocales a/e/i/o/u y variantes con marcas diacríticas.

    La descomposición NFD permite contar á, à, â, ä, ü y sus equivalentes
    combinados; casefold permite ignorar mayúsculas. Lanza TypeError para no str.
    """
    _require_string(s, "s")
    normalized = unicodedata.normalize("NFD", s.casefold())
    return sum(character in "aeiou" for character in normalized)


def is_palindrome(s: str) -> bool:
    """Indica si s es palíndroma, ignorando mayúsculas y no alfanuméricos.

    Conserva letras acentuadas compuestas: a y á difieren, al igual que n y ñ.
    Las marcas combinadas que NFC no puede componer se ignoran. NFC trata
    representaciones Unicode canónicamente equivalentes como iguales. Ignora
    espacios, puntuación y símbolos; vacío o solo puntuación devuelve True.
    Lanza TypeError si s no es str.
    """
    _require_string(s, "s")
    normalized = unicodedata.normalize("NFC", s)
    normalized = unicodedata.normalize("NFC", normalized.casefold())
    characters = "".join(character for character in normalized if character.isalnum())
    return characters == characters[::-1]


def to_upper(s: str) -> str:
    """Convierte s a mayúsculas Unicode (por ejemplo, ß se expande a SS).

    Conserva puntuación y símbolos; lanza TypeError si s no es str.
    """
    _require_string(s, "s")
    return s.upper()


def concat(a: str, b: str) -> str:
    """Concatena exactamente dos cadenas, sin añadir espacios ni separadores.

    Lanza TypeError si cualquiera de los argumentos no es str.
    """
    _require_string(a, "a")
    _require_string(b, "b")
    return a + b
