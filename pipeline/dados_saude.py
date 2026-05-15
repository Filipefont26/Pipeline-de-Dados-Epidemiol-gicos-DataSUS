import pandas as pd
import glob
import os 
from google.cloud import bigquery


# extração dos dados
BASE_DIR = os.path.dirname(__file__)

PASTA_TABELAS = os.path.join(BASE_DIR, "..", "tabelas")

arquivos = glob.glob(
   r"C:\Users\lipem\OneDrive\Documentos\pipeline ETL\base\*.csv"
)
dfs= {}

for arquivo in arquivos:
    nome = os.path.basename(arquivo).replace(".csv","")
    df = pd.read_csv(
    arquivo,
    header=None,
    encoding="latin1"
)

    dfs[nome] = df




# limpeza

def limpar_tabela(df):

    coluna = df.iloc[:,0].astype(str)

    inicio_idx = coluna[
        coluna.str.contains(
            "Ano Diagnóstico;",
            case=False,
            na=False
        )
    ].index

    if len(inicio_idx) == 0:
        return None

    inicio = inicio_idx[0]

    tabela = df.iloc[inicio:].copy()

    tabela.columns = tabela.iloc[0]

    tabela = tabela.iloc[1:].reset_index(drop=True)

    tabela = tabela.dropna(axis=1, how='all')

    tabela = tabela.replace("-", 0)

    return tabela



dfs_limpos = {}

for nome, df in dfs.items():

    tabela_limpa = limpar_tabela(df)

    if tabela_limpa is not None:
        dfs_limpos[nome] = tabela_limpa


#exportar csv limpo




os.makedirs("silver", exist_ok=True)

for nome, df in dfs_limpos.items():

    caminho = f"silver/{nome}_limpo.csv"

    df.to_csv(
        caminho,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"{nome} exportado!")







