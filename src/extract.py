import requests
import pandas as pd
from datetime import datetime,timedelta
# Dicionário com o nome e código de cada indicador no SGS do Banco Central

SERIES = {
"selic": 11,
"cambio_usd":1,
"ipca":13522,

}
# URL base da API 
BASE_URL= "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
 # Monta a URL com o código da série específica
def buscar_serie(nome,codigo,data_inicio,data_fim):
    url= BASE_URL.format(codigo=codigo)
       # Parâmetros da requisição: formato e período de coleta
    params = {
        "formato":"json",
        "dataInicial":data_inicio,
        "dataFinal":data_fim,
        }
         # Faz a requisição HTTP para a API do Banco Central
    response = requests.get(url,params= params ,timeout=15)
    dados = response.json()
    if isinstance(dados, dict) and "erro" in dados:
        raise ValueError(f"API BCB erro para série '{nome}' (código {codigo}): {dados}")
    # Converte o JSON retornado para um DataFrame do pandas
    return pd.DataFrame(dados)