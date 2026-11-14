import { test, expect } from '@playwright/test';

test('Chromium muestra una página de prueba', async ({ page }) => {
  await page.setContent('<h1>Playwright listo</h1>');
  await expect(page.getByRole('heading', { name: 'Playwright listo' })).toBeVisible();
});