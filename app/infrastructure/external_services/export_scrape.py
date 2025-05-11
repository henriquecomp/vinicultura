from API.models.responses.export_response import ExportResponse
from infrastructure.external_services.base_scrape import BaseScrape


class ExportScrape:
    def __init__(self, category: str = None):
        self.category = category

    def get_export_by_year(self, url) -> list[ExportResponse]:
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(ExportResponse(
                category=self.category,
                country=item.name,
                quantity=item.quantity,
                value=item.value,
            ))

        return data
