from app.application.DTOs.production_response import ProductionResponse
import pandas as pd


class ProductionCSV:

    def get_production_csv(
        self, file_path, category, year
    ) -> list[ProductionResponse]:
        """
        Serviço que configura a leitura de dados referentes à Produção de Vinhos
        e trata o retorno da leitura devolvida para o endpoint

        Args:
            file_path: str, # Caminho do arquivo CSV a ser trabalhado
            category: str, # Categoria de produção
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a importação

        Returns:
            list: Uma lista dos dados de produção importada dos arquivos CSV
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # Produto
                        "quantity": float, # a quantidade anual do produto produzido
                    }
                ]

        """
        
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                ProductionResponse(
                    category=category,
                    name=str(row["produto"]),
                    quantity=int(row[f"{year}"])
                )
            )

        return data
    