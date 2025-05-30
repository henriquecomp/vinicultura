from fastapi import HTTPException
from app.application.DTOs.config_response import ConfigResponse
from app.domain.enums.processing_enum import ProcessingEnum
from app.infrastructure.external_services.processing_scrape import ProcessingScrape
from app.application.DTOs.processing_response import ProcessingResponse
from app.application.common.config import Config
from app.application.common.url_handler import UrlHandler
from app.infrastructure.repositories.processing_csv import ProcessingCSV


class ProcessingService:

    def get_processing(
        self, year: int, category: ProcessingEnum
    ) -> list[ProcessingResponse]:
        """
        Serviço que configura a raspagem de dados na aba de processamento do sitema da Embrapa
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem
            category: ProcessingEnum # Qual a categoria que deseja filtrar os dados

        Returns:
            list: Uma lista dos dados de processamento raspados
                [
                    {
                        "category": str, # categoria do produto
                        "name": str, # nome do produto
                        "quantity": float, # a quantidade em Kg do produto raspado
                    }
                ]

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """

        data = []
        config = Config().get_category(Config().get_config("Processing"), category)
        actualConfig: ConfigResponse = None
        try:
            for item in config:
                actualConfig = item                
                url = UrlHandler().url_handler(item.url, year)
                processing_scrape = ProcessingScrape()
                results = processing_scrape.get_processing(url)
                for item in results:
                    data.append(
                        ProcessingResponse(
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
                    actualConfig = item
                    results = ProcessingCSV().get_processing_csv(
                        item.file, item.category, year
                    )
                    for item in results:
                        data.append(
                            ProcessingResponse(
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
