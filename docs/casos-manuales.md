# Ejecución manual pendiente

Las capturas actuales son reales, pero se obtuvieron mediante verificación asistida con Playwright. No acreditan ejecución manual por el estudiante. Ambos escenarios dieron OK en esa verificación; debes ejecutarlos personalmente y registrar fecha, resultado y capturas en el Excel.

## Preparación

Usa Chromium. Para abrirlo con la cuenta del proyecto ejecuta `npm.cmd run manual` y sigue las instrucciones de la terminal. Las credenciales se conservan localmente en `playwright/.auth/account.json` y no se suben a GitHub.

## CP-04 · HU-2 C1 · Actualizar perfil

1. Inicia sesión y entra en Profile.
2. Introduce First Name: Cesar, Last Name: QA, Gender: Male, Age: 25, Address: Ciudad de Guatemala, Phone: 55551234 y Hobby: Learning.
3. Captura los datos antes de guardar.
4. Pulsa Save. Verifica el mensaje de confirmación y captura la pantalla.
5. Sal del perfil con Buggy Rating y vuelve a Profile. Verifica los siete valores y captura su persistencia.

Esperado: confirmación de guardado y conservación de todos los datos. La verificación asistida obtuvo este resultado.

## CP-05 · HU-2 C3 · Edad con letras

1. Con la edad válida 25 previamente guardada, entra en Profile.
2. Cambia Age a `abc`; conserva los demás datos válidos. Captura la pantalla.
3. Pulsa Save y captura la respuesta.
4. Sal del perfil y vuelve a entrar. Captura el valor recuperado.
5. Comprueba que la edad inválida no quedó guardada; conserva/restaura 25.

Esperado: rechazo de la edad con letras y conservación de la edad válida. En la verificación asistida apareció `Unknown error` y al reingresar la edad seguía siendo 25. El criterio HU-2 C3 se cumple; el mensaje es poco informativo.

Guarda tus capturas en `evidencias/manuales/ejecucion-personal/`, cambia el estado PENDIENTE MANUAL del Excel por OK o FALLO según lo observado y añade tu nombre y fecha. No reemplaces resultados con suposiciones.
