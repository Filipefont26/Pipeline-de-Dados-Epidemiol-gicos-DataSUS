import pandas as pd
import glob
import os
from google.cloud import bigquery
from pandas_gbq import to_gbq



PROJECT_ID = "dadossaude-495822"
DATASET_ID = "saude_sus"

BASE_DIR = os.path.dirname(__file__)

PASTA_SILVER = r"C:\Users\lipem\OneDrive\Documentos\pipeline ETL\silver"



arquivos = glob.glob(os.path.join(PASTA_SILVER, "*_limpo.csv"))

dfs = {}

client = bigquery.Client(project=PROJECT_ID)

for arquivo in arquivos:
    nome = os.path.splitext(os.path.basename(arquivo))[0]
    df = pd.read_csv(
        arquivo,
        sep=";",        
        encoding="utf-8-sig"
    )

    df.columns = (
        df.columns
        .str.strip()                        
        .str.replace(" ", "_")              
        .str.replace(r"[^\w]", "_", regex=True)  
        .str.lower()                       
    )

    to_gbq(
        df,
        destination_table=f"{DATASET_ID}.{nome}",
        project_id=PROJECT_ID,
        if_exists="replace",
    )

    print(f"{nome} enviado!")











