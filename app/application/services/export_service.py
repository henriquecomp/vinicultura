from app.domain.enums.export_enum import ExportEnum
from app.infrastructure.external_services.export_scrape import (
    ExportScrape,
)
from app.application.DTOs.export_response import ExportResponse
from app.application.common.config import Config
from app.application.common.url_handler import UrlHandler
from app.infrastructure.repositories.export_csv import ExportCSV

class ExportService:
    
    def get_export(self, year: int, category: ExportEnum) -> list[ExportResponse]:

        """
        Serviço que configura a raspagem de dados na aba de Exportação do sitema da Embrapa 
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem
            category (ExportEnum): Categoria da uva, o valor padrão será em "" e trará todas as categorias.

        Returns:
            list: Uma lista dos dados de exportação raspados
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # país exportação
                        "quantity": float, # a quantidade em Kg do produto raspado
                        "value": float, # valor em dolares de exportações    
                    }
                ]            

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """             

        data = []
        config = Config().get_category(Config().get_config("Export"), category)

        try:
            for item in config:
                url = UrlHandler().url_handler(item.url, year)            
                export_scrape = ExportScrape(item.category)
                result = export_scrape.get_export(url)
                for item in result:
                    data.append(
                        ExportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value,
                        )
                    )

            return data
        except Exception as e:
            data.clear()
            for item in config:                
                results = ExportCSV().get_export_csv(item.file, item.category, year)
                for item in results:
                    data.append(
                        ExportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value
                        )
                    )

            return data
