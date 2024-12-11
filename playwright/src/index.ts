import { chromium } from "playwright";

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  console.log("Acessando dados da API...");

  // Navegar até a API do Flask
  await page.goto("http://app:5005/"); // O container Flask é acessado via 'app' no Docker Compose

  // Imprimir os dados recebidos
  const content = await page.textContent("body");
  console.log("Dados recebidos:", content);

  await browser.close();
})();
