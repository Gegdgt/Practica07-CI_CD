# Taller: construir y demostrar la librería de texto

Esta guía explica cómo reconstruir la librería, por qué se eligió cada algoritmo
y cómo demostrar que las pruebas detectan una modificación incorrecta. El
recorrido comienza con funciones pequeñas y termina con la misma validación
ejecutada por integración continua.

La instalación completa está en el [README](../README.md). La configuración de
automatización está en [GITHUB.md](GITHUB.md), y el análisis de resultados y
soluciones técnicas está en [EVIDENCIAS.md](EVIDENCIAS.md).

## 1. Preparar la estructura y el paquete

Crear una carpeta de proyecto con esta organización:

```text
Practica07-CI_CD/
├── .github/workflows/ci.yml
├── src/text_utils/
│   ├── __init__.py
│   └── operations.py
├── tests/
│   ├── __init__.py
│   └── test_operations.py
├── docs/
│   ├── DEMO.md
│   ├── EVIDENCIAS.md
│   └── GITHUB.md
├── .gitattributes
├── .gitignore
├── pyproject.toml
└── README.md
```

`operations.py` contiene la lógica; `__init__.py` expone la API pública;
`test_operations.py` describe los resultados que esa API debe cumplir. El
archivo `tests/__init__.py` puede estar vacío. Crear un `README.md` con la
descripción del proyecto y escribir esta configuración en `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "practica07-text-utils"
version = "0.1.0"
description = "Librería de texto para la práctica de integración continua CC3047"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest==8.4.2"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--strict-markers"
```

El directorio `src` separa el código del paquete de las pruebas. Se instala el
paquete antes de importarlo, lo que también permite detectar problemas de
empaquetado. `setuptools` construye el paquete y pytest es la dependencia de
desarrollo; no hay dependencias de ejecución. `unicodedata`, utilizado más
adelante, forma parte de la biblioteca estándar de Python.

Usar Python 3.12 para reproducir el entorno de la práctica. Después de guardar
la implementación de los siguientes pasos, instalar desde la raíz en PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
```

El modo editable permite probar cambios en `src` sin reinstalar tras cada
edición. Para recrear las exclusiones de entornos y cachés y las reglas de fin
de línea, copiar el contenido de [.gitignore](../.gitignore) y
[.gitattributes](../.gitattributes) a los archivos equivalentes de la nueva raíz.
La creación del workflow se explica en [GITHUB.md](GITHUB.md).

## 2. Definir el contrato y validar las entradas

Antes de implementar, establecer las reglas comunes: todas las entradas deben
ser cadenas, una cadena vacía es válida y los tipos incorrectos producen
`TypeError`. No convertir números o listas con `str()`, porque eso ocultaría un
uso incorrecto de la API.

Comenzar `src/text_utils/operations.py` con:

```python
"""Funciones puras para manipular cadenas Unicode."""

import unicodedata


def _require_string(value: object, parameter: str) -> None:
    """Rechaza entradas que no sean cadenas sin convertirlas implícitamente."""
    if not isinstance(value, str):
        raise TypeError(f"{parameter} debe ser una cadena (str)")
```

La función auxiliar centraliza la validación. Las anotaciones de tipos
documentan el contrato, pero no lo comprueban en tiempo de ejecución; por eso
cada función debe llamar explícitamente a `_require_string`.

## 3. Implementar las cinco funciones

Añadir los siguientes bloques al mismo `operations.py`, después del auxiliar.
Cada bloque incluye una función completa.

### `reverse`: invertir el orden del texto

```python
def reverse(s: str) -> str:
    """Invierte puntos de código; acepta vacío y exige str.

    No agrupa grafemas: una marca combinada se invierte por separado.
    """
    _require_string(s, "s")
    return s[::-1]
