import { test, expect } from '@playwright/test';
import { account, register } from '../helpers/account';
import fs from 'node:fs';

test('CP-01 | HU-1 C1 C2 | Registro con datos válidos', async ({ page }) => {
  const marker = 'playwright/.auth/registered.json';
  test.skip(fs.existsSync(marker), 'La cuenta ya fue registrada; no crear usuarios innecesarios. Para otra ejecución use una cuenta nueva conscientemente.');
  await register(page, account());
  await expect(page.getByText('Registration is successful')).toBeVisible();
  fs.writeFileSync(marker, JSON.stringify({ login: account().login, at: new Date().toISOString() }));
});
