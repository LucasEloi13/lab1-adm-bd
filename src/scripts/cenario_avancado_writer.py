import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import time
from random import randint
from faker import Faker
from db.conexao import conectar
from dotenv import load_dotenv

load_dotenv()
iso = os.getenv("DB_ISOLATION_LEVEL", "READ COMMITTED")
fake = Faker('pt_BR')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def bulk_writer():
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("SET autocommit = 0;")
        cur.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {iso};")
        cur.execute("START TRANSACTION;")

        logging.info("Inserindo 10 novos pedidos em lote...")
        for _ in range(10):
            cliente_id = randint(1, 20)
            produto_id = 1  # fixo para facilitar testes agregados
            quantidade = randint(1, 3)
            data = fake.date_this_year()

            cur.execute("""
                INSERT INTO pedidos (cliente_id, produto_id, quantidade, data_pedido)
                VALUES (%s, %s, %s, %s)
            """, (cliente_id, produto_id, quantidade, data))
        
        logging.info("Aguardando 8s antes do COMMIT...")
        time.sleep(8)
        conn.commit()
        logging.info("COMMIT realizado com sucesso.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    bulk_writer()
