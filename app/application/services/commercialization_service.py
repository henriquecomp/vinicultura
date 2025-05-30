from fastapi import HTTPException
from app.application.DTOs.config_response import ConfigResponse
from app.infrastructure.external_services.commercialization_scrape import CommercializationScrape
from app.application.DTOs.commercialization_response import CommercializationResponse
from app.application.common.config import Config
from app.application.common.url_handler import UrlHandler
from app.infrastructure.repositories.commercialization_csv import CommercializationCSV


class CommercializationService:

    def get_commercialization(self, year: int) -> list[CommercializationResponse]:
        """
        Serviço que configura a raspagem de dados na aba de Comercialização do sitema da Embrapa
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem

        Returns:
            list: Uma lista dos dados de comercialização raspados
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # nome do produto
                        "quantity": float, # a quantidade em litros do produto raspado
                    }
                ]

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """

        data = []
        config = Config().get_config("Commercialization")
        actualConfig: ConfigResponse = None
        try:
            for item in config:
                actualConfig = item                
                url = UrlHandler().url_handler(item.url, year)
                commercialization_scrape = CommercializationScrape()
                results = commercialization_scrape.get_commercialization(url)
                for item in results:
                    data.append(
                        CommercializationResponse(
                            category=item.category,
                            name=item.name,
                            quantity=item.quantity,
                            source="SCRAP"
                        )
                    )
            return data
        except Exception as e:
            try:
                data.clear()
                for item in config:
                    results = CommercializationCSV().get_commercialization_csv(
                        item.file, item.category, year
                    )
                    for item in results:
                        data.append(
                            CommercializationResponse(
                                category=item.category,
                                name=item.name,
                                quantity=item.quantity,
                                source="CSV"
                            )
                        )

                return data
            except FileNotFoundError as e:
                raise Exception(f"ERRO: Arquivo {actualConfig.file} não encontrado.")
            except PermissionError:
                raise Exception(f"ERRO: Sem permissão para ler o arquivo {actualConfig.file}.")
            except IOError as e:
                raise Exception(f"ERRO de E/S ao tentar ler o arquivo '{actualConfig.file}': {e}")
            except Exception as e:
                raise
        except Exception as e:
            raise
