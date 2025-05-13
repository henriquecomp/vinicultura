from infrastructure.external_services.import_scrape import ImportScrape
from application.DTOs.import_response import ImportResponse
from application.common.url_handler import UrlHandler
from application.common.config import Config



class ImportService:

    def get_import_by_year(self, year: int) -> list[ImportResponse]:
        data = []
        config = Config().get_config("Import")
        for item in config:
            url = UrlHandler().url_handler(item.url, year)
            import_scrape = ImportScrape(item.category)
            result = import_scrape.get_import_by_year(url)
            for item in result:
                data.append(
                    ImportResponse(
                        category=item.category,
                        country=item.country,
                        quantity=item.quantity,
                        value=item.value,
                    )
                )

        return data
