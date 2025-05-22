import pandas as pd
import json

def retornar_processamento_csv(file_path, categoria, ano):

    # Carregar o CSV com delimitador ';'
    df = pd.read_csv(file_path, delimiter=';')

    # Filtrar e construir a lista de dicionários
    resultado = [
        {"category": categoria,"name": row["cultivar"], "quantity": int(row[ano])}
        for _, row in df.iterrows()
    ]
    return json.dumps(resultado, ensure_ascii=False, indent=2)


from application.DTOs.processing_response import ProcessingResponse
import pandas as pd


class ProcessingCSV:

    def get_processing_by_year_csv(
        self, file_path, category, year
    ) -> list[ProcessingResponse]:
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                ProcessingResponse(
                    category=category,
                    name=str(row["cultivar"]),
                    quantity=int(row[f"{year}"])
                )
            )

        return data
    