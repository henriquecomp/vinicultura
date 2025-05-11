from infrastructure.external_services.export_scrape import ExportScrape
from API.models.responses.export_response import ExportResponse
from infrastructure.repositories.export_scrape_repository import ExportScrapeRepository
from application.common.url_handler import UrlHandler


class ExportService:
    def get_export_by_year(self, year: int) -> list[ExportResponse]:
        urls = ExportScrapeRepository().get_export_target()
        data = []
        for item in urls:
            url = UrlHandler().url_handler(item.url, year)
            print(url)
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
