# Validación, hallazgos y decisiones técnicas

La librería se validó mediante resultados esperados para cada función, ejecución
en entornos independientes y una modificación deliberadamente incorrecta. Este
documento explica qué se observó, qué problema resuelve cada decisión y hasta
dónde permiten llegar las conclusiones.

## Cómo se definió el comportamiento

Antes de automatizar las pruebas se definió el contrato de cada función:
qué entradas acepta, qué resultado produce y cómo responde ante datos inválidos.
Así, los resultados esperados no dependen de copiar la implementación en las
pruebas.

| Función | Decisión de implementación | Comportamiento que se comprueba |
| --- | --- | --- |
| `reverse(s)` | Validar `str` e invertir con `s[::-1]` | Se invierte el orden de los puntos de código, incluidos símbolos; la cadena vacía sigue vacía. |
| `count_vowels(s)` | Aplicar `casefold()`, descomponer con NFD y contar `a/e/i/o/u` | Se cuentan vocales mayúsculas y minúsculas, con acento o diéresis, sin contar dos veces sus marcas. |
| `is_palindrome(s)` | Normalizar con NFC, aplicar `casefold()`, normalizar de nuevo y conservar alfanuméricos | Se ignoran espacios, puntuación y símbolos; los dígitos participan y los acentos compuestos se conservan. |
| `to_upper(s)` | Utilizar `str.upper()` después de validar el tipo | Se convierte texto Unicode y se conservan los caracteres sin variante mayúscula. |
| `concat(a, b)` | Validar ambas entradas y devolver `a + b` | Se conserva exactamente el contenido y el orden, sin agregar ni quitar separadores. |

Las cinco funciones son puras: devuelven un resultado sin leer archivos,
acceder a la red ni modificar estado compartido. Esto permite comprobar cada
comportamiento con una entrada y una salida concretas.

### Por qué se rechazan tipos incorrectos

Las anotaciones de tipos documentan la interfaz, pero Python no las impone por
sí solo. Por eso `_require_string` comprueba `isinstance(value, str)` y lanza
`TypeError` antes de operar. Convertir automáticamente `123`, `None` o una lista
en texto ocultaría un uso incorrecto de la interfaz y produciría resultados
ambiguos. Las pruebas usan `pytest.raises(TypeError)` para verificar ese contrato;
en `concat` se comprueba cada argumento por separado y también ambos inválidos.

### Por qué el tratamiento de Unicode cambia según la función

Contar vocales y comparar palíndromos requieren criterios distintos. En el
contador, `á` debe contar como una vocal `a`: NFD separa la letra de su marca y
permite contar solo la letra base. La prueba `"e\u0301u\u0308"` demuestra que las
representaciones descompuestas también producen dos vocales.

En el palíndromo se conserva la diferencia entre `a` y `á`, y entre `n` y `ñ`.
NFC permite que `á` y `a\u0301` se comparen como la misma letra cuando sus
representaciones son canónicamente equivalentes. De ahí que `"aÁ"` no sea
palíndroma y `"á x a\u0301"` sí lo sea. Las marcas combinadas que NFC no logra
componer se descartan al filtrar con `isalnum()`; este es el comportamiento de
la implementación, no una afirmación de cobertura de todas las escrituras.

En `reverse` se invierten puntos de código, no grafemas o caracteres visuales
completos. Una marca combinada puede cambiar de posición respecto de su letra:
`"a\u0301b"` se transforma en `"b\u0301a"`. La prueba correspondiente deja
explícito ese límite. En `to_upper`, el caso `"straße" → "STRASSE"` demuestra
que convertir a mayúsculas puede aumentar la longitud de la cadena.

## Cómo se organizaron las pruebas

`tests/test_operations.py` utiliza `pytest.mark.parametrize` para ejecutar
variaciones independientes de un mismo contrato. Cada fila cuenta como un caso
de prueba y tiene un resultado esperado concreto. La suite incluye cadenas
vacías, combinaciones de mayúsculas y minúsculas, puntuación, acentos, símbolos
y entradas inválidas.

| Función | Casos con entrada válida | Casos de tipo inválido | Total |
| --- | ---: | ---: | ---: |
| `reverse` | 6 | 4 | 10 |
| `count_vowels` | 8 | 4 | 12 |
| `is_palindrome` | 12 | 4 | 16 |
| `to_upper` | 6 | 4 | 10 |
| `concat` | 8 | 8 | 16 |
| **Total** | **40** | **24** | **64** |

