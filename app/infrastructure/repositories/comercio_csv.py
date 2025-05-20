from application.DTOs.commercialization_response import CommercializationResponse
import pandas as pd
import json

def retornar_comercio_csv(file_path, categoria, ano):

    # Carregar o CSV com delimitador ';'
    df = pd.read_csv(file_path, delimiter=';')

    # Filtrar e construir a lista de dicionários
    # resultado = [
    #     {"category": categoria,"name": row["Produto"], "quantity": int(row[ano])}
    #     for _, row in df.iterrows()
    # ]
    
    data = []

    for row in df.iterrows():
        data.append(CommercializationResponse(
            category=categoria,
            name= row["Produto"],
            quantity=int(row[ano]),
    ))

    return data

    
    
    #return json.dumps(resultado, ensure_ascii=False, indent=2)
    #return resultado

#resultado_teste = retornar_comercio_csv("C:\\Eliel\\Pessoal\\ML\\Trabalho\\vinicultura\\app\\infrastructure\\files\\Comercio.csv", "", "2022")
#print(resultado_teste)



