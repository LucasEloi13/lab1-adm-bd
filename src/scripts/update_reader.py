# src/scripts/ecommerce_update_reader.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from db.conexao import conectar

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def update_reader():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SET autocommit = 0;")
        cur.execute("START TRANSACTION;")

        produto_id = 1  # fixo para simular leitura antes/depois
        cur.execute("SELECT preco FROM produtos WHERE id = %s", (produto_id,))
        preco1 = cur.fetchone()[0]
        logging.info(f"Preço inicial do produto {produto_id}: R$ {preco1}")

        logging.info("Aguardando 10s...")
        time.sleep(10)

        cur.execute("SELECT preco FROM produtos WHERE id = %s", (produto_id,))
        preco2 = cur.fetchone()[0]
        logging.info(f"Preço após espera: R$ {preco2}")

        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    update_reader()
