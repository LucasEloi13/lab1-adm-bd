import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from db.conexao import conectar
from dotenv import load_dotenv

load_dotenv()
iso = os.getenv("DB_ISOLATION_LEVEL", "READ COMMITTED")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def aggregate_reader():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SET autocommit = 0;")
        cur.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {iso};")
        cur.execute("START TRANSACTION;")

        logging.info(f"Iniciando leitura agregada de pedidos do produto_id=1 com isolamento '{iso}'...")

        cur.execute("""
            SELECT COUNT(*), SUM(quantidade), AVG(quantidade)
            FROM pedidos
            WHERE produto_id = 1
        """)
        r1 = cur.fetchone()
        logging.info(f"Primeira leitura → Total: {r1[0]}, Soma: {r1[1]}, Média: {r1[2]}")

        logging.info("Aguardando 10s antes da segunda leitura...")
        time.sleep(10)

        cur.execute("""
            SELECT COUNT(*), SUM(quantidade), AVG(quantidade)
            FROM pedidos
            WHERE produto_id = 1
        """)
        r2 = cur.fetchone()
        logging.info(f"Segunda leitura → Total: {r2[0]}, Soma: {r2[1]}, Média: {r2[2]}")

        if r2 != r1:
            logging.warning("Inconsistência detectada entre as leituras (phantom read/agregado instável).")
        else:
            logging.info("Leitura agregada consistente.")

        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    aggregate_reader()
