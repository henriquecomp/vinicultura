from infrastructure.external_services.processing_scrape import ProcessingScrape
from application.DTOs.processing_response import ProcessingResponse
from application.common.config import Config
from application.common.url_handler import UrlHandler

class ProcessingService:

    def get_processing_by_year(self, year: int) -> list[ProcessingResponse]:
        try:
            data = []
            config = Config().get_config("Processing")
            for item in config:
                url = UrlHandler().url_handler(item.url, year)
                processing_scrape = ProcessingScrape()
                results = processing_scrape.get_processing_by_year(url)
                for item in results:
                    data.append(
                        ProcessingResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity,
                        )
                    )
            return data
        except Exception as e:
            print(f"Error: {e}")
            # Vou chamar infrastructure/repositories/production_csv.py
            return []