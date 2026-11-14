"""Genera entregables a partir de las plantillas del examen y resultados observados.
Preparación: python -m pip install --target .tools/python python-docx openpyxl
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.tools/python'))
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from docx import Document
from docx.shared import Inches

ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS = Path.home() / 'Downloads'
OUT = ROOT / 'docs'

def workbook():
    book = load_workbook(DOWNLOADS / 'Plantilla - Casos de prueba (EJEMPLO).xlsx')
    sheet = book.active
    sheet['A1'] = 'SUITE DE PRUEBAS - BUGGY CARS RATING · 14/11/2026'
    sheet['A2'] = 'ID'
    for row in [4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26]:
        for col in range(1, 10): sheet.cell(row, col).value = None
    cases = [
      (4, ['CP-01', 'HU-1 C1 C2 · Registro válido (automatizado)', 'Alta', 'Login único no registrado; sitio disponible.',
       'Login: qa_cesar_1794674654703; First Name: Cesar; Last Name: QA; clave de 19 caracteres con mayúsculas, minúsculas, números y !; confirmación igual. Clave local excluida de Git.',
       '1. Abrir /register.\n2. Completar los cinco campos.\n3. Pulsar Register.\n4. Verificar confirmación.',
       'El sitio crea la cuenta y muestra Registration is successful.',
       'Registration is successful. Ejecución real en Chromium el 14/11/2026. Evidencia: evidencias/automaticos/CP-01.png; ejecucion-inicial/resultados.json.', 'OK']),
      (5, ['CP-02', 'HU-1 C2 · Clave de 7 caracteres (automatizado)', 'Alta', 'Login de intento no registrado. No usar la cuenta válida como login de este intento.',
       'Login de la cuenta + _corta; Cesar; QA; Password y Confirm Password: Qa12!xy (7 caracteres).',
       '1. Abrir /register.\n2. Completar campos con clave de 7 caracteres.\n3. Pulsar Register.\n4. Esperar respuesta y comprobar rechazo.',
       'Registro rechazado por longitud inferior a 8; no muestra confirmación de registro.',
       'Rechazado: InvalidPasswordException: Password did not conform with policy: Password not long enough. CP-02 pasa; mensaje técnico registrado aparte como BUG-002 (HU-1 C4). Evidencia CP-02.png y CP-02-resultados.json.', 'OK']),
      (12, ['CP-04', 'HU-2 C1 · Actualizar perfil (manual)', 'Media', 'Usuario registrado y autenticado; acceder a Profile.',
       'Cesar; QA; Male; 25; Ciudad de Guatemala; 55551234; Learning.',
       '1. Completar los siete campos.\n2. Capturar.\n3. Save y capturar confirmación.\n4. Salir y volver a Profile.\n5. Comparar los siete valores y capturar.',
       'Guardado confirmado; todos los valores se conservan al reingresar.',
       'Verificación asistida: OK, siete valores persistieron. Capturas CP-04-01/02/03 en evidencias/manuales. NO acredita ejecución manual humana; pendiente ejecutarla con npm run manual y actualizar esta fila.', 'PENDIENTE MANUAL']),
      (13, ['CP-05', 'HU-2 C3 · Edad con letras (manual)', 'Media', 'Cuenta autenticada; perfil con edad válida 25 guardada.',
       'Age: abc. Otros campos válidos, sin cambios.',
       '1. Abrir Profile.\n2. Cambiar Age a abc y capturar.\n3. Save y capturar respuesta.\n4. Salir y volver.\n5. Verificar que abc no persistió; capturar.',
       'Rechaza la edad con letras y conserva la edad válida previamente guardada.',
       'Verificación asistida: OK para HU-2 C3. Respuesta Unknown error; al volver Age = 25. Capturas CP-05-01/02/03. Pendiente ejecución manual humana; mensaje poco informativo como observación.', 'PENDIENTE MANUAL']),
      (18, ['CP-03', 'HU-3 C1 C2 C4 · Voto con comentario (automatizado)', 'Alta', 'Cuenta registrada sin voto previo en el primer auto de Overall Rating. Sitio compartido; no repetir voto.',
       'Primer auto observado: Lamborghini Diablo. Comentario único: Prueba académica QA 1794674778390: diseño del auto interesante.',
       '1. Abrir Overall Rating y primer auto sin sesión; verificar restricción.\n2. Login.\n3. Reabrir auto y leer votos.\n4. Comentar y Vote!.\n5. Verificar confirmación, incremento, comentario, fecha y autor.\n6. Recargar y comprobar que no puede repetir voto.',
       'Sin sesión no permite votar. Con sesión confirma, suma exactamente 1 y muestra comentario con fecha y autor; no permite otro voto del mismo usuario.',
       'FALLO BUG-001: contador 11043 → 11044 y confirmación correctos; comentario y fecha visibles, autor vacío. Reingreso posterior confirma voto existente sin botón Vote!. Trace y captura en evidencias/automaticos. No se repitió el voto.', 'FALLO']),
    ]
    for row, values in cases:
        sheet.row_dimensions[row].height = 205
        for col, value in enumerate(values, 1):
            cell = sheet.cell(row, col, value)
            cell.alignment = Alignment(wrap_text=True, vertical='top')
    sheet.column_dimensions['A'].width = 10
    for c in ['B', 'D', 'E', 'F', 'G', 'H']: sheet.column_dimensions[c].width = 38
    sheet.column_dimensions['I'].width = 22
    sheet['A25'] = 'OBSERVACIONES DE EJECUCIÓN'
    sheet['B26'] = 'Fecha 14/11/2026 · Windows · Chromium 149.0.7827.55 · Playwright 1.61.1. CP-04 y CP-05 requieren ejecución manual por el estudiante. Resultados automatizados consolidados de ejecuciones separadas para no crear cuentas ni votar otra vez. Fallos iniciales de selectores corregidos; BUG-001 se mantiene.'
    sheet['B26'].alignment = Alignment(wrap_text=True, vertical='top')
    sheet.row_dimensions[26].height = 180
    for validation in sheet.data_validations.dataValidation:
        validation.formula1 = '"OK,FALLO,PENDIENTE MANUAL"'
    sheet.print_options.horizontalCentered = True
    sheet.print_area = 'A1:I26'
    sheet.page_setup.orientation = 'landscape'
    sheet.page_setup.paperSize = sheet.PAPERSIZE_A3
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    book.save(OUT / 'Casos-de-prueba.xlsx')

def bug(number, title, description, steps, expected, actual, evidence, image):
    doc = Document(DOWNLOADS / 'Plantilla de reporte de errores (EJEMPLO).docx')
    values = [number, 'Cesar · ejecución asistida por Codex', title, '14/11/2026', 'Windows (versión no verificada)', 'Chromium 149.0.7827.55 · Playwright 1.61.1', 'Media', 'Sin asignar']
    for row, value in zip(doc.tables[0].rows, values): row.cells[1].text = value
    replacements = {0: 'REPORTE DE ERROR · BUGGY CARS RATING', 3: description, 5: steps[0], 6: steps[1], 7: steps[2], 9: expected, 11: actual, 13: evidence, 17: 'Captura real de la ejecución del 14/11/2026.'}
    for i, text in replacements.items(): doc.paragraphs[i].text = text
    for i in [14, 15, 16]: doc.paragraphs[i].clear()
    doc.paragraphs[14].add_run().add_picture(str(ROOT / image), width=Inches(6))
    doc.add_paragraph('Estado: abierto. La prueba conserva el resultado obtenido. No se ha aplicado corrección en el sitio externo.')
    doc.save(OUT / 'bugs' / f'{number}.docx')

if __name__ == '__main__':
    workbook()
    bug('BUG-001', 'El comentario de un voto se muestra sin autor',
        'HU-3 C4 exige que el comentario aparezca con fecha y autor. En CP-03 el usuario estaba autenticado y el perfil contenía nombre Cesar y apellido QA. Tras votar, la columna Author quedó vacía.',
        ['1. Iniciar sesión con una cuenta registrada sin voto previo; abrir Overall Rating y el primer auto (Lamborghini Diablo en esta ejecución).',
         '2. Anotar el contador, escribir un comentario único y pulsar Vote! una sola vez.',
         '3. Revisar la confirmación, el contador y la fila del comentario; comprobar la columna Author.'],
        'Confirma el voto, incrementa el contador en 1 y muestra el comentario con su fecha y el autor de la cuenta autenticada.',
        'Se confirmó el voto y el contador pasó de 11043 a 11044. El comentario Prueba académica QA 1794674778390: diseño del auto interesante. se mostró con fecha Nov 14, 2026, 10:46:23 AM; la celda Author estaba vacía. CP-03 falla al exigir Cesar. Al reingresar se conserva el voto y no hay botón para repetirlo. La fecha se transcribe como la muestra el sitio.',
        'evidencias/automaticos/CP-03-autor-ausente.png; ejecucion-voto/trace.zip; ejecucion-voto/resultados.json; CP-03-observado.json. Reproducir en otra cuenta solo si es necesario, sin repetir votos.',
        'evidencias/automaticos/CP-03-autor-ausente.png')
    bug('BUG-002', 'El rechazo de clave corta expone una excepción técnica',
        'HU-1 C4 requiere errores comprensibles para el usuario final. La clave de siete caracteres se rechaza correctamente según C2, pero el mensaje expone el identificador técnico InvalidPasswordException y no indica el mínimo de ocho caracteres. Este defecto de claridad no cambia el resultado OK de CP-02 para C2.',
        ['1. Abrir https://buggy.justtestit.org/register y usar un login de prueba único no registrado; completar nombre y apellido.',
         '2. Introducir Qa12!xy en Password y Confirm Password: siete caracteres con mayúscula, minúscula, número y carácter especial.',
         '3. Pulsar Register y leer el mensaje de rechazo.'],
        'Rechaza el registro y muestra un mensaje comprensible, por ejemplo: Password must contain at least 8 characters.',
        'Muestra InvalidPasswordException: Password did not conform with policy: Password not long enough. El rechazo es correcto; el texto expone una excepción interna y omite la longitud mínima requerida.',
        'evidencias/automaticos/CP-02.png y CP-02-resultados.json. No usar el texto de ejemplo de la plantilla (mínimo 6); el examen exige mínimo 8.',
        'evidencias/automaticos/CP-02.png')
    print('Excel y dos reportes Word generados a partir de las plantillas originales.')
