from application.DTOs.export_response import ExportResponse
from infrastructure.external_services.base_scrape import BaseScrape


class ExportScrape:
    def __init__(self, category: str = None):
        self.category = category

    def get_export_by_year(self, url) -> list[ExportResponse]:
        """
        Serviço que utiliza o serviço BaseScrape (genérico) e especializa os 
        dados devolvendo-os como dados de exportação.

        Args:
            

        Returns:
            list[ExportResponse]: Dados do usuário criado:
                {
                    category: str, # categoria do produto
                    country: str, # país exportação
                    quantity: float, # quantidade do produto                    
                    value: float, # valor em dolares
                }

        Raises:
            

        """            
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(ExportResponse(
                category=self.category,
                country=item.name,
                quantity=item.quantity,
                value=item.value,
            ))

        return data
