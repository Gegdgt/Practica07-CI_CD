"""Verifica resultados, casos borde, Unicode y validación estricta de tipos."""

import pytest

from text_utils import concat, count_vowels, is_palindrome, reverse, to_upper


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        pytest.param("hola", "aloh", id="palabra"),
        pytest.param("Python!", "!nohtyP", id="mayuscula-y-puntuacion"),
        pytest.param("", "", id="cadena-vacia"),
        pytest.param("áéñ", "ñéá", id="acentos"),
        pytest.param("a🙂b", "b🙂a", id="emoji"),
        pytest.param("a\u0301b", "b\u0301a", id="puntos-de-codigo-combinados"),
    ],
)
def test_reverse_invierte_puntos_de_codigo(texto: str, esperado: str) -> None:
    """La inversión mantiene todos los puntos de código en orden inverso."""
    assert reverse(texto) == esperado


@pytest.mark.parametrize("valor", [None, 123, ["hola"], b"hola"])
def test_reverse_rechaza_tipos_invalidos(valor: object) -> None:
    """La inversión no convierte otros tipos a texto silenciosamente."""
    with pytest.raises(TypeError):
        reverse(valor)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        pytest.param("casa", 2, id="palabra"),
        pytest.param("Murciélago", 5, id="mayusculas-y-acento"),
        pytest.param("ÁÉÍÓÚÜáéíóúü", 12, id="vocales-acentuadas-y-dieresis"),
        pytest.param("bcd 123!? ñ", 0, id="sin-vocales"),
        pytest.param("", 0, id="cadena-vacia"),
        pytest.param("e\u0301u\u0308", 2, id="acentos-combinados"),
        pytest.param("aeiou", 5, id="todas-las-vocales"),
        pytest.param("pingüino y ÑANDÚ", 6, id="mezcla-de-casos-y-dieresis"),
    ],
)
def test_count_vowels_cuenta_vocales_unicode(texto: str, esperado: int) -> None:
    """Cada vocal cuenta una vez, incluso con marcas Unicode combinadas."""
    assert count_vowels(texto) == esperado


@pytest.mark.parametrize("valor", [None, 123, ["a"], b"aeiou"])
def test_count_vowels_rechaza_tipos_invalidos(valor: object) -> None:
    """El contador exige una cadena como entrada."""
    with pytest.raises(TypeError):
        count_vowels(valor)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        pytest.param("reconocer", True, id="palabra-palindroma"),
        pytest.param("Ana", True, id="ignora-mayusculas"),
        pytest.param("Anita lava la tina", True, id="ignora-espacios"),
        pytest.param("¡Anita, lava la tina!", True, id="ignora-puntuacion"),
        pytest.param("ÁnÁ", True, id="acentos-simetricos"),
        pytest.param("aÁ", False, id="conserva-los-acentos"),
        pytest.param("nñ", False, id="enie-distinta-de-ene"),
        pytest.param("á x a\u0301", True, id="equivalencia-canonica-unicode"),
        pytest.param("", True, id="cadena-vacia"),
        pytest.param("!? 🙂 —", True, id="solo-puntuacion-y-simbolos"),
        pytest.param("Python", False, id="palabra-no-palindroma"),
        pytest.param("12,321", True, id="conserva-digitos"),
    ],
)
def test_is_palindrome_normaliza_sin_eliminar_acentos(
    texto: str, esperado: bool
) -> None:
    """Compara caracteres alfanuméricos con equivalencia Unicode canónica."""
    assert is_palindrome(texto) is esperado


@pytest.mark.parametrize("valor", [None, 121, ["a", "a"], b"ana"])
def test_is_palindrome_rechaza_tipos_invalidos(valor: object) -> None:
    """Los números y secuencias no se reinterpretan como cadenas."""
    with pytest.raises(TypeError):
        is_palindrome(valor)


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        pytest.param("hola", "HOLA", id="minusculas"),
        pytest.param("HoLa Mundo", "HOLA MUNDO", id="mezcla-de-casos"),
        pytest.param("", "", id="cadena-vacia"),
        pytest.param("áéíóúüñ", "ÁÉÍÓÚÜÑ", id="acentos-dieresis-y-enie"),
        pytest.param("¡Hola! 123 🙂\n", "¡HOLA! 123 🙂\n", id="simbolos-y-salto"),
        pytest.param("straße", "STRASSE", id="expansion-unicode"),
    ],
)
def test_to_upper_respeta_conversion_unicode(texto: str, esperado: str) -> None:
    """Convierte letras y preserva los caracteres sin variante mayúscula."""
    assert to_upper(texto) == esperado


@pytest.mark.parametrize("valor", [None, 123, ["hola"], b"hola"])
def test_to_upper_rechaza_tipos_invalidos(valor: object) -> None:
    """La conversión a mayúsculas requiere texto, no otros tipos."""
    with pytest.raises(TypeError):
        to_upper(valor)


@pytest.mark.parametrize(
    ("primero", "segundo", "esperado"),
    [
        pytest.param("Hola", " mundo", "Hola mundo", id="espacio-existente"),
        pytest.param("a", "b", "ab", id="sin-separador"),
        pytest.param("", "", "", id="ambas-vacias"),
        pytest.param("", "hola", "hola", id="primera-vacia"),
        pytest.param("hola", "", "hola", id="segunda-vacia"),
        pytest.param("áñ", "Ü", "áñÜ", id="unicode-y-mayusculas"),
        pytest.param("🙂", "!", "🙂!", id="emoji-y-puntuacion"),
        pytest.param("a ", "\tb", "a \tb", id="conserva-espacios-y-tabulacion"),
    ],
)
def test_concat_une_exactamente_las_cadenas(
    primero: str, segundo: str, esperado: str
) -> None:
    """La concatenación no agrega separadores ni elimina espacios."""
    assert concat(primero, segundo) == esperado


@pytest.mark.parametrize(
    ("primero", "segundo"),
    [
        pytest.param(None, "b", id="primero-none"),
        pytest.param(1, "b", id="primero-entero"),
        pytest.param([], "b", id="primero-lista"),
        pytest.param(True, "b", id="primero-booleano"),
        pytest.param("a", None, id="segundo-none"),
        pytest.param("a", 1, id="segundo-entero"),
        pytest.param("a", [], id="segundo-lista"),
        pytest.param(None, False, id="ambos-invalidos"),
    ],
)
def test_concat_rechaza_cualquier_argumento_invalido(
    primero: object, segundo: object
) -> None:
    """Ambos argumentos deben ser cadenas, incluidos los valores falsy."""
    with pytest.raises(TypeError):
        concat(primero, segundo)