Se incluyeron resultados positivos y negativos para evitar pruebas que puedan
aprobar con un valor fijo. Por ejemplo, `is_palindrome` debe aceptar
`"Anita lava la tina"` y rechazar `"Python"`; `count_vowels` debe devolver tanto
cero como cantidades mayores. La cadena vacía es válida en todas las funciones:
se transforma en `""`, produce cero vocales o se considera palíndroma según la
operación. Una cadena formada solo por símbolos también resulta palíndroma
porque, después del filtrado, queda vacía.

## Resultados de instalación y ejecución

Las comprobaciones realizadas el 19 de octubre de 2026 dieron estos resultados:

| Entorno | Python | Forma de instalación | Resultado de `python -m pytest -v` |
| --- | --- | --- | --- |
| Windows, `.venv` | 3.12.6 | Editable, desde `src/text_utils` | **64 passed in 0.12s**, salida 0 |
| Windows, `.venv-clean` | 3.12.6 | Instalación normal mediante wheel | **64 passed in 0.09s**, salida 0 |
| Ubuntu 24.04.2 LTS en WSL, `.venv-linux` | 3.12.3 | Instalación normal mediante wheel | **64 passed in 1.03s**, salida 0 |

`python -m pip check` terminó en los tres entornos con
`No broken requirements found.`. También se comprobó que la instalación de
desarrollo importara el paquete desde `src/text_utils`, mientras que las
instalaciones normales lo cargaran desde el `site-packages` de su propio entorno.

Estas ejecuciones muestran que los casos definidos funcionan en Windows y en
Ubuntu local con Python 3.12. No demuestran compatibilidad con todas las versiones
de Python o todos los sistemas operativos. Los tiempos son registros de esas
ejecuciones; no constituyen una comparación de rendimiento entre plataformas.

La librería no tiene dependencias externas de ejecución. Para probarla se fijó
`pytest==8.4.2` en el extra `dev` de `pyproject.toml`. En la validación también se
resolvieron pluggy 1.7.0, iniconfig 2.3.1, packaging 26.3 y Pygments 2.21.0;
Windows incluyó colorama 0.4.6. Son versiones observadas, no un archivo de bloqueo
de todas las dependencias transitivas. El backend `setuptools>=77` se utiliza en
el entorno aislado de construcción de pip.

## Problemas encontrados y cómo se resolvieron

### Una instalación editable dejó de encontrar el paquete

**Observación.** Después de mover el proyecto, `find_spec('text_utils')` devolvía
`None`. Los metadatos de la instalación editable y los activadores del entorno
virtual conservaban la ubicación anterior.

**Causa.** Una instalación editable enlaza el intérprete con el código fuente
mediante rutas. Mover la carpeta no actualiza automáticamente esos enlaces ni
los ejecutables del entorno virtual.

**Solución.** Se reconstruyeron los entornos virtuales con Python 3.12 en la
ubicación de trabajo y se reinstaló el paquete desde su `pyproject.toml`.

**Verificación.** La importación volvió a resolver al paquete correcto, la
activación seleccionó el intérprete del entorno reconstruido y las 64 pruebas
pasaron tanto en la instalación editable como en la normal. La conclusión es
que los entornos virtuales deben recrearse al trasladar el proyecto; no deben
tratarse como carpetas portables.

### Ubuntu no disponía de `ensurepip`

**Observación.** La instalación disponible de Python en Ubuntu no incluía pip
ni `ensurepip`, por lo que no podía inicializar un entorno con pip mediante el
procedimiento habitual.

**Solución.** Se creó el entorno con `python3.12 -m venv --without-pip` y se
instaló pip 24.2 dentro de él a partir de su wheel oficial. Después se instaló
el proyecto con `python -m pip install '.[dev]'`. Esta solución no requirió
instalar dependencias globales.

**Verificación.** El intérprete del entorno importó la distribución instalada,
las 64 pruebas pasaron y `pip check` no encontró conflictos. La ausencia de
`ensurepip` era una limitación del aprovisionamiento de Python, no un fallo de
la librería. En un entorno que sí incluya ese módulo basta con crear el entorno
virtual de la forma habitual que describe el [README](../README.md).

### Una ejecución desde el código fuente no basta para validar el empaquetado

**Riesgo identificado.** Un paquete puede importar correctamente desde el árbol
de trabajo y, sin embargo, faltar en la distribución instalada por una
configuración incorrecta del empaquetado.

