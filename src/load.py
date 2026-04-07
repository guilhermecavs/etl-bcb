from sqlalchemy import text
from src.database import get_engine

# Table mapping
TABELAS = {
    "selic":      "selic",
    "cambio_usd": "cambio_usd",
    "ipca":       "ipca",
}

def carregar(df, nome):
    tabela = TABELAS.get(nome)
    engine = get_engine()

    # Open database connection
    with engine.begin() as conn:
        for _, row in df.iterrows():
            # Insert row, skip if date already exists
            sql = text(f"""
                INSERT INTO {tabela} (data, valor)
                VALUES (:data, :valor)
                ON CONFLICT (data) DO NOTHING
            """)
            conn.execute(sql, {"data": row["data"], "valor": row["valor"]})