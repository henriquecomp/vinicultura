from infrastructure.external_services.processing_scrape import ProcessingScrape
from application.DTOs.processing_response import ProcessingResponse


class ProcessingService:

    def get_processing_by_year(self, year: int) -> list[ProcessingResponse]:
        urlQuery = ""
        if year is not None:
            urlQuery = f"&ano={year}"

        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03{urlQuery}"
        processing_scrape = ProcessingScrape()

        return processing_scrape.get_processing_by_year(url)
