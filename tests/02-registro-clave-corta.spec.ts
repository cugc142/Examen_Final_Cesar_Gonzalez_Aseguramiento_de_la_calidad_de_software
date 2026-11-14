import { test, expect } from '@playwright/test';
import { account, register } from '../helpers/account';

test('CP-02 | HU-1 C2 | Rechazar clave de siete caracteres', async ({ page }) => {
  await register(page, { ...account(), login: `${account().login}_corta`, password: 'Qa12!xy' });
  await expect(page.getByRole('button', { name: 'Register', exact: true })).toBeEnabled();
  await expect(page.getByText('Registration is successful')).not.toBeVisible();
  await expect(page.getByText(/Password.*(short|length|long enough)|minimum.*8/i)).toBeVisible();
});
