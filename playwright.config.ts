import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  outputDir: './test-results',
  workers: 1,
  retries: 0,
  timeout: 60000,
  expect: { timeout: 15000 },
  reporter: [['list'], ['html', { open: 'never' }], ['json', { outputFile: 'evidencias/automaticos/resultados.json' }]],
  use: {
    baseURL: 'https://buggy.justtestit.org/',
    browserName: 'chromium',
    screenshot: 'on',
    video: 'on',
    trace: 'on',
  },
});
