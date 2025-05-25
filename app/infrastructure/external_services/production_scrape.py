from app.application.DTOs.production_response import ProductionResponse
from app.infrastructure.external_services.base_scrape import BaseScrape


class ProductionScrape:
    def get_production(self, url) -> list[ProductionResponse]:
        """
        Serviço que utiliza o serviço BaseScrape (genérico) e especializa os 
        dados devolvendo-os como dados de produção.

        Args:
            

        Returns:
            list[ProductionResponse]: Dados do usuário criado:
                {
                    category: str, # categoria do produto
                    nome: str, # nome do produto
                    quantity: float, # quantidade do produto                                        
                }

        Raises:
            

        """           
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(ProductionResponse(
                category=item.category,
                name=item.name,
                quantity=item.quantity,
            ))

        return data
