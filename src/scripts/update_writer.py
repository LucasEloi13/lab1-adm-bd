# src/scripts/ecommerce_update_writer.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from db.conexao import conectar

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def update_writer():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SET autocommit = 0;")
        cur.execute("START TRANSACTION;")

        produto_id = 1
        cur.execute("SELECT preco FROM produtos WHERE id = %s", (produto_id,))
        preco_atual = cur.fetchone()[0]
        logging.info(f"Preço atual do produto {produto_id}: R$ {preco_atual}")

        novo_preco = round(preco_atual * 1.10, 2)
        cur.execute("UPDATE produtos SET preco = %s WHERE id = %s", (novo_preco, produto_id))
        logging.info(f"Preço alterado para R$ {novo_preco}, mas ainda sem COMMIT.")

        logging.info("Aguardando 10s antes de ROLLBACK...")
        time.sleep(10)

        conn.rollback()
        logging.info("ROLLBACK executado. Preço revertido.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    update_writer()
