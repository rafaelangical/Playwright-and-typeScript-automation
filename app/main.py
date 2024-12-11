from flask import Flask, jsonify
import sqlite3
import requests
import pandas as pd
import os

DB_PATH = "health_data.db"

app = Flask(__name__)

# API externa para dados de mortes de covid
COVID_API = "https://api.brasil.io/v1/dataset/covid19/obito_cartorio/data/"
DENGUE_API = "https://api.brasil.io/v1/dataset/dengue/caso_municipal/data/"

API_TOKEN = "f291a3123f7087d00a41dc020ba5efe3f656e87f" 

HEADERS = {
    "Authorization": f"Token {API_TOKEN}"
}

COVID_DATA_TABLE = "covid_data_table"
DENGUE_DATA_TABLE = "dengue_data_table"

def save_to_database(data, table_name, db_name="health_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Criar tabela específica, se não existir
    if table_name == COVID_DATA_TABLE:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS covid_data_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT,
                cases TEXT
            )
        """)
    elif table_name == DENGUE_DATA_TABLE:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dengue_data_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year TEXT,
                cases TEXT
            )
        """)

    # Inserir os dados
    for record in data:
        if table_name == COVID_DATA_TABLE:
            cursor.execute("""
                INSERT INTO covid_data_table (year, cases)
                VALUES (?, ?)
            """, (
                record.get("year"),
                record.get("cases"),
            ))
        elif table_name == DENGUE_DATA_TABLE:
            cursor.execute("""
                INSERT INTO dengue_data_table (year, cases)
                VALUES (?, ?)
            """, (
                record.get("year"),
                record.get("cases"),
            ))

    conn.commit()
    conn.close()


# Função para persistir dados
# def save_to_db(data, table):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     for item in data:
#         cursor.execute(f"""
#             INSERT INTO {table} (year, cases)
#             VALUES (?, ?)
#         """, (item["year"], item["cases"]))
#     conn.commit()
#     conn.close()

# Função para carregar dados das APIs
def load_data():
    try:
        # COVID-19
        response_covid = requests.get(COVID_API, headers=HEADERS).json()
        parsed_response = [{"year": item["date"], "cases": item["deaths_covid19"]} for item in response_covid["results"]]
        save_to_database(parsed_response, COVID_DATA_TABLE)
        
        print(response_covid)
        print(parsed_response)
        
        # Dengue
        # response_dengue = requests.get(DENGUE_API, params={"state": "SP", "city": "São Paulo"}).json()
        # dengue_data = [{"year": item["year"], "cases": item["cases"]} for item in response_dengue["results"]]
        # save_to_db(dengue_data, DENGUE_DATA_TABLE)
        
        print("Dados carregados com sucesso!")
        
    except Exception as e:
        print(e)
        print(f"Erro ao carregar dados: {e}")

# Função para consultar dados do banco SQLite
def get_covid_data():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM covid_data_table"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_dengue_data():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM dengue_data_table"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Rota para carregar dados
# @app.route('/load_data', methods=['GET'])
# def load_data_route():
#     load_data()
#     return jsonify({"status": "Dados carregados com sucesso!"}), 200

# Rota para retornar dados persistidos
@app.route('/', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Consultar dados de COVID
    cursor.execute("SELECT * FROM covid_data_table")
    covid_data = cursor.fetchall()

    # Consultar dados de Dengue
    cursor.execute("SELECT * FROM dengue_data_table")
    dengue_data = cursor.fetchall()

    conn.close()
    
    return jsonify({"covid_data": covid_data, "dengue_data": dengue_data})

# Rodar a função de carregamento de dados automaticamente no início
if __name__ == '__main__':
    # init_db()  # Inicializa o banco de dados
    load_data()  # Carrega os dados ao iniciar a aplicação
    app.run(host="0.0.0.0", port=5005)
