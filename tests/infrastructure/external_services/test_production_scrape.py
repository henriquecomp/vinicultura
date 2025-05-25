import pytest
from unittest.mock import patch, MagicMock

from app.infrastructure.external_services.production_scrape import ProductionScrape
from app.application.DTOs.production_response import ProductionResponse
from app.domain.value_objects.base_scrape import BaseScrapeValueObject


@pytest.fixture
def mock_base_scrape_instance():
    """
    Fixture que cria uma instância mockada de BaseScrape.
    Esta instância será retornada quando BaseScrape() for chamado dentro de ProductionScrape,
    graças ao @patch.
    """
    mock = MagicMock()
    mock.handle.return_value = [
        BaseScrapeValueObject(
            category="VINHO DE MESA", name="Tinto Fino", quantity=150.75, value=10.5
        ),
        BaseScrapeValueObject(
            category="VINHO BRANCO", name="Branco Seco", quantity=250.0, value=12.0
        ),
    ]
    return mock


@patch("app.infrastructure.external_services.production_scrape.BaseScrape")
def test_get_production_calls_base_scrape_and_transforms_data(
    mock_base_scrape_class, mock_base_scrape_instance
):
    """
    Testa se ProductionScrape.get_production:
    1. Instancia BaseScrape com a URL correta.
    2. Chama o método handle() da instância de BaseScrape.
    3. Transforma corretamente os BaseScrapeValueObjects em ProductionResponse.
    """
    # Arrange
    mock_base_scrape_class.return_value = mock_base_scrape_instance

    production_scraper = ProductionScrape()
    test_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"

    # Act
    result = production_scraper.get_production(test_url)

    # Assert
    mock_base_scrape_class.assert_called_once_with(test_url)
    mock_base_scrape_instance.handle.assert_called_once_with()

    assert len(result) == 2

    assert isinstance(result[0], ProductionResponse)
    assert result[0].category == "VINHO DE MESA"
    assert result[0].name == "Tinto Fino"
    assert result[0].quantity == 150.75

    assert isinstance(result[1], ProductionResponse)
    assert result[1].category == "VINHO BRANCO"
    assert result[1].name == "Branco Seco"
    assert result[1].quantity == 250.0


@patch("app.infrastructure.external_services.production_scrape.BaseScrape")
def test_get_production_handles_empty_list_from_base_scrape(
    mock_base_scrape_class, mock_base_scrape_instance
):
    """
    Testa se ProductionScrape.get_production lida corretamente com uma lista vazia
    retornada por BaseScrape.handle().
    """
    # Arrange
    mock_base_scrape_class.return_value = mock_base_scrape_instance
    mock_base_scrape_instance.handle.return_value = []

    production_scraper = ProductionScrape()
    test_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"

    # Act
    result = production_scraper.get_production(test_url)

    # Assert
    mock_base_scrape_class.assert_called_once_with(test_url)
    mock_base_scrape_instance.handle.assert_called_once_with()

    assert len(result) == 0
    assert result == []
