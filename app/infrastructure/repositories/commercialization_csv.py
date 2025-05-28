from app.application.DTOs.commercialization_response import CommercializationResponse
import pandas as pd


class CommercializationCSV:

    def get_commercialization_csv(
        self, file_path, category, year
    ) -> list[CommercializationResponse]:
        """
        Serviço que configura a leitura de dados referentes à Comercialização
        e trata o retorno da leitura devolvida para o endpoint

        Args:
            file_path: str, # Caminho do arquivo CSV a ser trabalhado
            category: str, # Categoria de comercialilzação
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a importação

        Returns:
            list: Uma lista dos dados de comercialização importada dos arquivos CSV
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # Produto
                        "quantity": float, # a quantidade em Kg do produto importado
                    }
                ]

        """
        
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                CommercializationResponse(
                    category=category,
                    name=str(row["Produto"]),
                    quantity=int(row[f"{year}"])
                )
            )

        return data
