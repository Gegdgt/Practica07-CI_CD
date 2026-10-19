# Cómo reproducir la integración continua

La integración continua vuelve a instalar y probar la librería de texto cada
vez que se propone un cambio hacia `main`. Su propósito es detectar una
regresión antes de incorporarla: por ejemplo, que `reverse("hola")` deje de
devolver `"aloh"` o que `concat` convierta un número a texto en vez de lanzar
`TypeError`.

El programa y las pruebas se construyen siguiendo el [README](../README.md).
Esta guía explica cómo automatizar esa misma verificación y convertir su
resultado en una condición para integrar cambios. La
[demostración](DEMO.md) reproduce un error y su corrección, y el
[análisis de resultados](EVIDENCIAS.md) explica qué permiten concluir las pruebas.

## 1. Qué se ejecuta

```text
Pull Request hacia main
        ↓
Entorno Ubuntu nuevo
        ↓
Obtener código → seleccionar Python 3.12
        ↓
Instalar paquete y pytest desde pyproject.toml
        ↓
Ejecutar los 64 casos de la suite
        ↓
Código de salida de pytest → resultado de unit-tests
        ↓
Regla de protección → permitir o bloquear la integración
```

La misma suite revisa los cinco contratos de la librería:

| Función | Comportamiento que deben conservar los cambios |
|---|---|
| `reverse` | Invertir los puntos de código, incluidos caracteres especiales, sin aceptar otros tipos. |
| `count_vowels` | Contar vocales con mayúsculas, acentos y diéresis, incluidas representaciones Unicode combinadas. |
| `is_palindrome` | Ignorar mayúsculas y caracteres no alfanuméricos, respetando la política documentada para los acentos. |
| `to_upper` | Aplicar la conversión Unicode y conservar puntuación y símbolos. |
| `concat` | Unir exactamente dos cadenas sin insertar ni eliminar separadores. |

Las entradas vacías y los tipos inválidos forman parte del contrato. Un cambio
que conserva los ejemplos más sencillos puede fallar en esos límites; por eso
el workflow ejecuta la suite completa.

## 2. Crear el workflow

Guarda este contenido en `.github/workflows/ci.yml`, desde la raíz del proyecto.
Es la configuración utilizada por la librería:

```yaml
name: Integración continua

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  unit-tests:
    name: unit-tests
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Obtener el código
        uses: actions/checkout@v7.0.1
      - name: Configurar Python 3.12
        uses: actions/setup-python@v7.0.0
        with:
          python-version: '3.12'
      - name: Instalar el paquete y las dependencias de pruebas
        run: python -m pip install '.[dev]'
      - name: Ejecutar las pruebas unitarias
        run: python -m pytest -v
```

`pull_request` cubre la apertura, reapertura y actualización de un PR cuya
rama de destino sea `main`. `push` comprueba el resultado incorporado a `main`.
`workflow_dispatch` permite iniciar una ejecución manual desde Actions cuando
el workflow está en la rama predeterminada. La selección de eventos sigue la
[referencia oficial de GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).

## 3. Por qué se eligió esta configuración

| Decisión | Razón técnica |
|---|---|
| `ubuntu-latest` | Proporciona un entorno de ejecución independiente de la instalación local de Windows. |
| Python `3.12` | Mantiene la misma versión menor del lenguaje en desarrollo y en CI. El parche concreto puede variar. |
| `actions/checkout@v7.0.1` | Obtiene el código que se va a probar mediante una versión oficial estable de la acción. |
| `actions/setup-python@v7.0.0` | Selecciona Python explícitamente, sin depender de la versión predeterminada del runner. |
| `contents: read` | El job solo necesita leer el proyecto e instalarlo; no publica ni modifica archivos remotos. |
| Nombre único `unit-tests` | Ofrece un identificador estable que la regla de protección puede exigir. |
| Límite de cinco minutos | Evita que un proceso atascado mantenga la ejecución indefinidamente. |
| Sin filtros de archivos ni condiciones del job | Las propuestas hacia `main` reciben la misma verificación, incluso si solo cambian documentación. |
| Sin `continue-on-error` | Una falla de pytest produce una falla visible del job. |

Las versiones de las acciones corresponden a sus publicaciones oficiales:
[checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1) y
[setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0).

`python -m pip install '.[dev]'` instala el paquete definido por
`pyproject.toml`, junto con `pytest==8.4.2`. Esto verifica también que la
distribución pueda instalarse desde `src/`; las pruebas no dependen de agregar
esa carpeta manualmente a `PYTHONPATH`. La librería no requiere dependencias
externas en tiempo de ejecución: utiliza operaciones de cadenas y
`unicodedata`, incluidos con Python.

