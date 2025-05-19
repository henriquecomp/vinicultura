from infrastructure.external_services.production_scrape import ProductionScrape
from application.DTOs.production_response import ProductionResponse
from application.common.config import Config
from application.common.url_handler import UrlHandler


class ProductionService:

    def get_production_by_year(self, year: int) -> list[ProductionResponse]:
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
