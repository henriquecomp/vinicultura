from app.infrastructure.external_services.commercialization_scrape import (
    CommercializationScrape,
)
from app.application.DTOs.commercialization_response import CommercializationResponse
from app.application.common.config import Config
from app.application.common.url_handler import UrlHandler
from app.infrastructure.repositories.commercialization_csv import CommercializationCSV

class CommercializationService:

    def get_commercialization_by_year(self, year: int) -> list[CommercializationResponse]:

        """
        Serviço que configura a raspagem de dados na aba de Comercialização do sitema da Embrapa 
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem

        Returns:
            list: Uma lista dos dados de comercialização raspados
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # nome do produto
                        "quantity": float, # a quantidade em litros do produto raspado
                    }
                ]            

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """           
        try:

            division = 1 / 0        # retirar esta linha
            data = []
            config = Config().get_config("Commercialization")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)
                commercialization_scrape = CommercializationScrape()
                results = commercialization_scrape.get_commercialization_by_year(url)
                for item in results:
                    data.append(
                        CommercializationResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity,
                        )
                    )
            return data
        except Exception as e:
            data = []
            config = Config().get_config("Commercialization")
            for item in config:                
                results = CommercializationCSV().get_commercialization_by_year_csv(item.file, item.category, year)
                for item in results:
                    data.append(
                        CommercializationResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity
                        )
                    )

            return data
