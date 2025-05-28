from app.application.DTOs.import_response import ImportResponse
import pandas as pd


class ImportCSV:

    def get_import_csv(
        self, file_path, category, year
    ) -> list[ImportResponse]:
        """
        Serviço que configura a leitura de dados referentes à Importação 
        e trata o retorno da leitura devolvida para o endpoint

        Args:
            file_path: str, # Caminho do arquivo CSV a ser trabalhado
            category: str, # Categoria de Exportação
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados importação

        Returns:
            list: Uma lista dos dados de exportação, importada dos arquivos CSV
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # País destino da importação
                        "quantity": float, # a quantidade anual importado
                        "value": float, # O valor anual importado
                    }
                ]

        """
        
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                ImportResponse(
                    category=category,
                    country=str(row["País"]),
                    quantity=int(row[f"Qtd {year}"]),
                    value=int(row[f"Val {year}"])
                )
            )

        return data
