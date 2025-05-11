from infrastructure.external_services.commercialization_scrape import CommercializationScrape
from API.models.responses.commercialization_response import CommercializationResponse


class CommercializationService:

    def get_commercialization_by_year(self, year: int) -> list[CommercializationResponse]:
        urlQuery = ""
        if year is not None:
            urlQuery = f"&ano={year}"

        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04{urlQuery}"
        commercialization_scrape = CommercializationScrape()

        return commercialization_scrape.get_commercialization_by_year(url)
