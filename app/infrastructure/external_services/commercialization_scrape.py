from API.models.responses.commercialization_response import CommercializationResponse
from infrastructure.external_services.base_scrape import BaseScrape


class CommercializationScrape:
    def get_commercialization_by_year(self, url) -> list[CommercializationResponse]:
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(CommercializationResponse(
                category=item.category,
                name=item.name,
                quantity=item.quantity,
            ))

        return data
