import browser from 'webextension-polyfill';

// Initialize settings
document.addEventListener('DOMContentLoaded', async () => {
  const temperatureInput = document.getElementById(
    'temperature',
  ) as HTMLInputElement;
  const maxTokensInput = document.getElementById(
    'maxTokens',
  ) as HTMLInputElement;
  const temperatureValue = temperatureInput.nextElementSibling as HTMLElement;
  const maxTokensValue = maxTokensInput.nextElementSibling as HTMLElement;

  // Load saved settings
  const settings = await browser.storage.local.get({
    temperature: 0.6,
    maxTokens: 20,
  });

  temperatureInput.value = settings.temperature.toString();
  maxTokensInput.value = settings.maxTokens.toString();
  temperatureValue.textContent = settings.temperature.toString();
  maxTokensValue.textContent = settings.maxTokens.toString();

  // Update settings on change
  temperatureInput.addEventListener('input', async () => {
    const value = parseFloat(temperatureInput.value);
    temperatureValue.textContent = value.toString();
    await browser.storage.local.set({ temperature: value });
  });

  maxTokensInput.addEventListener('input', async () => {
    const value = parseInt(maxTokensInput.value, 10);
    maxTokensValue.textContent = value.toString();
    await browser.storage.local.set({ maxTokens: value });
  });
});
