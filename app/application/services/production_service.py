from infrastructure.external_services.production_scrape import ProductionScrape
from application.DTOs.production_response import ProductionResponse
from application.common.config import Config
from application.common.url_handler import UrlHandler


class ProductionService:

    def get_production_by_year(self, year: int) -> list[ProductionResponse]:
        """
        Serviço que configura a raspagem de dados na aba de produção do sitema da Embrapa 
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem

        Returns:
            list: Uma lista dos dados de produção raspados
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
            data = []
            config = Config().get_config("Production")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)
                production_scrape = ProductionScrape()
                results = production_scrape.get_production_by_year(url)
                for item in results:
                    data.append(
                        ProductionResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity,
                        )
                    )
            return data
        except Exception as e:
            print(f"Error: {e}")
            # Vou chamar infrastructure/repositories/production_csv.py
            config = Config().get_config("Production")
            for item in config:
                fileName = item.file


            print(config)
            return []
