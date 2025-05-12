# Simulação de Transações em E-commerce com Python + MySQL

Este projeto simula cenários clássicos de anomalias de transações (como phantom reads, rollbacks e atualizações concorrentes) usando **MySQL**, **Python** e **Docker**. O banco simula um sistema de pedidos de e-commerce.

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/LucasEloi13/lab1-adm-bd.git
cd lab1-adm-bd
```

### 2. Suba o container MySQL

O projeto usa o `docker-compose.yml` localizado em `docker/` (lembre-se de alterar as informações do banco de dados se julgar necessário).

```bash
docker compose -f docker/docker-compose.yml up -d
```

Esse comando iniciará o MySQL na porta `3306`. 

### 3. Configure as variáveis de ambiente
Antes de rodar o projeto, é necessário configurar o arquivo `.env` com as credenciais e parâmetros corretos do banco de dados. Um exemplo está disponível no arquivo `example.env`.

#### Como usar:
1. Copie o arquivo de exemplo:
   ```bash
   cp example.env .env
   ```
2. Edite o novo arquivo EXAMPLE.env com suas configurações reais.

### 4. Instale as dependências do Python

Execute dentro do Codespaces ou localmente (com Python 3.8+).

```bash
pip install -r requirements.txt
```

### 5. Configure o banco com dados falsos

```bash
python src/scripts/setup_database.py
```

Esse script usa a biblioteca `Faker` para criar:

- 20 clientes
- 6 produtos
- 50 pedidos aleatórios

---

## 🧪 Testes de concorrência

Os testes a seguir simulam **transações paralelas** que podem gerar problemas como *phantom read* ou *non-repeatable read*.

---

### ✅ Phantom Read

#### 1. Terminal A: execute o leitor

```bash
python src/scripts/phantom_reader.py
```

Esse script inicia uma transação, conta os pedidos de um produto e aguarda 10s antes de contar novamente.

#### 2. Terminal B (durante a espera de 10s): execute o escritor

```bash
python src/scripts/phantom_writer.py
```

Esse script insere um novo pedido para um produto aleatório e realiza `COMMIT` após 5s.

#### Resultado esperado:

- Se ambos acessarem o **mesmo `produto_id`**, o `phantom_reader` detectará um aumento entre as contagens (`phantom read detectado`).

---

### ✅ Update Read com Rollback

#### 1. Terminal A: execute o escritor

```bash
python src/scripts/update_writer.py
```

Lê o preço de um produto antes e depois de 10s.

#### 2. Terminal B: execute o leitor

```bash
python src/scripts/update_reader.py
```

Altera o preço do mesmo produto e executa `ROLLBACK` após 10s.

#### Resultado esperado:

- Se o `reader` ver o preço alterado, houve **non-repeatable read**.
- Se não, a transação está protegida (dependendo do nível de isolamento).

---

### ✅ Cenários Avançados

Além dos scripts básicos, o projeto inclui cenários avançados para testar situações mais complexas de concorrência e isolamento:

- `src/scripts/cenario_avancado_writer.py`
- `src/scripts/cenario_avancado_reader.py`

#### Como executar:

1. **Terminal A:**  
   Execute o leitor avançado:
   ```bash
   python src/scripts/cenario_avancado_reader.py
   ```

2. **Terminal B:**  
   Execute o escritor avançado:
   ```bash
   python src/scripts/cenario_avancado_writer.py
   ```

Esses scripts simulam operações concorrentes mais sofisticadas, permitindo observar anomalias e comportamentos específicos de acordo com o nível de isolamento configurado.

Se os agregados (COUNT, SUM, AVG) mudarem entre as leituras, houve phantom read ou instabilidade.

O script já imprime:

- Inconsistência detectada entre as leituras
- Leitura agregada consistente

---

## ⚙️ Configurações de isolamento

Você pode alterar o nível de isolamento diretamente no arquivo `.env`:

```env
DB_ISOLATION_LEVEL=READ COMMITTED
```

Valores suportados:

- `READ UNCOMMITTED`
- `READ COMMITTED`
- `REPEATABLE READ`
- `SERIALIZABLE`

Isso pode ser implementado dinamicamente nos scripts, usando:

```python
iso = os.getenv("DB_ISOLATION_LEVEL", "READ COMMITTED")
cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {iso};")
```

---

## 🧹 Para encerrar o ambiente

```bash
docker compose -f docker/docker-compose.yml down
```

---

## 📁 Estrutura do projeto

```
.
├── requirements.txt
├── EXAMPLE.env
├── README.md
├── docker
│   └── docker-compose.yml
└── src
    ├── db
    │   ├── __pycache__
    │   │   └── conexao.cpython-312.pyc
    │   ├── check_connection.py
    │   ├── conexao.py
    │   └── setup_database.py
    └── scripts
        ├── import.py
        ├── phantom_reader.py
        ├── phantom_writer.py
        ├── update_reader.py
        ├── update_writer.py
        ├── cenario_avancado_reader.py
        └── cenario_avancado_writer.py
```

---

## ✅ Requisitos

- Docker e Docker Compose
- Python 3.8+
- [Faker](https://faker.readthedocs.io/)
- mysql-connector-python
