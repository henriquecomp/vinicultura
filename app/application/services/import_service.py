from infrastructure.external_services.import_scrape import ImportScrape
from API.models.responses.import_response import ImportResponse
from infrastructure.repositories.import_scrape_repository import ImportScrapeRepository
from application.common.url_handler import UrlHandler


class ImportService:

    def get_import_by_year(self, year: int) -> list[ImportResponse]:
        urls = ImportScrapeRepository().get_import_target()
        data = []
        for item in urls:
            url = UrlHandler().url_handler(item.url, year)
            print(url)
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
