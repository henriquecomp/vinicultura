from app.infrastructure.external_services.import_scrape import ImportScrape
from app.application.DTOs.import_response import ImportResponse
from app.application.common.url_handler import UrlHandler
from app.application.common.config import Config
from app.infrastructure.repositories.import_csv import ImportCSV



class ImportService:

    def get_import_by_year(self, year: int) -> list[ImportResponse]:
        
        """
        Serviço que configura a raspagem de dados na aba de Importação do sitema da Embrapa 
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem

        Returns:
            list: Uma lista dos dados de importação raspados
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # país importação
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
            config = Config().get_config("Import")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)
                import_scrape = ImportScrape(item.category)
                result = import_scrape.get_import_by_year(url)
                for item in result:
                    data.append(
                        ImportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value,
                        )
                    )

            return data
        
        except Exception as e:
            data = []
            config = Config().get_config("Import")
            for item in config:                
                results = ImportCSV().get_import_by_year_csv(item.file, item.category, year)
                for item in results:
                    data.append(
                        ImportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value
                        )
                    )

            return data
