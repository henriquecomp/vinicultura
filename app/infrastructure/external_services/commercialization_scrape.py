from app.application.DTOs.commercialization_response import CommercializationResponse
from app.infrastructure.external_services.base_scrape import BaseScrape


class CommercializationScrape:
    def get_commercialization(self, url) -> list[CommercializationResponse]:
        """
        Serviço que utiliza o BaseScrape (genérico) e especializa os 
        dados devolvendo-os como dados de comercialização.

        Args:
            

        Returns:
            list[CommercializationResponse]: Dados do usuário criado:
                {
                    category: str, # categoria do produto
                    name: str, # nome do produto
                    quantity: float, # quantidade do produto                    
                }

        Raises:
            

        """        
        result = BaseScrape(url).handle()
        data = []

        for item in result:
            data.append(CommercializationResponse(
                category=item.category,
                name=item.name,
                quantity=item.quantity,
            ))

        return data
