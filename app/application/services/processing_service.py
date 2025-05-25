from app.infrastructure.external_services.processing_scrape import ProcessingScrape
from app.application.DTOs.processing_response import ProcessingResponse
from app.application.common.config import Config
from app.application.common.url_handler import UrlHandler
from app.infrastructure.repositories.processing_csv import ProcessingCSV

class ProcessingService:

    def get_processing_by_year(self, year: int) -> list[ProcessingResponse]:
        
        """
        Serviço que configura a raspagem de dados na aba de processamento do sitema da Embrapa 
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem

        Returns:
            list: Uma lista dos dados de processamento raspados
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # nome do produto
                        "quantity": float, # a quantidade em Kg do produto raspado
                    }
                ]            

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """          
        try:
            
            division = 1 / 0        # retirar esta linha
            data = []
            config = Config().get_config("Processing")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)
                processing_scrape = ProcessingScrape()
                results = processing_scrape.get_processing_by_year(url)
                for item in results:
                    data.append(
                        ProcessingResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity,
                        )
                    )
            return data
        
        except Exception as e:
            data = []
            config = Config().get_config("Processing")
            for item in config:                
                results = ProcessingCSV().get_processing_by_year_csv(item.file, item.category, year)
                for item in results:
                    data.append(
                        ProcessingResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity
                        )
                    )

            return data