**Decisión.** Se utilizó la estructura `src/`, se declaró la búsqueda de paquetes
en `pyproject.toml` y se comprobó una instalación normal además de la editable.
La estructura `src/` reduce la posibilidad de importar accidentalmente el código
solo por encontrarse en la raíz del proyecto.

**Verificación.** Las instalaciones normales construyeron un wheel, cargaron
`text_utils` desde `site-packages` y aprobaron las mismas pruebas. Esto aporta
evidencia de que el paquete instalable contiene la implementación necesaria.

## Cómo se comprobó que las pruebas detectan un error

En una copia local aislada se sustituyó únicamente la instrucción de `reverse`:

```python
# Implementación correcta:
return s[::-1]

# Modificación incorrecta utilizada en la comprobación:
return s
```

Se comprobó que el intérprete cargara esa copia y se ejecutó pytest. El resultado
observado fue **5 failed, 59 passed in 0.20s**, con código de salida **1**.
Fallaron los casos de palabra, mayúscula y puntuación, acentos, emoji y puntos
de código combinados. El código de la implementación principal se conservó.

El resultado se explica por el contrato: devolver una palabra intacta incumple
la inversión, mientras que devolver una cadena vacía intacta sigue produciendo
el resultado esperado. Las pruebas de tipos continuaron aprobando porque la
validación no se modificó. Las otras cuatro funciones tampoco cambiaron.

La conclusión es que la suite detecta esta regresión concreta y que pytest
comunica el fallo mediante un código de salida utilizable por CI. Una mutación
no prueba que se detecten todos los errores posibles ni equivale a una medida
de cobertura total. El [guion de demostración](DEMO.md) explica cómo reproducir
el ciclo de introducir el defecto, observar el fallo y aplicar la corrección.

## Qué se validó del proceso de integración continua

El workflow `.github/workflows/ci.yml` declara un job `unit-tests` sobre
`ubuntu-latest`, configura Python 3.12, instala el paquete con su extra `dev` y
ejecuta `python -m pytest -v`. Se activa para los Pull Requests dirigidos a
`main`, además de cambios en esa rama y ejecución manual. Sus permisos son
`contents: read`.

La revisión encontró que no utiliza `continue-on-error`, `pull_request_target`
ni filtros de rutas que omitan la comprobación. Si pytest devuelve 1, el paso
de pruebas falla y ese resultado se propaga al job. Este vínculo entre una
prueba fallida y el resultado del job es la base del control automático.

El archivo se validó con **actionlint 1.7.12**, que terminó sin errores y con
código de salida 0. La ejecución de las pruebas en Ubuntu local comprueba
además que el paquete y la suite funcionan en Linux. La validación estática
comprueba el workflow, pero no sustituye la ejecución en un runner de GitHub.
Del mismo modo, un job fallido y una regla de protección son piezas diferentes:
la regla debe exigir `unit-tests` para impedir una integración con resultados
fallidos. El procedimiento de configuración y comprobación se explica en
[GITHUB.md](GITHUB.md).

## Cómo volver a comprobar los resultados

También se comprobó la guía de reconstrucción: se reunieron el auxiliar y las
cinco funciones de los fragmentos de [DEMO.md](DEMO.md), y se ejecutaron sobre
esa implementación los 21 ejemplos del tutorial y los 64 casos de la suite.
Las **85 comprobaciones pasaron**. Ese total combina dos conjuntos de pruebas;
el comando habitual del proyecto ejecuta los 64 casos de `tests/`.
Se verificó además que el TOML y el YAML documentados coincidan con los archivos
de configuración. Esto aporta evidencia de que las instrucciones permiten
reproducir el comportamiento descrito, además de explicar sus algoritmos.

Con los entornos ya instalados, ejecutar desde la raíz del proyecto en
PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m pip check
.\.venv-clean\Scripts\python.exe -m pytest -v
.\.venv-clean\Scripts\python.exe -m pip check
```

En Ubuntu/WSL, usando el entorno Linux:

```bash
.venv-linux/bin/python -m pytest -v
.venv-linux/bin/python -m pip check
```

El [README](../README.md) describe la instalación desde cero. Al repetir las
comprobaciones, contrastar el total de casos, el código de salida, la ubicación
del paquete importado y la ausencia de conflictos. Son las observaciones que
sustentan la conclusión de que la implementación y su distribución funcionan
en los entornos evaluados.
