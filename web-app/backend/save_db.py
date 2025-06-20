from sqlalchemy import create_engine, inspect, text
import sqlite3
import os
from models import Base  # seus modelos SQLAlchemy com alterações

NOVO_BANCO = "test1.db"
ANTIGO_BANCO = "test.db"

def criar_novo_banco():
    print("Criando novo banco com estrutura atualizada...")
    engine = create_engine(f"sqlite:///{NOVO_BANCO}")
    Base.metadata.create_all(engine)

def copiar_dados_compatíveis():
    src_conn = sqlite3.connect(ANTIGO_BANCO)
    dest_conn = sqlite3.connect(NOVO_BANCO)

    src_cursor = src_conn.cursor()
    dest_cursor = dest_conn.cursor()

    print("Copiando dados de tabelas compatíveis...")
    src_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in src_cursor.fetchall() if not t[0].startswith("sqlite_")]

    for table in tables:
        try:
            src_cursor.execute(f"PRAGMA table_info({table})")
            src_cols = [col[1] for col in src_cursor.fetchall()]

            dest_cursor.execute(f"PRAGMA table_info({table})")
            dest_cols = [col[1] for col in dest_cursor.fetchall()]

            common_cols = list(set(src_cols) & set(dest_cols))
            if not common_cols:
                continue

            col_str = ", ".join(common_cols)
            src_cursor.execute(f"SELECT {col_str} FROM {table}")
            rows = src_cursor.fetchall()

            placeholders = ",".join(["?"] * len(common_cols))
            insert_sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"
            dest_cursor.executemany(insert_sql, rows)

            print(f"-> {table}: {len(rows)} registros copiados.")
        except Exception as e:
            print(f"Erro ao copiar tabela {table}: {e}")

    dest_conn.commit()
    src_conn.close()
    dest_conn.close()

if __name__ == "__main__":
    if os.path.exists(NOVO_BANCO):
        os.remove(NOVO_BANCO)

    criar_novo_banco()
    copiar_dados_compatíveis()
