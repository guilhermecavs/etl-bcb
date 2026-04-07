import pandas as pd
def transformar(df):
    # Convert 'data' column from string to date
    df["data"]= pd.to_datetime(df["data"], format = "%d/%m/%Y")
    # Replace comma with dot and convert to number
    df["valor"]=df["valor"].str.replace(",", ".")
    df["valor"]= pd.to_numeric(df["valor"])
    
    # Remove rows with null values
    df = df.dropna()
    return df[["data","valor"]]