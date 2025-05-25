from app.application.DTOs.processing_response import ProcessingResponse
from app.infrastructure.external_services.base_scrape import BaseScrape


class ProcessingScrape:
    def get_processing(self, url) -> list[ProcessingResponse]:
        """
        Serviço que utiliza o serviço BaseScrape (genérico) e especializa os 
        dados devolvendo-os como dados de processamento.

        Args:
            

        Returns:
            list[ProcessingResponse]: Dados do usuário criado:
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
            data.append(
                ProcessingResponse(
                    category=item.category,
                    name=item.name,
                    quantity=item.quantity,
                )
            )

        return data
