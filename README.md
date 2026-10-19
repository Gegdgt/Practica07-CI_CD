# Librería de texto e integración continua

Práctica 7 de CC3047 – Administración y Mantenimiento de Sistemas,
Universidad del Valle de Guatemala, semestre II de 2026.

El proyecto implementa cinco operaciones de texto en Python 3.12. Cada operación
recibe cadenas, produce un resultado y rechaza tipos incorrectos. Las pruebas
unitarias comprueban ese contrato; GitHub Actions permite repetirlas
al proponer cambios al programa.

## Qué hace el programa

Es una librería que se importa desde otros programas de Python. No necesita una
interfaz, una base de datos ni conexión a servicios para ejecutar sus funciones.
Las operaciones son puras: no modifican la entrada ni guardan información entre
llamadas, por lo que los resultados pueden comprobarse de forma independiente.

| Función | Resultado | Ejemplo |
| --- | --- | --- |
| `reverse(s)` | Cadena con sus puntos de código en orden inverso. | `reverse("hola") == "aloh"` |
| `count_vowels(s)` | Número de vocales, incluidas sus variantes con acentos y diéresis. | `count_vowels("PINGÜINO") == 4` |
| `is_palindrome(s)` | Booleano que indica si el texto normalizado se lee igual en ambos sentidos. | `is_palindrome("¡Anita lava la tina!") is True` |
| `to_upper(s)` | Cadena convertida a mayúsculas mediante las reglas Unicode. | `to_upper("mañana") == "MAÑANA"` |
| `concat(a, b)` | Las dos cadenas unidas, sin añadir separadores. | `concat("Hola", " mundo") == "Hola mundo"` |

Todas las entradas deben ser `str`. Una entrada inválida produce `TypeError`;
no se convierte automáticamente un número, una lista o `None` en texto. Las
anotaciones de tipos describen el contrato y la validación interna lo hace
cumplir durante la ejecución.

Las cadenas vacías son válidas: inversión, mayúsculas y concatenación pueden
producir `""`; el contador devuelve `0` y el detector de palíndromos devuelve
`True` porque no existen caracteres que contradigan la simetría.

## Cómo se construyó la solución

La construcción sigue una secuencia que relaciona cada decisión con una forma
de comprobarla:

1. **Definir los contratos.** Especificar entradas válidas, resultados,
   comportamiento con vacío y excepciones antes de implementar cada función.
2. **Centralizar la validación.** Usar `_require_string` para aplicar la misma
   regla de tipos sin repetirla ni introducir conversiones implícitas.
3. **Implementar las operaciones.** Utilizar slicing, normalización Unicode,
   filtrado y métodos de cadenas de la biblioteca estándar.
4. **Diseñar los escenarios de prueba.** Comparar resultados concretos e incluir
   entradas normales, casos borde y errores para cada operación.
5. **Validar la instalación.** Probar tanto el código editable como el paquete
   construido, para detectar dependencias de rutas locales.
6. **Automatizar la comprobación.** Ejecutar la misma suite en un entorno de
   Ubuntu preparado por GitHub Actions.

La [guía de construcción y demostración](docs/DEMO.md) desarrolla estos pasos,
con la implementación de cada función y ejemplos de pruebas. La
[guía de integración continua](docs/GITHUB.md) explica cómo reproducir la
configuración automática. Los [hallazgos y conclusiones](docs/EVIDENCIAS.md)
relacionan las observaciones técnicas con las soluciones adoptadas.

## Decisiones sobre Unicode

Las cinco operaciones no normalizan el texto de la misma manera, porque
resuelven problemas distintos:

- **Inversión:** `s[::-1]` invierte puntos de código. Una letra y una marca
  combinada se invierten por separado; no se intenta invertir grafemas completos.
- **Conteo de vocales:** `casefold()` elimina diferencias de mayúsculas y NFD
  descompone letras acentuadas. Así, `é` y `e\u0301` aportan una sola vocal,
  y `ü` se reconoce por su base `u`.
- **Palíndromos:** NFC unifica representaciones canónicamente equivalentes;
  `casefold()` permite ignorar mayúsculas y `isalnum()` conserva letras y
  dígitos. Se ignoran espacios, puntuación y símbolos. `a` y `á` son distintos,
  al igual que `n` y `ñ`. Las marcas combinadas que NFC no puede componer se
  eliminan por el filtro alfanumérico.
- **Mayúsculas:** `upper()` aplica las reglas Unicode y puede cambiar la
  longitud: `"straße"` se convierte en `"STRASSE"`.
- **Concatenación:** `a + b` conserva exactamente el contenido y el orden de
  ambas entradas, incluidos espacios, tabulaciones y acentos.