El comando `python -m pytest -v` usa el mismo intérprete con el que se instaló
el paquete. La opción `-v` muestra cada caso parametrizado, lo que permite
identificar con precisión qué entrada dejó de cumplir el contrato. Se usa
`pull_request` para probar la propuesta sin introducir el contexto de
`pull_request_target`.

## 4. Reproducir la ejecución antes de automatizarla

Con Python 3.12 y el soporte de `venv` y `ensurepip` disponibles en Ubuntu, abre
una terminal en la raíz del proyecto:

```bash
python3.12 -m venv .venv-ci
source .venv-ci/bin/activate
python -m pip install '.[dev]'
python -m pip check
python -m pytest -v
```

Esta instalación nueva permite detectar dependencias que estuvieran disponibles
por accidente en otro entorno. `pip check` revisa la compatibilidad declarada
de las dependencias; pytest verifica el comportamiento. Son comprobaciones
complementarias. Los comandos equivalentes para PowerShell están en el
[README](../README.md).

Para revisar la sintaxis y las referencias del workflow, si `actionlint` está
instalado, ejecuta desde la raíz:

```powershell
actionlint .github/workflows/ci.yml
```

La validación estática detecta errores de configuración. La prueba completa
requiere una ejecución de Actions que instale el paquete y llegue al paso de
pytest.

## 5. Hacer obligatorio el resultado de las pruebas

Para reproducir la configuración en un repositorio de GitHub, incorpora el
proyecto con el workflow en `main` y abre un PR con una mejora pequeña de
documentación. En **Checks**, abre `unit-tests` y verifica que los pasos de
instalación y pruebas terminen correctamente. Esa primera ejecución permite
seleccionar el check por su nombre al configurar la regla.

En **Settings > Branches > Add classic branch protection rule**, configura:

1. Patrón de rama: `main`.
2. Exigir un Pull Request antes de fusionar; dejar desactivada la exigencia de
   aprobaciones manuales, equivalente a cero revisiones obligatorias.
3. Exigir comprobaciones exitosas y seleccionar `unit-tests`, emitido por
   GitHub Actions.
4. Exigir que la rama esté actualizada con `main` antes de fusionar.
5. Activar **Do not allow bypassing the above settings**, para aplicar también
   las condiciones a administradores.
6. Mantener desactivadas las opciones que permiten force push y eliminación.
7. Guardar y volver a abrir la regla para revisar los valores.

Estos pasos reproducen la configuración descrita por la
[documentación de protección de ramas](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule).

El workflow calcula el resultado de las pruebas; la regla exige ese resultado
para integrar una propuesta. Ambas piezas son necesarias para demostrar que
un error detiene la integración. Para comprobarlo, sigue el experimento de
[DEMO.md](DEMO.md): observa el check fallido y el mensaje de bloqueo del PR
correspondiente a esa ejecución, sin intentar fusionar código defectuoso.

## 6. Interpretar una falla y decidir qué corregir

Abre **Actions > Integración continua > ejecución > unit-tests**. Empieza por
el primer paso que falla:

| Evidencia en el registro | Interpretación | Cómo resolverla |
|---|---|---|
| `AssertionError` y comparación entre resultado esperado y obtenido | La implementación incumple al menos uno de los ejemplos definidos por las pruebas. | Reproducir el caso localmente y revisar la función implicada. |
| Una entrada inválida no produce `TypeError` | Se debilitó la validación del contrato. | Restaurar la comprobación de tipos, sin convertir entradas automáticamente. |
| Error al instalar el paquete o importar `text_utils` | No se alcanzó una ejecución válida de toda la suite. | Revisar `pyproject.toml`, el intérprete activo y la instalación del paquete. |
| Error de descarga, preparación del runner o tiempo agotado | La infraestructura o la preparación impidió completar la verificación. | Examinar ese paso y repetir cuando su causa esté resuelta. |
| No aparece `unit-tests` | No existe todavía un resultado que permita evaluar la propuesta. | Revisar la ruta del workflow, su sintaxis, el evento y la rama de destino. |

Una ejecución correcta de este workflow debe mostrar `64 passed` y salida
cero de pytest. Eso demuestra que los casos incluidos se cumplieron en ese
entorno; no demuestra que se hayan cubierto todas las cadenas Unicode posibles.
Una salida distinta de cero debe detener el job. Revisa el registro antes de
atribuir la causa al programa, porque una falla de instalación no equivale a
una aserción fallida.

La resolución de un defecto debe conservar las pruebas que lo detectaron.
Después de corregir la función y repetir la suite local, publicar la
actualización en la misma rama del PR provoca una nueva verificación. Compara
el caso que fallaba con su resultado corregido para explicar por qué la
solución funciona.
