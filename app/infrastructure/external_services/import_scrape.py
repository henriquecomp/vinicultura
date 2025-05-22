from application.DTOs.import_response import ImportResponse
from infrastructure.external_services.base_scrape import BaseScrape


class ImportScrape:
    def __init__(self, category: str = None):
        self.category = category

    def get_import_by_year(self, url) -> list[ImportResponse]:
        """
        Serviço que utiliza o serviço BaseScrape (genérico) e especializa os 
        dados devolvendo-os como dados de importação.

        Args:
            

        Returns:
            list[ImportResponse]: Dados do usuário criado:
                {
                    category: str, # categoria do produto
                    country: str, # país importação
                    quantity: float, # quantidade do produto                    
                    value: float, # valor em dolares
                }

        Raises:
            

        """            
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(ImportResponse(
                category=self.category,
                country=item.name,
                quantity=item.quantity,
                value=item.value,
            ))

        return data
