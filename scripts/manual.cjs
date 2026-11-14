const { chromium } = require('playwright');
const fs = require('node:fs');
const readline = require('node:readline/promises');
const path = require('node:path');
(async () => {
  const user = require('../playwright/.auth/account.json');
  const browser = await chromium.launch({ headless: false });
  const terminal = readline.createInterface({ input: process.stdin, output: process.stdout });
  try {
    const page = await browser.newPage({ viewport: { width: 1366, height: 1000 } });
    await page.goto('https://buggy.justtestit.org/');
    await page.locator('[name=login]').fill(user.login);
    await page.locator('input[name=password]').fill(user.password);
    await page.getByRole('button', { name: 'Login', exact: true }).click();
    await page.getByRole('link', { name: 'Profile', exact: true }).click();
    const dir = 'evidencias/manuales/ejecucion-personal';
    fs.mkdirSync(dir, { recursive: true });
    const steps = [
      ['CP-04-01', 'Completa los siete datos de CP-04 según docs/casos-manuales.md, sin guardar.'],
      ['CP-04-02', 'Pulsa Save y revisa la confirmación.'],
      ['CP-04-03', 'Sal y vuelve a Profile; verifica los siete valores.'],
      ['CP-05-01', 'Cambia Age a abc, sin guardar.'],
      ['CP-05-02', 'Pulsa Save y revisa la respuesta.'],
      ['CP-05-03', 'Sal y vuelve al perfil; comprueba la edad recuperada.'],
    ];
    for (const [id, instruction] of steps) {
      await terminal.question(`${id}: ${instruction} Pulsa Enter aquí para capturar. `);
      await page.screenshot({ path: path.join(dir, `${id}.png`), fullPage: true });
    }
    const tester = await terminal.question('Tu nombre: ');
    const cp04 = await terminal.question('CP-04: resultado y observaciones reales: ');
    const cp05 = await terminal.question('CP-05: resultado y observaciones reales: ');
    fs.writeFileSync(path.join(dir, 'resultados.json'), JSON.stringify({ tester, date: new Date().toISOString(), cp04, cp05 }, null, 2));
    console.log('Capturas guardadas. Actualiza la tabla Excel con estos resultados.');
  } finally { terminal.close(); await browser.close(); }
})();
