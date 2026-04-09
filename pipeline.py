import schedule
import time
from datetime import datetime, timedelta
from src.extract import buscar_serie, SERIES
from src.transform import transformar
from src.load import carregar

def executar_pipeline():
    # Define date range — last 30 days
    data_fim= datetime.today().strftime("%d/%m/%Y")
    data_inicio = (datetime.today()-timedelta(days=60)).strftime("%d/%m/%Y")

    # Run ETL for each series
    for nome, codigo in SERIES.items():
        try:
            df = buscar_serie(nome, codigo, data_inicio, data_fim)
            df = transformar(df)
            carregar(df, nome)
        except ValueError as e:
            print(f"[AVISO] Pulando série '{nome}': {e}")
def main():
    executar_pipeline()
    schedule.every().day.at("08:00").do(executar_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(60)
if __name__ == "__main__":

    main()       