from infrastructure.external_services.export_scrape import ExportScrape
from application.DTOs.export_response import ExportResponse
from application.common.url_handler import UrlHandler
from application.common.config import Config


class ExportService:
    def get_export_by_year(self, year: int) -> list[ExportResponse]:
        data = []
        config = Config().get_config("Export")
        for item in config:
            url = UrlHandler().url_handler(item.url, year)            
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
