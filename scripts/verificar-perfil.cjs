// Verificación asistida por navegador; no equivale a ejecución manual por una persona.
const { chromium, expect } = require('@playwright/test');
const fs = require('node:fs');
const user = require('../playwright/.auth/account.json');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 1000 } });
  const results = { date: new Date().toISOString(), method: 'Verificación asistida con Playwright; pendiente ejecución manual por el estudiante', browser: browser.version() };
  try {
    await page.goto('https://buggy.justtestit.org/');
    await page.locator('[name=login]').fill(user.login);
    await page.locator('input[name=password]').fill(user.password);
    await page.getByRole('button', { name: 'Login', exact: true }).click();
    await page.getByRole('link', { name: 'Profile', exact: true }).click();
    await expect(page.locator('#firstName')).toHaveValue(user.firstName);
    const values = { firstName: 'Cesar', lastName: 'QA', gender: 'Male', age: '25', address: 'Ciudad de Guatemala', phone: '55551234', hobby: 'Learning' };
    for (const [id, value] of Object.entries(values)) {
      if (id === 'hobby') await page.locator('#hobby').selectOption({ label: value });
      else await page.locator('#' + id).fill(value);
    }
    await page.screenshot({ path: 'evidencias/manuales/CP-04-01-datos-validos.png', fullPage: true });
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    await expect(page.locator('.result.alert-success:visible').first()).toBeVisible();
    await page.screenshot({ path: 'evidencias/manuales/CP-04-02-guardado.png', fullPage: true });
    await page.getByRole('link', { name: 'Buggy Rating', exact: true }).click();
    await page.getByRole('link', { name: 'Profile', exact: true }).click();
    for (const [id, value] of Object.entries(values)) await expect(page.locator('#' + id)).toHaveValue(value);
    results.CP04 = { status: 'OK en verificación asistida', values };
    await page.screenshot({ path: 'evidencias/manuales/CP-04-03-persistencia.png', fullPage: true });
    await page.locator('#age').fill('abc');
    await page.screenshot({ path: 'evidencias/manuales/CP-05-01-edad-letras.png', fullPage: true });
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    await expect(page.locator('.result:visible').first()).toBeVisible();
    const message = await page.locator('.result:visible').first().innerText();
    await page.screenshot({ path: 'evidencias/manuales/CP-05-02-guardado.png', fullPage: true });
    await page.getByRole('link', { name: 'Buggy Rating', exact: true }).click();
    await page.getByRole('link', { name: 'Profile', exact: true }).click();
    await expect(page.locator('#age')).toHaveValue('25');
    results.CP05 = { status: 'OK en verificaci?n asistida: edad con letras rechazada', message, ageAfterReentry: await page.locator('#age').inputValue(), observation: 'Unknown error no explica el formato v?lido.' };
    await page.screenshot({ path: 'evidencias/manuales/CP-05-03-persistencia.png', fullPage: true });
    await page.locator('#age').fill('25');
    await page.getByRole('button', { name: 'Save', exact: true }).click();
    await expect(page.locator('.result.alert-success:visible').first()).toBeVisible();
  } catch (e) {
    results.error = String(e);
    await page.screenshot({ path: 'evidencias/manuales/error-verificacion.png', fullPage: true });
    process.exitCode = 1;
  } finally {
    fs.writeFileSync('evidencias/manuales/verificacion-asistida.json', JSON.stringify(results, null, 2));
    console.log(JSON.stringify(results, null, 2));
    await browser.close();
  }
})();

