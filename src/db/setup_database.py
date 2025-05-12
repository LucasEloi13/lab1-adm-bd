# src/scripts/setup_ecommerce.py

import logging
from faker import Faker
from random import randint, choice
from conexao import conectar

fake = Faker('pt_BR')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def setup_database():
    logging.info("Conectando ao banco...")
    conn = conectar()
    cur = conn.cursor()

    try:
        logging.info("Removendo tabelas antigas...")
        cur.execute("DROP TABLE IF EXISTS pedidos")
        cur.execute("DROP TABLE IF EXISTS clientes")
        cur.execute("DROP TABLE IF EXISTS produtos")

        logging.info("Criando tabela 'clientes'...")
        cur.execute("""
            CREATE TABLE clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100),
                email VARCHAR(100),
                cidade VARCHAR(50)
            )
        """)

        logging.info("Criando tabela 'produtos'...")
        cur.execute("""
            CREATE TABLE produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100),
                preco DECIMAL(10, 2)
            )
        """)

        logging.info("Criando tabela 'pedidos'...")
        cur.execute("""
            CREATE TABLE pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_id INT,
                produto_id INT,
                quantidade INT,
                data_pedido DATE,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            )
        """)

        logging.info("Inserindo clientes falsos...")
        for _ in range(20):
            nome = fake.name()
            email = fake.email()
            cidade = fake.city()
            cur.execute("INSERT INTO clientes (nome, email, cidade) VALUES (%s, %s, %s)", (nome, email, cidade))

        logging.info("Inserindo produtos falsos...")
        produtos = [
            ("Notebook Gamer", 5800.00),
            ("Smartphone", 1800.00),
            ("Fone Bluetooth", 199.90),
            ("Smartwatch", 899.99),
            ("Teclado Mecânico", 349.00),
            ("Mouse Óptico", 89.99)
        ]
        for nome, preco in produtos:
            cur.execute("INSERT INTO produtos (nome, preco) VALUES (%s, %s)", (nome, preco))

        logging.info("Inserindo pedidos aleatórios...")
        for _ in range(50):
            cliente_id = randint(1, 20)
            produto_id = randint(1, len(produtos))
            quantidade = randint(1, 5)
            data = fake.date_this_year()
            cur.execute("""
                INSERT INTO pedidos (cliente_id, produto_id, quantidade, data_pedido)
                VALUES (%s, %s, %s, %s)
            """, (cliente_id, produto_id, quantidade, data))

        conn.commit()
        logging.info("Banco de dados de e-commerce configurado com sucesso.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Erro ao configurar o banco: {e}")
    finally:
        cur.close()
        conn.close()
        logging.info("Conexão com o banco encerrada.")

if __name__ == "__main__":
    setup_database()
