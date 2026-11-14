import { expect, Page } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';

const file = path.resolve('playwright/.auth/account.json');
export type Account = { login: string; password: string; firstName: string; lastName: string };
export function account(): Account {
  if (fs.existsSync(file)) return JSON.parse(fs.readFileSync(file, 'utf8'));
  const value = { login: `qa_cesar_${Date.now()}`, password: 'QaExamen2026!Seguro', firstName: 'Cesar', lastName: 'QA' };
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(value, null, 2));
  return value;
}
export async function register(page: Page, user: Account) {
  await page.goto('/register');
  await page.locator('#username').fill(user.login);
  await page.locator('#firstName').fill(user.firstName);
  await page.locator('#lastName').fill(user.lastName);
  await page.locator('#password').fill(user.password);
  await page.locator('#confirmPassword').fill(user.password);
  await page.getByRole('button', { name: 'Register', exact: true }).click();
}
export async function login(page: Page, user = account()) {
  await page.goto('/');
  await page.locator('input[name="login"]').fill(user.login);
  await page.locator('input[name="password"]').fill(user.password);
  await page.getByRole('button', { name: 'Login', exact: true }).click();
  await expect(page.getByRole('link', { name: 'Profile', exact: true })).toBeVisible();
}
