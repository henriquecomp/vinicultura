from API.models.responses.import_response import ImportResponse
from infrastructure.external_services.base_scrape import BaseScrape


class ImportScrape:
    def __init__(self, category: str = None):
        self.category = category

    def get_import_by_year(self, url) -> list[ImportResponse]:
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(ImportResponse(
                category=self.category,
                country=item.name,
                quantity=item.quantity,
                value=item.value,
            ))

        return data
