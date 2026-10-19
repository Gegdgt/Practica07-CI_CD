# Comandos ejecutados, resultados y explicación

Ejecutar los comandos en PowerShell desde la carpeta raíz `Practica07-CI_CD`, con el entorno `.venv` instalado. Cada apartado presenta un comando, su salida obtenida y la explicación del resultado.

Las salidas se capturaron en una ejecución local realizada el 19/10/2026. Se muestran completas; únicamente se sustituyó la ruta absoluta de la carpeta por `<raiz-del-proyecto>`. Los ejemplos con `-c` ejecutan código Python directamente desde PowerShell, sin abrir el intérprete interactivo.

## 1. Todas las pruebas

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

**Resultado obtenido:**

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-8.4.2, pluggy-1.7.0 -- <raiz-del-proyecto>\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: <raiz-del-proyecto>
configfile: pyproject.toml
testpaths: tests
collecting ... collected 64 items

tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[palabra] PASSED [  1%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[mayuscula-y-puntuacion] PASSED [  3%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[cadena-vacia] PASSED [  4%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[acentos] PASSED [  6%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[emoji] PASSED [  7%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[puntos-de-codigo-combinados] PASSED [  9%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[None] PASSED [ 10%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[123] PASSED [ 12%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[valor2] PASSED [ 14%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[hola] PASSED [ 15%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[palabra] PASSED [ 17%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[mayusculas-y-acento] PASSED [ 18%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[vocales-acentuadas-y-dieresis] PASSED [ 20%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[sin-vocales] PASSED [ 21%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[cadena-vacia] PASSED [ 23%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[acentos-combinados] PASSED [ 25%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[todas-las-vocales] PASSED [ 26%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[mezcla-de-casos-y-dieresis] PASSED [ 28%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[None] PASSED [ 29%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[123] PASSED [ 31%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[valor2] PASSED [ 32%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[aeiou] PASSED [ 34%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[palabra-palindroma] PASSED [ 35%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[ignora-mayusculas] PASSED [ 37%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[ignora-espacios] PASSED [ 39%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[ignora-puntuacion] PASSED [ 40%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[acentos-simetricos] PASSED [ 42%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[conserva-los-acentos] PASSED [ 43%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[enie-distinta-de-ene] PASSED [ 45%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[equivalencia-canonica-unicode] PASSED [ 46%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[cadena-vacia] PASSED [ 48%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[solo-puntuacion-y-simbolos] PASSED [ 50%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[palabra-no-palindroma] PASSED [ 51%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[conserva-digitos] PASSED [ 53%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[None] PASSED [ 54%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[121] PASSED [ 56%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[valor2] PASSED [ 57%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[ana] PASSED [ 59%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[minusculas] PASSED [ 60%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[mezcla-de-casos] PASSED [ 62%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[cadena-vacia] PASSED [ 64%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[acentos-dieresis-y-enie] PASSED [ 65%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[simbolos-y-salto] PASSED [ 67%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[expansion-unicode] PASSED [ 68%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[None] PASSED [ 70%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[123] PASSED [ 71%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[valor2] PASSED [ 73%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[hola] PASSED [ 75%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[espacio-existente] PASSED [ 76%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[sin-separador] PASSED [ 78%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[ambas-vacias] PASSED [ 79%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[primera-vacia] PASSED [ 81%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[segunda-vacia] PASSED [ 82%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[unicode-y-mayusculas] PASSED [ 84%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[emoji-y-puntuacion] PASSED [ 85%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[conserva-espacios-y-tabulacion] PASSED [ 87%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-none] PASSED [ 89%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-entero] PASSED [ 90%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-lista] PASSED [ 92%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-booleano] PASSED [ 93%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[segundo-none] PASSED [ 95%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[segundo-entero] PASSED [ 96%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[segundo-lista] PASSED [ 98%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[ambos-invalidos] PASSED [100%]

============================= 64 passed in 0.07s ==============================
```

**Explicación:** Se encontraron y ejecutaron **64 pruebas**, y todas pasaron. `PASSED` indica que el resultado de cada caso coincidió con lo esperado. Las pruebas de entradas inválidas también pasan porque comprueban que se lance `TypeError`. Los porcentajes muestran el avance de la ejecución, no la cobertura del código. La cabecera identifica Python 3.12.6 y pytest 8.4.2; `pyproject.toml` configura la búsqueda dentro de `tests`. El tiempo del resumen corresponde a esta ejecución y puede variar.

## 2. Comprobación de dependencias

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pip check
```

**Resultado obtenido:**

```text
No broken requirements found.
```

**Explicación:** `No broken requirements found.` significa que pip no encontró dependencias declaradas faltantes ni incompatibles en este entorno virtual. Esta comprobación revisa los paquetes instalados; las pruebas anteriores verifican el comportamiento de la librería.

## 3. Pruebas de reverse

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k reverse
```

**Resultado obtenido:**

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-8.4.2, pluggy-1.7.0 -- <raiz-del-proyecto>\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: <raiz-del-proyecto>
configfile: pyproject.toml
testpaths: tests
collecting ... collected 64 items / 54 deselected / 10 selected

tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[palabra] PASSED [ 10%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[mayuscula-y-puntuacion] PASSED [ 20%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[cadena-vacia] PASSED [ 30%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[acentos] PASSED [ 40%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[emoji] PASSED [ 50%]
tests/test_operations.py::test_reverse_invierte_puntos_de_codigo[puntos-de-codigo-combinados] PASSED [ 60%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[None] PASSED [ 70%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[123] PASSED [ 80%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[valor2] PASSED [ 90%]
tests/test_operations.py::test_reverse_rechaza_tipos_invalidos[hola] PASSED [100%]

====================== 10 passed, 54 deselected in 0.03s ======================
```

**Explicación:** Pasaron **10 pruebas** de `reverse`. Las otras **54** aparecen como `deselected` porque el filtro `-k` las excluyó de esta ejecución; no son fallas. Se verificó la inversión de palabras, puntuación, acentos, emoji y puntos de código combinados, además de la cadena vacía y el rechazo de tipos incorrectos.

## 4. Pruebas de count_vowels

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k count_vowels
```

**Resultado obtenido:**

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-8.4.2, pluggy-1.7.0 -- <raiz-del-proyecto>\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: <raiz-del-proyecto>
configfile: pyproject.toml
testpaths: tests
collecting ... collected 64 items / 52 deselected / 12 selected

tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[palabra] PASSED [  8%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[mayusculas-y-acento] PASSED [ 16%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[vocales-acentuadas-y-dieresis] PASSED [ 25%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[sin-vocales] PASSED [ 33%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[cadena-vacia] PASSED [ 41%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[acentos-combinados] PASSED [ 50%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[todas-las-vocales] PASSED [ 58%]
tests/test_operations.py::test_count_vowels_cuenta_vocales_unicode[mezcla-de-casos-y-dieresis] PASSED [ 66%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[None] PASSED [ 75%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[123] PASSED [ 83%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[valor2] PASSED [ 91%]
tests/test_operations.py::test_count_vowels_rechaza_tipos_invalidos[aeiou] PASSED [100%]

====================== 12 passed, 52 deselected in 0.03s ======================
```

**Explicación:** Pasaron **12 pruebas** de `count_vowels`. Las otras **52** aparecen como `deselected` porque el filtro `-k` las excluyó de esta ejecución; no son fallas. Se verificó el conteo de vocales en mayúsculas y minúsculas, con acentos y diéresis, incluyendo marcas combinadas, texto sin vocales, cadena vacía y tipos incorrectos.

## 5. Pruebas de is_palindrome

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k is_palindrome
```

**Resultado obtenido:**

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-8.4.2, pluggy-1.7.0 -- <raiz-del-proyecto>\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: <raiz-del-proyecto>
configfile: pyproject.toml
testpaths: tests
collecting ... collected 64 items / 48 deselected / 16 selected

tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[palabra-palindroma] PASSED [  6%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[ignora-mayusculas] PASSED [ 12%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[ignora-espacios] PASSED [ 18%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[ignora-puntuacion] PASSED [ 25%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[acentos-simetricos] PASSED [ 31%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[conserva-los-acentos] PASSED [ 37%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[enie-distinta-de-ene] PASSED [ 43%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[equivalencia-canonica-unicode] PASSED [ 50%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[cadena-vacia] PASSED [ 56%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[solo-puntuacion-y-simbolos] PASSED [ 62%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[palabra-no-palindroma] PASSED [ 68%]
tests/test_operations.py::test_is_palindrome_normaliza_sin_eliminar_acentos[conserva-digitos] PASSED [ 75%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[None] PASSED [ 81%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[121] PASSED [ 87%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[valor2] PASSED [ 93%]
tests/test_operations.py::test_is_palindrome_rechaza_tipos_invalidos[ana] PASSED [100%]

====================== 16 passed, 48 deselected in 0.03s ======================
```

**Explicación:** Pasaron **16 pruebas** de `is_palindrome`. Las otras **48** aparecen como `deselected` porque el filtro `-k` las excluyó de esta ejecución; no son fallas. Se verificaron resultados verdaderos y falsos, la omisión de espacios y puntuación, la conservación de dígitos y diferencias entre letras acentuadas, equivalencias Unicode, cadenas vacías y tipos incorrectos.

## 6. Pruebas de to_upper

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k to_upper
```

**Resultado obtenido:**

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-8.4.2, pluggy-1.7.0 -- <raiz-del-proyecto>\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: <raiz-del-proyecto>
configfile: pyproject.toml
testpaths: tests
collecting ... collected 64 items / 54 deselected / 10 selected

tests/test_operations.py::test_to_upper_respeta_conversion_unicode[minusculas] PASSED [ 10%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[mezcla-de-casos] PASSED [ 20%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[cadena-vacia] PASSED [ 30%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[acentos-dieresis-y-enie] PASSED [ 40%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[simbolos-y-salto] PASSED [ 50%]
tests/test_operations.py::test_to_upper_respeta_conversion_unicode[expansion-unicode] PASSED [ 60%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[None] PASSED [ 70%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[123] PASSED [ 80%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[valor2] PASSED [ 90%]
tests/test_operations.py::test_to_upper_rechaza_tipos_invalidos[hola] PASSED [100%]

====================== 10 passed, 54 deselected in 0.03s ======================
```

**Explicación:** Pasaron **10 pruebas** de `to_upper`. Las otras **54** aparecen como `deselected` porque el filtro `-k` las excluyó de esta ejecución; no son fallas. Se verificó la conversión a mayúsculas, incluidos acentos, diéresis, ñ y la expansión de ß a SS, junto con símbolos, cadena vacía y tipos incorrectos.

## 7. Pruebas de concat

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -m pytest -v -k concat
```

**Resultado obtenido:**

```text
============================= test session starts =============================
platform win32 -- Python 3.12.6, pytest-8.4.2, pluggy-1.7.0 -- <raiz-del-proyecto>\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: <raiz-del-proyecto>
configfile: pyproject.toml
testpaths: tests
collecting ... collected 64 items / 48 deselected / 16 selected

tests/test_operations.py::test_concat_une_exactamente_las_cadenas[espacio-existente] PASSED [  6%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[sin-separador] PASSED [ 12%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[ambas-vacias] PASSED [ 18%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[primera-vacia] PASSED [ 25%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[segunda-vacia] PASSED [ 31%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[unicode-y-mayusculas] PASSED [ 37%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[emoji-y-puntuacion] PASSED [ 43%]
tests/test_operations.py::test_concat_une_exactamente_las_cadenas[conserva-espacios-y-tabulacion] PASSED [ 50%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-none] PASSED [ 56%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-entero] PASSED [ 62%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-lista] PASSED [ 68%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[primero-booleano] PASSED [ 75%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[segundo-none] PASSED [ 81%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[segundo-entero] PASSED [ 87%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[segundo-lista] PASSED [ 93%]
tests/test_operations.py::test_concat_rechaza_cualquier_argumento_invalido[ambos-invalidos] PASSED [100%]

====================== 16 passed, 48 deselected in 0.04s ======================
```

**Explicación:** Pasaron **16 pruebas** de `concat`. Las otras **48** aparecen como `deselected` porque el filtro `-k` las excluyó de esta ejecución; no son fallas. Se verificó la unión exacta de dos cadenas, incluyendo espacios existentes, tabulaciones, caracteres especiales y cadenas vacías. También se comprobó que ambos argumentos deben ser cadenas.

## 8. Invertir una cadena

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import reverse; print(reverse('hola'))"
```

**Resultado obtenido:**

```text
aloh
```

**Explicación:** La función devolvió `aloh`, que contiene los caracteres de `hola` en orden inverso.

## 9. Contar vocales con diéresis

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import count_vowels; print(count_vowels('PINGÜINO'))"
```

**Resultado obtenido:**

```text
4
```

**Explicación:** El resultado es `4` porque se cuentan I, Ü, I y O. Las mayúsculas y la diéresis no impiden reconocer las vocales.

## 10. Reconocer una frase palíndroma

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import is_palindrome; print(is_palindrome('Anita lava la tina'))"
```

**Resultado obtenido:**

```text
True
```

**Explicación:** El resultado `True` indica que la frase es palíndroma. Al ignorar espacios y mayúsculas, la secuencia coincide con su inversa.

## 11. Reconocer una palabra que no es palíndroma

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import is_palindrome; print(is_palindrome('Python'))"
```

**Resultado obtenido:**

```text
False
```

**Explicación:** El resultado `False` indica que la palabra no es palíndroma: `python` y su inversa `nohtyp` son diferentes.

## 12. Convertir a mayúsculas

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import to_upper; print(to_upper('mañana'))"
```

**Resultado obtenido:**

```text
MAÑANA
```

**Explicación:** El resultado `MAÑANA` demuestra que se convierten las letras a mayúsculas, incluida la ñ.

## 13. Concatenar dos cadenas

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import concat; print(concat('Hola', ' mundo'))"
```

**Resultado obtenido:**

```text
Hola mundo
```

**Explicación:** El resultado conserva exactamente el contenido de ambos argumentos. El espacio ya estaba al inicio de la segunda cadena; la función no lo agregó.

## 14. Rechazar una entrada inválida

**Comando ejecutado:**

```powershell
.\.venv\Scripts\python.exe -c "from text_utils import reverse; reverse(123)"
```

**Resultado obtenido:**

```text
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "<raiz-del-proyecto>\src\text_utils\operations.py", line 18, in reverse
    _require_string(s, "s")
  File "<raiz-del-proyecto>\src\text_utils\operations.py", line 9, in _require_string
    raise TypeError(f"{parameter} debe ser una cadena (str)")
TypeError: s debe ser una cadena (str)
```

**Explicación:** La llamada terminó con `TypeError: s debe ser una cadena (str)` porque `123` es un entero. La traza señala la llamada, la validación de `reverse` y la línea que lanza la excepción. Este rechazo es el comportamiento requerido. El comando terminó con código de salida `1` porque la excepción no se capturó; en las pruebas unitarias se usa `pytest.raises(TypeError)` para comprobarla y obtener `PASSED`.