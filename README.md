# Examen final QA · Buggy Cars Rating

Pruebas de https://buggy.justtestit.org/ basadas en **Examen final QA.docx**, Serie 3: tres casos automatizados con Playwright y dos casos definidos para ejecución manual.

## Resultados del 14/11/2026

Entorno: Windows (versión no verificada), **Chromium 149.0.7827.55**, Playwright 1.61.1 y Node.js 24.17.0.

| Caso | Requisitos | Resultado real |
|---|---|---|
| CP-01 Registro válido | HU-1 C1 C2 | OK: registro confirmado |
| CP-02 Clave de siete caracteres | HU-1 C2 | OK: registro rechazado |
| CP-03 Voto con comentario | HU-3 C1 C2 C4 | FALLO: comentario sin autor, BUG-001 |
| CP-04 Actualizar perfil | HU-2 C1 | Pendiente manual; verificación asistida OK |
| CP-05 Edad con letras | HU-2 C3 | Pendiente manual; verificación asistida OK |

El contador pasó de 11043 a 11044 y el voto fue confirmado. El comentario tenía fecha, pero el autor estaba vacío. Se conserva el fallo conforme al enunciado. Una comprobación posterior confirmó que ya no aparece el botón para repetir el voto.

Las capturas de CP-04 y CP-05 se obtuvieron mediante un script de verificación asistida. Para completar el requisito **manual**, el estudiante debe ejecutar los pasos personalmente, guardar sus capturas y actualizar el Excel. Al guardar edad `abc` apareció `Unknown error`; al volver al perfil se conservó la edad válida 25.

## Descripción de las pruebas realizadas

### CP-01 · Registro de usuario con datos válidos

**Objetivo:** comprobar el registro solicitado por HU-1, criterios C1 y C2. Automatizamos el ingreso de un login único, nombre Cesar, apellido QA y una clave de 19 caracteres con mayúsculas, minúsculas, números y un carácter especial. Repetimos la clave en su confirmación y pulsamos Register.

**Esperado y obtenido:** el sitio debía crear la cuenta y confirmar el registro. Mostró `Registration is successful`, por lo que el caso pasó. La cuenta creada se reutilizó en las pruebas de voto y perfil para evitar registros innecesarios.

**Evidencia:** [captura del registro](evidencias/automaticos/CP-01.png). Implementación: [01-registro-valido.spec.ts](tests/01-registro-valido.spec.ts).

### CP-02 · Registro con clave de siete caracteres

**Objetivo:** verificar el mínimo de ocho caracteres de HU-1 C2. Completamos el registro con un login diferente y la clave `Qa12!xy`, que tiene siete caracteres e incluye mayúscula, minúsculas, números y un carácter especial. Pulsamos Register y comprobamos la respuesta.

**Esperado y obtenido:** el registro debía rechazarse por longitud insuficiente. El sitio lo rechazó con `InvalidPasswordException: Password did not conform with policy: Password not long enough`. El caso pasó para C2. Documentamos por separado el mensaje técnico como **BUG-002**, relacionado con la claridad de errores de HU-1 C4.

**Evidencia:** [captura del rechazo](evidencias/automaticos/CP-02.png). Implementación: [02-registro-clave-corta.spec.ts](tests/02-registro-clave-corta.spec.ts).

### CP-03 · Votar por el primer auto con un comentario

**Objetivo:** verificar HU-3 C1, C2 y C4. Abrimos Overall Rating y el primer auto, Lamborghini Diablo en esa ejecución. Sin sesión, comprobamos el mensaje `You need to be logged in to vote.`. Después iniciamos sesión con la cuenta registrada, anotamos el contador y emitimos un solo voto con un comentario único.

**Esperado:** confirmación del voto, incremento de exactamente uno y publicación del comentario con fecha y autor. La misma cuenta no debía poder votar otra vez por ese auto.

**Obtenido:** apareció `Thank you for your vote!` y el contador cambió de **11043 a 11044**. El comentario se publicó con fecha, pero la columna Author quedó vacía. Por ello el caso falló y se reportó **BUG-001**. En una comprobación posterior, sin emitir otro voto, confirmamos que el voto seguía registrado y ya no aparecía el botón Vote!.

**Evidencia:** [comentario sin autor](evidencias/automaticos/CP-03-autor-ausente.png) y [comprobación al reingresar](evidencias/automaticos/CP-03-reingreso.png). Implementación: [03-voto-con-comentario.spec.ts](tests/03-voto-con-comentario.spec.ts).

### CP-04 · Actualizar el perfil con datos válidos

**Objetivo:** verificar que los datos de HU-2 C1 se conservan. Mediante verificación asistida abrimos Profile e ingresamos nombre Cesar, apellido QA, género Male, edad 25, dirección Ciudad de Guatemala, teléfono 55551234 y hobby Learning. Guardamos, salimos del perfil y volvimos a entrar para comparar los siete campos.

**Esperado y obtenido:** debía confirmarse el guardado y recuperarse todos los valores. La verificación asistida confirmó ambos comportamientos. **La ejecución manual por el estudiante sigue pendiente**; este resultado no se presenta como una prueba realizada manualmente.

**Evidencia:** [datos ingresados](evidencias/manuales/CP-04-01-datos-validos.png), [guardado](evidencias/manuales/CP-04-02-guardado.png) y [persistencia](evidencias/manuales/CP-04-03-persistencia.png).

### CP-05 · Intentar guardar una edad con letras

**Objetivo:** comprobar que la edad solo admite números según HU-2 C3. Con la edad válida 25 previamente guardada, cambiamos Age a `abc`, conservamos los demás datos válidos y pulsamos Save. Después salimos del perfil y volvimos a entrar.

