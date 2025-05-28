import pandas as pd
import json
from app.application.DTOs.processing_response import ProcessingResponse
import pandas as pd

class ProcessingCSV:

    def get_processing_csv(
        self, file_path, category, year
    ) -> list[ProcessingResponse]:
        """
        Serviço que configura a leitura de dados referentes ao Processamento de Uvas
        e trata o retorno da leitura devolvida para o endpoint

        Args:
            file_path: str, # Caminho do arquivo CSV a ser trabalhado
            category: str, # Categoria de comercialilzação
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a importação

        Returns:
            list: Uma lista dos dados de processamento importado dos arquivos CSV
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # Produto
                        "quantity": float, # a quantidade em Kg do produto processado
                    }
                ]

        """

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
    