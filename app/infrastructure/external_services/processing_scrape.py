from application.DTOs.processing_response import ProcessingResponse
from infrastructure.external_services.base_scrape import BaseScrape


class ProcessingScrape:
    def get_processing_by_year(self, url) -> list[ProcessingResponse]:
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(
                ProcessingResponse(
                    category=item.category,
                    name=item.name,
                    quantity=item.quantity,
                )
            )

        return data