```

El corte `[::-1]` recorre la cadena desde el final con paso negativo y construye
una nueva. La cadena original no cambia. No hace falta tratar el vacío por
separado: invertir una secuencia de longitud cero produce otra igual.

| Entrada | Resultado | Qué comprueba |
| --- | --- | --- |
| `"hola"` | `"aloh"` | Orden inverso de una palabra. |
| `"Python!"` | `"!nohtyP"` | Conservación de mayúsculas y puntuación. |
| `""` | `""` | Caso vacío. |
| `"a\u0301b"` | `"b\u0301a"` | Inversión de la marca combinada como otro punto de código. |
| `123` | `TypeError` | Rechazo de un tipo incorrecto. |

Un punto de código no siempre equivale a un carácter visual completo. La
secuencia `a` más un acento combinable contiene dos puntos de código; esta
función invierte ambos por separado. Esa decisión está documentada y probada.

### `count_vowels`: reconocer vocales y acentos

```python
def count_vowels(s: str) -> int:
    """Cuenta a/e/i/o/u y variantes con diacríticos sin distinguir caso.

    Acepta representaciones compuestas y combinadas; exige str.
    """
    _require_string(s, "s")
    normalized = unicodedata.normalize("NFD", s.casefold())
    return sum(character in "aeiou" for character in normalized)
```

Primero `casefold()` permite comparar sin distinguir mayúsculas. Luego la
normalización NFD descompone letras como `é` y `ü` en una letra base y una marca.
Así, cada vocal base cuenta una vez y la marca no suma otra vocal. `sum` agrega
los valores booleanos: cada `True` aporta uno.

| Entrada | Resultado | Qué comprueba |
| --- | --- | --- |
| `"casa"` | `2` | Conteo básico. |
| `"Murciélago"` | `5` | Mayúsculas y acento. |
| `"PINGÜINO"` | `4` | Diéresis. |
| `"e\u0301u\u0308"` | `2` | Vocales con marcas combinadas. |
| `"bcd 123!? ñ"` o `""` | `0` | Ausencia de vocales. |
| `None` | `TypeError` | Validación del argumento. |

Buscar solamente en `"aeiou"` dentro del texto original no reconoce `é` ni `ü`.
La normalización resuelve ese problema sin mantener una lista manual de cada
vocal acentuada. El criterio es la letra base a/e/i/o/u obtenida con NFD.

### `is_palindrome`: comparar texto normalizado

```python
def is_palindrome(s: str) -> bool:
    """Compara sin distinguir caso e ignora caracteres no alfanuméricos.

    NFC conserva acentos compuestos: a y á difieren, igual que n y ñ.
    Las marcas que no se pueden componer se descartan con isalnum().
    Vacío o solo puntuación devuelve True; exige str.
    """
    _require_string(s, "s")
    normalized = unicodedata.normalize("NFC", s)
    normalized = unicodedata.normalize("NFC", normalized.casefold())
    characters = "".join(character for character in normalized if character.isalnum())
    return characters == characters[::-1]
```

El algoritmo realiza cuatro pasos: compone representaciones Unicode
equivalentes con NFC, aplica `casefold` y vuelve a normalizar, conserva letras
y dígitos mediante `isalnum()`, y compara el resultado con su inversión.
Espacios, puntuación y símbolos no participan en la comparación.

Aquí los acentos sí distinguen letras: `a` y `á` son diferentes. Se usa NFC
porque permite que `á` y `a\u0301` se comparen como la misma letra sin eliminar
su acento. Las marcas combinadas que NFC no puede unir a una letra se eliminan
al aplicar el filtro alfanumérico.

| Entrada | Resultado | Qué comprueba |
| --- | --- | --- |
| `"Ana"` | `True` | Comparación independiente de mayúsculas. |
| `"¡Anita, lava la tina!"` | `True` | Eliminación de espacios y puntuación. |
| `"12,321"` | `True` | Conservación de dígitos. |
| `"á x a\u0301"` | `True` | Equivalencia Unicode canónica. |
| `"aÁ"` o `"nñ"` | `False` | Distinción entre letras con y sin diacríticos. |
| `"Python"` | `False` | Texto no palíndromo. |
| `""` o `"!?"` | `True` | La secuencia filtrada vacía coincide con su inversión. |
| `121` | `TypeError` | Los números no se convierten automáticamente en texto. |

El conteo de vocales y la detección de palíndromos tienen contratos distintos.
Por eso NFD ayuda al primero y NFC al segundo; aplicar la misma transformación
a todo el programa cambiaría el significado de las comparaciones.

### `to_upper`: aplicar las reglas Unicode de mayúsculas

```python
def to_upper(s: str) -> str:
    """Convierte a mayúsculas Unicode, conserva símbolos y exige str.

    Algunos caracteres se expanden: ß se convierte en SS.
    """
    _require_string(s, "s")
    return s.upper()