## Organización del proyecto

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
│   ├── GITHUB.md
│   └── EVIDENCIAS.md
├── .gitattributes
├── .gitignore
├── pyproject.toml
└── README.md
```

`operations.py` contiene la lógica y `__init__.py` expone la API pública.
`tests/` contiene las comprobaciones del comportamiento. `pyproject.toml`
define el paquete, Python requerido, dependencias y descubrimiento de pruebas.
El directorio `src/` separa el código importable de los archivos auxiliares y
permite comprobar que la instalación del paquete funciona correctamente.

Los entornos virtuales, las cachés y los artefactos de construcción son
recreables y se excluyen mediante `.gitignore`.

## Instalación y ejecución

Los comandos se ejecutan desde la carpeta que contiene `pyproject.toml`.
Se requiere Python 3.12. La librería no tiene dependencias externas de ejecución;
pytest 8.4.2 se instala como dependencia de desarrollo mediante el extra `dev`.
El backend de construcción es `setuptools>=77`.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -v
```

Invocar el ejecutable del entorno evita depender del Python predeterminado del
sistema. Si el entorno ya está activado, se puede usar `python -m pytest -v`.

### Ubuntu

Python debe disponer del soporte de `venv` y `ensurepip`. Para evitar mezclar
entornos de distintos sistemas cuando se comparte una carpeta con WSL, se
utiliza un nombre diferente:

```bash
python3.12 -m venv .venv-linux
.venv-linux/bin/python -m pip install -e '.[dev]'
.venv-linux/bin/python -m pip check
.venv-linux/bin/python -m pytest -v
```

Un entorno virtual debe recrearse cuando cambia su ubicación o el sistema
operativo. El análisis del problema de rutas y de la ausencia de `ensurepip`
se describe en [hallazgos de instalación](docs/EVIDENCIAS.md).

### Uso desde Python

Con el paquete instalado, el siguiente código puede ejecutarse desde un archivo
Python o desde el intérprete del entorno:

```python
from text_utils import concat, count_vowels, is_palindrome, reverse, to_upper

assert reverse("hola") == "aloh"
assert count_vowels("PINGÜINO") == 4
assert is_palindrome("¡Anita lava la tina!") is True
assert to_upper("mañana") == "MAÑANA"
assert concat("Hola", " mundo") == "Hola mundo"
```

### Comprobación de una instalación independiente

La instalación editable permite probar los cambios del código sin reinstalar.
Una instalación normal comprueba además la construcción del paquete:

```powershell
py -3.12 -m venv .venv-clean
.\.venv-clean\Scripts\python.exe -m pip install '.[dev]'
.\.venv-clean\Scripts\python.exe -m pip check
.\.venv-clean\Scripts\python.exe -m pytest -v
```

## Cómo se comprueba el comportamiento

La suite contiene **64 casos**. `pytest.mark.parametrize` reúne entradas y
salidas esperadas sin duplicar la lógica de la prueba. `pytest.raises(TypeError)`
comprueba las entradas inválidas.

| Función | Casos | Qué se busca detectar |
| --- | ---: | --- |
| `reverse` | 10 | Inversión incorrecta, pérdida de caracteres o aceptación de otros tipos. |
| `count_vowels` | 12 | Omisiones de mayúsculas, acentos, diéresis o representaciones combinadas. |
| `is_palindrome` | 16 | Comparación sin normalizar, tratamiento incorrecto de puntuación o pérdida indebida de acentos compuestos. |
| `to_upper` | 10 | Conversión incompleta o alteración de caracteres especiales. |
| `concat` | 16 | Separadores añadidos, espacios eliminados o validación de un solo argumento. |

Las 64 pruebas se aprobaron en desarrollo y en instalación limpia sobre Windows,
y en una instalación sobre Ubuntu. Además, una alteración controlada de
`reverse` produjo cinco fallas. Esto permite concluir que las pruebas detectan
esa regresión concreta; no demuestra que cualquier error posible esté cubierto.
La [validación técnica](docs/EVIDENCIAS.md) explica el método y sus límites.

## Cómo interviene la integración continua

El workflow [ci.yml](.github/workflows/ci.yml) prepara Ubuntu y Python 3.12,
instala el paquete y ejecuta `python -m pytest -v`. El job se llama `unit-tests`.
La configuración declara su ejecución en Pull Requests hacia `main`, cambios
a `main` y activación manual.

La comprobación automática permite evaluar cambios con el mismo procedimiento.
Al configurar `unit-tests` como requisito de integración, una prueba fallida o
incompleta impide fusionar el cambio. Las pruebas detectan el error; la regla
que exige el check es la que impide integrarlo. La [guía de CI](docs/GITHUB.md)
explica esta relación y cómo reproducirla.
