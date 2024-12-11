import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "health_data.db"


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

def get_total_of_death_dengue():
    return 100

def get_total_of_death_covid():
    return 1000

def get_difference_of_deaths():
    covid_number = get_total_of_death_covid()
    dengue_number = get_total_of_death_dengue() 
    
    if covid_number < dengue_number:
        return 'Tivemos mais mortes por dengue: ' + 'diferença de: ' + str(dengue_number - covid_number)
    elif dengue_number < covid_number:
        return 'Tivemos mais mortes por covid: ' + 'diferença de: ' +  str(covid_number - dengue_number)
    else:
        return 'Número de mortes iguais'
    
# Configuração da interface Streamlit
st.title("Dados de Mortes por COVID-19 no Brasil")

# Exibir dados de COVID-19
st.write("Exibindo dados de mortes por COVID-19 nos últimos 5 anos:")
covid_data = get_covid_data()

if not covid_data.empty:
    st.subheader("Dados de COVID-19")
    st.dataframe(covid_data)
else:
    st.write("Não há dados de COVID-19 disponíveis.")
    
    
# Configuração da interface Streamlit
st.title("Dados de Mortes por DENGUE no Brasil")

# Exibir dados de COVID-19
st.write("Exibindo dados de mortes por DENGUE nos últimos 5 anos:")
dengue_data = get_covid_data()

if not dengue_data.empty:
    st.subheader("Dados de DENGUE")
    st.dataframe(dengue_data)
else:
    st.write("Não há dados de DENGUE disponíveis.")

st.write("Diferença de morte entre covid e dengue últimos 5 anos:")
total_death_covid = get_total_of_death_covid()
total_death_dengue = get_total_of_death_dengue()
difference_death = get_difference_of_deaths()

st.subheader('Mortes por covid: ' + str(total_death_covid))
st.subheader('Mortes por dengue: ' + str(total_death_dengue))

st.subheader(difference_death)