```

`upper()` ya implementa la conversión Unicode. No se necesita una tabla propia
para letras acentuadas, eñes o diéresis. La longitud puede cambiar cuando una
letra se transforma en varias, como `ß` en `SS`.

| Entrada | Resultado | Qué comprueba |
| --- | --- | --- |
| `"hola"` | `"HOLA"` | Conversión básica. |
| `"áéíóúüñ"` | `"ÁÉÍÓÚÜÑ"` | Caracteres acentuados. |
| `"¡Hola! 123"` | `"¡HOLA! 123"` | Conservación de signos y dígitos. |
| `"straße"` | `"STRASSE"` | Expansión Unicode. |
| `""` | `""` | Caso vacío. |
| `b"hola"` | `TypeError` | Los bytes no son cadenas `str`. |

### `concat`: unir dos cadenas sin alterar su contenido

```python
def concat(a: str, b: str) -> str:
    """Une exactamente dos cadenas, sin separadores ni conversiones.

    Lanza TypeError si cualquiera de los argumentos no es str.
    """
    _require_string(a, "a")
    _require_string(b, "b")
    return a + b
```

Ambos argumentos se validan por separado antes de sumarlos. El espacio de
`"Hola mundo"` procede de la segunda entrada, no de la función. Tampoco se
eliminan tabulaciones, saltos de línea o espacios ya presentes.

| Entradas | Resultado | Qué comprueba |
| --- | --- | --- |
| `"Hola", " mundo"` | `"Hola mundo"` | Conservación del espacio existente. |
| `"a", "b"` | `"ab"` | Ausencia de separadores añadidos. |
| `"", "hola"` | `"hola"` | Primera cadena vacía. |
| `"hola", ""` | `"hola"` | Segunda cadena vacía. |
| `"", ""` | `""` | Ambas cadenas vacías. |
| `None, "b"` o `"a", 1` | `TypeError` | Validación de cualquiera de los dos argumentos. |

## 4. Exponer la API y probarla directamente

Escribir en `src/text_utils/__init__.py`:

```python
"""Operaciones de texto con validación explícita de tipos."""

from .operations import concat, count_vowels, is_palindrome, reverse, to_upper

__all__ = ["reverse", "count_vowels", "is_palindrome", "to_upper", "concat"]
```

La API permite importar las funciones desde `text_utils` sin depender del
nombre interno del módulo. Con el paquete instalado, abrir el intérprete:

```powershell
.\.venv\Scripts\python.exe
```

Ejecutar estas expresiones Python:

```python
from text_utils import concat, count_vowels, is_palindrome, reverse, to_upper

reverse("hola")                     # "aloh"
count_vowels("Murciélago")           # 5
is_palindrome("Anita lava la tina")  # True
to_upper("mañana")                  # "MAÑANA"
concat("Hola", " mundo")            # "Hola mundo"
```

Usar `exit()` para volver a PowerShell. Estos ejemplos sirven para observar la
API; las pruebas automatizadas evitan comprobar manualmente cada combinación.

## 5. Convertir los contratos en pruebas

Una prueba debe tener una entrada y un resultado esperado independiente de la
implementación. Por ejemplo, afirmar `reverse("hola") == "aloh"` detecta si la
función deja de invertir; comparar dos llamadas iguales no demostraría nada.

Este bloque permite crear una primera suite en `tests/test_operations.py`.
Incluye dos resultados normales, una cadena vacía y al menos un tipo inválido
por función; `concat` comprueba además cuál de sus dos argumentos es inválido:

```python
import pytest

from text_utils import concat, count_vowels, is_palindrome, reverse, to_upper


