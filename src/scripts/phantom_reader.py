# src/scripts/ecommerce_phantom_reader.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from random import randint
from db.conexao import conectar

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def phantom_reader():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SET autocommit = 0;")
        cur.execute("START TRANSACTION;")

        produto_id = randint(1, 6)
        logging.info(f"Iniciando leitura de pedidos do produto {produto_id}...")

        cur.execute("SELECT COUNT(*) FROM pedidos WHERE produto_id = %s", (produto_id,))
        count1 = cur.fetchone()[0]
        logging.info(f"Leitura inicial: {count1} pedidos encontrados.")

        time.sleep(10)

        cur.execute("SELECT COUNT(*) FROM pedidos WHERE produto_id = %s", (produto_id,))
        count2 = cur.fetchone()[0]
        logging.info(f"Leitura final: {count2} pedidos encontrados.")

        if count2 > count1:
            logging.warning("Phantom read detectado.")
        else:
            logging.info("Leitura consistente.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro na transação: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    phantom_reader()
