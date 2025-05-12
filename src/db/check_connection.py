# check_connection.py
import mysql.connector
from dotenv import load_dotenv
import os

from conexao import conectar

load_dotenv()

try:
    conn = conectar()
    print("Conexão estabelecida com sucesso!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Erro ao conectar: {err}")
