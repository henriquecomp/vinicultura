from fastapi import HTTPException
from app.application.DTOs.config_response import ConfigResponse
from app.domain.enums.import_enum import ImportEnum
from app.infrastructure.external_services.import_scrape import ImportScrape
from app.application.DTOs.import_response import ImportResponse
from app.application.common.url_handler import UrlHandler
from app.application.common.config import Config
from app.infrastructure.repositories.import_csv import ImportCSV


class ImportService:

    def get_import(self, year: int, category: ImportEnum) -> list[ImportResponse]:
        """
        Serviço que configura a raspagem de dados na aba de Importação do sitema da Embrapa
        e trata o retorno da raspagem devolvida da enviar para o endpoint

        Args:
            year: int, # Ano que é passado por parametro pelo endpoint para filtrar os dados para a raspagem
            category (ImportEnum): Categoria da uva, o valor padrão será em "" e trará todas as categorias.

        Returns:
            list: Uma lista dos dados de importação raspados
                [
                    {
                        "category": str, # categoria do produto
                        "country": str, # país importação
                        "quantity": float, # a quantidade em Kg do produto raspado
                        "value": float, # valor em dolares de exportações
                    }
                ]

        Raises:
            Exception: Caso haja um lançamento de exception, irá acionar o arquivo para retornar os dados
                        como uma forma de responder a requisição caso o site esteja indisponível.
        """

        data = []
        config = Config().get_category(Config().get_config("Import"), category)
        actualConfig: ConfigResponse = None
        try:
            for item in config:
                actualConfig = item                
                url = UrlHandler().url_handler(item.url, year)
                import_scrape = ImportScrape(item.category)
                result = import_scrape.get_import(url)
                for item in result:
                    data.append(
                        ImportResponse(
                            category=item.category,
                            country=item.country,
                            quantity=item.quantity,
                            value=item.value,
                        )
                    )

            return data

        except ConnectionError as e:
            try:
                data.clear()
                for item in config:
                    actualConfig = item                
                    results = ImportCSV().get_import_csv(item.file, item.category, year)
                    for item in results:
                        data.append(
                            ImportResponse(
                                category=item.category,
                                country=item.country,
                                quantity=item.quantity,
                                value=item.value,
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
