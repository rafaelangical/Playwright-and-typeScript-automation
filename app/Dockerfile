# FROM python:3.9-slim

FROM python:3.9-slim

# Instalar dependências
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Definir o diretório de trabalho
WORKDIR /app
COPY . .

# Expor a porta do Flask e do Streamlit
EXPOSE 5005
EXPOSE 8501

# Rodar o servidor Flask

CMD ["python", "main.py"]

# CMD ["streamlit", "run", "streamlit_app.py"]
CMD ["python", "main.py"]