**Esperado y obtenido:** el sistema debía rechazar la edad con letras y conservar el valor válido anterior. Mostró `Unknown error`; al reabrir el perfil, Age seguía siendo 25. La verificación asistida pasó para C3, con la observación de que el mensaje no explica el formato permitido. **La ejecución manual por el estudiante sigue pendiente.**

**Evidencia:** [edad con letras](evidencias/manuales/CP-05-01-edad-letras.png), [respuesta al guardar](evidencias/manuales/CP-05-02-guardado.png) y [edad conservada](evidencias/manuales/CP-05-03-persistencia.png).

## Instalación y ejecución

En PowerShell, desde esta carpeta:

```powershell
node --version
npm.cmd ci
npx.cmd playwright install chromium
npx.cmd playwright test --list
npm.cmd test
npm.cmd run report
```

Se usa Chromium headless, un worker y cero reintentos para evitar repetir operaciones en el sitio compartido. Cada prueba dispone de 60 segundos y las aserciones de 15 segundos. Los fallos devuelven código de salida distinto de cero.

El registro genera un login único y conserva la cuenta local en `playwright/.auth/account.json`. CP-03 reutiliza esa cuenta. Para ejecutar el voto individualmente primero debe haberse ejecutado CP-01.

```powershell
npx.cmd playwright test tests/01-registro-valido.spec.ts
npx.cmd playwright test tests/02-registro-clave-corta.spec.ts
npx.cmd playwright test tests/03-voto-con-comentario.spec.ts
```

CP-01 se omite si la cuenta ya fue registrada y CP-03 se omite si esa cuenta ya votó por el primer auto. **Omitido no significa aprobado.** Los resultados de la entrega provienen de las ejecuciones conservadas. No borres los archivos locales para forzar nuevas cuentas o votos sin necesidad.

El primer auto depende del orden actual de Overall Rating. Un voto simultáneo de otra persona podría afectar la comprobación exacta de +1; en esta ejecución se observó exactamente +1.

## Casos manuales

Lee [los pasos y resultados esperados](docs/casos-manuales.md) y ejecuta:

```powershell
npm.cmd run manual
```

Este comando abre Chromium con la cuenta existente. Tú realizas las acciones y verificas los resultados; la terminal permite capturar cada paso pulsando Enter. Las capturas y tus observaciones quedan en `evidencias/manuales/ejecucion-personal/`. Actualiza las filas CP-04 y CP-05 del Excel con tu resultado, nombre y fecha.

La verificación asistida se repite con `node scripts/verificar-perfil.cjs`; no sustituye la ejecución manual.

## Entregables

```text
tests/                         Tres pruebas automatizadas
helpers/account.ts             Cuenta única, registro y acceso
docs/Casos-de-prueba.xlsx       Cinco casos en la plantilla Excel original
docs/bugs/BUG-001.docx          Comentario sin autor (HU-3 C4)
docs/bugs/BUG-002.docx          Error técnico de clave corta (HU-1 C4)
docs/casos-manuales.md          Pasos para la ejecución manual
evidencias/automaticos/         Capturas, resultados JSON y video del voto
evidencias/manuales/            Capturas de verificación asistida
scripts/                       Captura manual y generación de documentos
playwright.config.ts           Configuración e informes
```

Se completaron las plantillas indicadas por el usuario: `Plantilla - Casos de prueba (EJEMPLO) (1).xlsx` y `Plantilla de reporte de errores (EJEMPLO) (2).docx`, ubicadas en Descargas. Se conserva su estructura y los ejemplos se reemplazaron por resultados reales y los requisitos del examen (mínimo ocho caracteres). Los originales de Descargas permanecen sin cambios; las versiones completadas están en el proyecto:

- [Tabla Excel con los cinco casos](docs/Casos-de-prueba.xlsx).
- [Reporte Word BUG-001: comentario sin autor](docs/bugs/BUG-001.docx).
- [Reporte Word BUG-002: mensaje técnico de clave corta](docs/bugs/BUG-002.docx).

Los JSON de `ejecucion-inicial/` y `ejecucion-voto/` conservan el historial, incluidos fallos de selectores de las primeras versiones. Esos errores del código de prueba fueron corregidos. CP-02 se volvió a ejecutar y pasó; su resultado definitivo está en `CP-02-resultados.json`. CP-03 no volvió a emitir un voto: el fallo del autor está respaldado por captura, video y `CP-03-observado.json`. El código actual usa una aserción suave para comprobar también la restricción del segundo voto aunque falte el autor.

Consulta `evidencias/automaticos/resumen-entrega.json` para el resultado consolidado. El reporte HTML corresponde a la última ejecución, que fue solo CP-02.

`.gitignore` excluye `node_modules`, `test-results`, informes temporales, credenciales y trazas con sesiones. El trace original del voto permanece local en `evidencias/automaticos/ejecucion-voto/trace.zip`; se excluye de Git porque puede contener datos de sesión. Las capturas, video y resultados JSON sí forman parte de la entrega.

`diagnostico.spec.ts` en la raíz es una comprobación previa y queda fuera de la suite configurada en `tests/`.

## GitHub

Git local está inicializado; falta configurar el remoto y subir los archivos. Tras completar los casos manuales, crea un repositorio vacío en GitHub y reemplaza la URL por la tuya:

```powershell
git add .
git commit -m "Entrega examen final QA Buggy Cars"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git push -u origin main
```

Verifica que el Excel, ambos Word y las capturas aparezcan en GitHub. Todavía no se ha publicado ni se declara finalizada la entrega manual.
