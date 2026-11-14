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

Se usaron las plantillas originales `Plantilla - Casos de prueba (EJEMPLO).xlsx` y `Plantilla de reporte de errores (EJEMPLO).docx` encontradas en Descargas. Los ejemplos se reemplazaron por resultados reales y los requisitos del examen (mínimo ocho caracteres).

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
