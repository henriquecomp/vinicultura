from infrastructure.external_services.production_scrape import ProductionScrape
from API.models.responses.production_response import ProductionResponse


class ProductionService:

    def get_production_by_year(self, year: int) -> list[ProductionResponse]:
        urlQuery = ""
        if year is not None:
            urlQuery = f"&ano={year}"

        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02{urlQuery}"
        production_scrape = ProductionScrape()

        return production_scrape.get_production_by_year(url)
