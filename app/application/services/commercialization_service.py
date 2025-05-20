from infrastructure.external_services.commercialization_scrape import (
    CommercializationScrape,
)
from application.DTOs.commercialization_response import CommercializationResponse
from application.common.config import Config
from application.common.url_handler import UrlHandler
from infrastructure.repositories.commercialization_csv import CommercializationCSV


class CommercializationService:

    def get_commercialization_by_year(
        self, year: int
    ) -> list[CommercializationResponse]:
        try:

            division = 1 / 0
            data = []
            config = Config().get_config("Commercialization")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)
                commercialization_scrape = CommercializationScrape()
                results = commercialization_scrape.get_commercialization_by_year(url)
                for item in results:
                    data.append(
                        CommercializationResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity,
                        )
                    )
            return data
        except Exception as e:
            data = []
            config = Config().get_config("Commercialization")
            for item in config:                
                results = CommercializationCSV().get_commercialization_by_year_csv(item.file, item.category, year)
                for item in results:
                    data.append(
                        CommercializationResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity
                        )
                    )

            return data
