# src/scripts/ecommerce_phantom_writer.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from random import randint
from faker import Faker
from db.conexao import conectar

fake = Faker('pt_BR')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def phantom_writer():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SET autocommit = 0;")
        cur.execute("START TRANSACTION;")

        cliente_id = randint(1, 20)
        produto_id = randint(1, 6)
        quantidade = randint(1, 3)
        data = fake.date_this_year()

        logging.info(f"Inserindo pedido para produto {produto_id} (cliente {cliente_id})...")
        cur.execute("""
            INSERT INTO pedidos (cliente_id, produto_id, quantidade, data_pedido)
            VALUES (%s, %s, %s, %s)
        """, (cliente_id, produto_id, quantidade, data))

        logging.info("Pedido inserido. Aguardando 5s antes do COMMIT...")
        time.sleep(5)

        conn.commit()
        logging.info("COMMIT realizado com sucesso.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro na transação: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    phantom_writer()