@pytest.mark.parametrize(
    ("function", "arguments", "expected"),
    [
        (reverse, ("hola",), "aloh"),
        (reverse, ("Python!",), "!nohtyP"),
        (reverse, ("",), ""),
        (count_vowels, ("casa",), 2),
        (count_vowels, ("Murciélago",), 5),
        (count_vowels, ("",), 0),
        (is_palindrome, ("Ana",), True),
        (is_palindrome, ("Python",), False),
        (is_palindrome, ("",), True),
        (to_upper, ("hola",), "HOLA"),
        (to_upper, ("áüñ",), "ÁÜÑ"),
        (to_upper, ("",), ""),
        (concat, ("Hola", " mundo"), "Hola mundo"),
        (concat, ("a", "b"), "ab"),
        (concat, ("", ""), ""),
    ],
)
def test_ejemplos_del_contrato(function, arguments, expected):
    assert function(*arguments) == expected


@pytest.mark.parametrize(
    ("function", "arguments"),
    [
        (reverse, (123,)),
        (count_vowels, (None,)),
        (is_palindrome, (121,)),
        (to_upper, (b"hola",)),
        (concat, (None, "b")),
        (concat, ("a", 1)),
    ],
)
def test_rechazo_de_tipos(function, arguments):
    with pytest.raises(TypeError):
        function(*arguments)
```

El bloque anterior contiene **21 casos**: 15 resultados esperados y 6 rechazos
de tipos. Para reproducir la suite completa, sustituir ese bloque por el
contenido de [tests/test_operations.py](../tests/test_operations.py) en el
archivo con ese nombre de la nueva carpeta. La suite completa amplía las
entradas de cada función con combinaciones Unicode, símbolos, comparaciones
que deben dar `False` y más tipos inválidos. Sustituir el ejemplo, en lugar de
agregarlo, conserva el recuento de 64 casos de la suite completa.

| Función | Casos con resultado esperado | Casos que exigen `TypeError` | Total |
| --- | ---: | ---: | ---: |
| `reverse` | 6 | 4 | 10 |
| `count_vowels` | 8 | 4 | 12 |
| `is_palindrome` | 12 | 4 | 16 |
| `to_upper` | 6 | 4 | 10 |
| `concat` | 8 | 8 | 16 |
| **Total** | **40** | **24** | **64** |

Ejecutar desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m pip check
```

Con la implementación correcta, la primera suite produce `21 passed`; al
reemplazarla por la suite completa, la salida esperada es `64 passed`.
`pip check` comprueba compatibilidad de dependencias, mientras pytest comprueba
comportamiento: son verificaciones complementarias.

Para estudiar una operación de forma aislada:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k reverse
.\.venv\Scripts\python.exe -m pytest -v -k count_vowels
.\.venv\Scripts\python.exe -m pytest -v -k is_palindrome
.\.venv\Scripts\python.exe -m pytest -v -k to_upper
.\.venv\Scripts\python.exe -m pytest -v -k concat
```

## 6. Demostrar que una prueba detecta lógica incorrecta

Este es un experimento controlado para realizar en una copia de demostración
o en una rama separada. Mantener la implementación correcta como referencia y
modificar únicamente la expresión de retorno dentro de `reverse`.

Para una demostración mediante Pull Request, crear la rama desde la versión
correcta antes de editar:

```powershell
git switch main
if ($LASTEXITCODE -ne 0) { throw 'No se pudo seleccionar la version de referencia.' }
git switch -c demo/falla-intencional
if ($LASTEXITCODE -ne 0) { throw 'No editar hasta crear la rama de demostracion.' }
```

Cambiar manualmente este fragmento de `src/text_utils/operations.py`:

```python
    _require_string(s, "s")
    return s[::-1]
```

por este otro:

```python
    _require_string(s, "s")
    return s
