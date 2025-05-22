from infrastructure.external_services.export_scrape import (
    ExportScrape,
)
from application.DTOs.export_response import ExportResponse
from application.common.config import Config
from application.common.url_handler import UrlHandler
from infrastructure.repositories.export_csv import ExportCSV

class ExportService:
    
    def get_export_by_year(self, year: int) -> list[ExportResponse]:

        """
        Serviço que configura a raspagem de dados na aba de Exportação do sitema da Embrapa 
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem

        Returns:
            list: Uma lista dos dados de exportação raspados
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # país exportação
                        "quantity": float, # a quantidade em Kg do produto raspado
                        "value": float, # valor em dolares de exportações    
                    }
                ]            

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """             
        try:

            division = 1 / 0        # retirar esta linha
            data = []
            config = Config().get_config("Export")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)            
                export_scrape = ExportScrape(item.category)
                result = export_scrape.get_export_by_year(url)
                for item in result:
                    data.append(
                        ExportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value,
                        )
                    )

            return data
        except Exception as e:
            data = []
            config = Config().get_config("Export")
            for item in config:                
                results = ExportCSV().get_export_by_year_csv(item.file, item.category, year)
                for item in results:
                    data.append(
                        ExportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value
                        )
                    )

            return data
