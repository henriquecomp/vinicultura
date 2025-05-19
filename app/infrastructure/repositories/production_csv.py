import pandas as pd
import json

def retornar_producao_csv(file_path, categoria, ano):

    # Carregar o CSV com delimitador ';'
    df = pd.read_csv(file_path, delimiter=';')

    # Filtrar e construir a lista de dicionários
    resultado = [
        {"category": categoria,"name": row["produto"], "quantity": int(row[ano])}
        for _, row in df.iterrows()
    ]
    return json.dumps(resultado, ensure_ascii=False, indent=2)


resultado_teste = retornar_producao_csv("C:\\Eliel\\Pessoal\\ML\\Trabalho\\vinicultura\\app\\infrastructure\\files\\Producao.csv", "producao", "2023")
print(resultado_teste)