```

La función sigue siendo válida sintácticamente y conserva el rechazo de tipos
incorrectos. El defecto es lógico: devuelve el texto original. Ejecutar:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Con esta única modificación y la suite completa, el resultado esperado es
**5 fallidas y 59 aprobadas**. Fallan las inversiones de palabra, texto con
puntuación, acentos, emoji y marcas combinadas. El vacío sigue pasando porque
su inversión también es vacío, y las cuatro entradas inválidas siguen
produciendo `TypeError`.

La diferencia entre el valor recibido y el esperado permite localizar la
regresión. Por ejemplo, la prueba de `"hola"` muestra que obtuvo `"hola"`, pero
exigía `"aloh"`. No se debe cambiar esa expectativa para acomodar la función
rota: el contrato sigue requiriendo invertir.

Para llevar el experimento a CI, seguir el flujo de Pull Request de
[GITHUB.md](GITHUB.md). En la página del PR, abrir **Checks → unit-tests** y
consultar el paso **Ejecutar las pruebas unitarias**. El registro debe mostrar
las aserciones fallidas y el código de salida no exitoso de pytest.

Cuando `unit-tests` se configura como requisito de integración, ese resultado
impide el merge ordinario. Comprobar tanto el fallo del check como el mensaje
de bloqueo en el PR: un workflow por sí solo no establece esa restricción.
La configuración y el procedimiento de verificación se explican en la guía de
integración continua enlazada.

## 7. Corregir la causa y repetir la validación

Durante la demostración, restaurar `return s[::-1]` dentro de `reverse`,
inmediatamente después de `_require_string(s, "s")`. No modificar las pruebas
ni las otras cuatro funciones. La corrección recupera el recorrido inverso y
mantiene la validación de tipos.

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

El resultado esperado vuelve a ser `64 passed`. Si se realiza el experimento
con un PR, registrar y publicar la corrección en la misma rama:

```powershell
git add src/text_utils/operations.py
if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar la correccion.' }
git commit -m "fix: restaurar la inversion de texto en reverse"
if ($LASTEXITCODE -ne 0) { throw 'No se pudo registrar la correccion.' }
git push origin demo/falla-intencional
```

El cambio provoca una nueva ejecución del workflow del mismo PR. Revisar la
ejecución correspondiente a la corrección y esperar a que termine. Solo cuando
el control obligatorio sea exitoso, y se satisfagan los requisitos de la rama,
completar el merge. Para validar la versión integrada:

```powershell
git switch main
if ($LASTEXITCODE -ne 0) { throw 'No se pudo seleccionar la version integrada.' }
git pull --ff-only origin main
if ($LASTEXITCODE -ne 0) { throw 'No se pudo actualizar la version integrada.' }
.\.venv\Scripts\python.exe -m pytest -v
```

La conclusión se apoya en la secuencia completa: la implementación correcta
satisface el contrato, el defecto controlado rompe cinco comprobaciones y la
corrección restaura esas mismas comprobaciones. CI repite ese mecanismo en un
entorno independiente.

## 8. Presentar el proyecto en 3 a 5 minutos

1. **Primer minuto:** mostrar la estructura y explicar las cinco funciones.
   Usar `count_vowels("PINGÜINO")` e `is_palindrome("aÁ")` para ilustrar por qué
   el tratamiento de los acentos depende del contrato de cada operación.
2. **Segundo minuto:** mostrar una prueba de resultado y otra con
   `pytest.raises`. Explicar que los 64 casos cubren entradas normales, bordes
   y errores de tipos.
3. **Tercer minuto:** mostrar la versión `return s`, ejecutar pytest y leer una
   aserción fallida. Explicar por qué los cinco casos de inversión fallan y el
   vacío sigue pasando. En la variante con CI, mostrar el check y el bloqueo.
4. **Cuarto minuto:** restaurar `return s[::-1]` y repetir las pruebas. Mostrar
   que se corrige el algoritmo sin debilitar sus expectativas.
5. **Último minuto:** explicar cómo el mismo comando se ejecuta en Ubuntu con
   Python 3.12 y cómo un check obligatorio controla la integración. Si se
   muestra GitHub, describir el resultado de la ejecución que se ve en
   pantalla; la duración del runner puede exceder el tiempo de exposición.

Los [hallazgos y resoluciones](EVIDENCIAS.md) desarrollan las conclusiones sobre
Unicode, instalación del paquete, aislamiento de entornos y detección de
regresiones.
