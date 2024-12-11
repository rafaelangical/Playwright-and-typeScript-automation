FROM mcr.microsoft.com/playwright:v1.39.0-focal

# Definir o diretório de trabalho
WORKDIR /usr/src/app

# Copiar arquivos do projeto
COPY package.json . 
RUN npm install
COPY src/ ./src/

# Comando para rodar o Playwright
CMD ["npx", "playwright", "test"]
