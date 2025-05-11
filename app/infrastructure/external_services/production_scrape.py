from API.models.responses.production_response import ProductionResponse
from infrastructure.external_services.base_scrape import BaseScrape


class ProductionScrape:
    def get_production_by_year(self, url) -> list[ProductionResponse]:
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(ProductionResponse(
                category=item.category,
                name=item.name,
                quantity=item.quantity,
            ))

        return data
