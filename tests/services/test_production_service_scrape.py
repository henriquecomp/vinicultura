import pytest
from unittest.mock import patch, MagicMock

# Importar a classe de serviço e DTOs necessários
from app.application.services.production_service import ProductionService #
from app.application.DTOs.production_response import ProductionResponse
from app.application.DTOs.config_response import ConfigResponse


@pytest.fixture
def mock_config_instance():
    """Fixture para mockar a instância da classe Config."""
    mock = MagicMock()
    mock.get_config.return_value = [
        ConfigResponse(category="", url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02", file="./app/infrastructure/files/Producao.csv")
    ]
    return mock

@pytest.fixture
def mock_url_handler_instance():
    """Fixture para mockar a instância da classe UrlHandler."""
    mock = MagicMock()
    mock.url_handler.return_value = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=2023"
    return mock

@pytest.fixture
def mock_production_scrape_instance():
    """Fixture para mockar a instância da classe ProductionScrape."""
    mock = MagicMock()
    # Simula o retorno do método get_production do scrape
    mock.get_production.return_value = [
        ProductionResponse(category="VINHO DE MESA", name="Tinto Seco", quantity=500.0),
        ProductionResponse(category="VINHO DE MESA", name="Branco Suave", quantity=300.0),
    ]
    return mock

@pytest.fixture
def mock_production_csv_instance():
    """Fixture para mockar a instância da classe ProductionCSV."""
    mock = MagicMock()
    # Simula o retorno do método get_production_csv
    mock.get_production_csv.return_value = [
        ProductionResponse(category="VINHO DE MESA", name="Tinto CSV", quantity=1000.0),
        ProductionResponse(category="VINHO DE MESA", name="Branco CSV", quantity=700.0),
    ]
    return mock

def test_get_production_success_via_scrape(
    mock_config_instance,
    mock_url_handler_instance,
    mock_production_scrape_instance,
    mock_production_csv_instance # Não será usado, mas o patch precisa dele
):
    """
    Testa o ProductionService.get_production quando o scraping é bem sucedido.
    """
    # Patch das classes no escopo do módulo production_service
    with patch('app.application.services.production_service.Config', return_value=mock_config_instance) as mock_config_class, \
         patch('app.application.services.production_service.UrlHandler', return_value=mock_url_handler_instance) as mock_url_handler_class, \
         patch('app.application.services.production_service.ProductionScrape', return_value=mock_production_scrape_instance) as mock_scrape_class, \
         patch('app.application.services.production_service.ProductionCSV', return_value=mock_production_csv_instance) as mock_csv_class:

        # Arrange
        service = ProductionService()
        test_year = 2023
        expected_config_name = "Production"
        expected_url_from_config = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
        expected_file_from_config = "./app/infrastructure/files/Producao.csv"

        # Act
        result = service.get_production(year=test_year)

        # Assert
        # Verifica se Config foi instanciado e get_config foi chamado
        mock_config_class.assert_called_once_with()
        mock_config_instance.get_config.assert_called_once_with(expected_config_name)

        # Verifica se UrlHandler foi instanciado e url_handler foi chamado
        mock_url_handler_class.assert_called_once_with()
        mock_url_handler_instance.url_handler.assert_called_once_with(expected_url_from_config, test_year)

        # Verifica se ProductionScrape foi instanciado e get_production foi chamado
        mock_scrape_class.assert_called_once_with()
        mock_production_scrape_instance.get_production.assert_called_once_with("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=2023")

        # Verifica se ProductionCSV NÃO foi chamado (porque o scrape teve sucesso)
        mock_csv_class.assert_not_called()
        mock_production_csv_instance.get_production_csv.assert_not_called()

        # Verifica o resultado
        assert len(result) == 2
        assert result[0].name == "Tinto Seco"
        assert result[0].quantity == 500.0
        assert result[1].name == "Branco Suave"
        assert result[1].quantity == 300.0

def test_get_production_fallback_to_csv_on_scrape_exception(
    mock_config_instance,
    mock_url_handler_instance,
    mock_production_scrape_instance,
    mock_production_csv_instance
):
    """
    Testa o ProductionService.get_production quando o scraping falha e o fallback para CSV ocorre.
    """
    # Configura o mock do scrape para levantar uma exceção
    mock_production_scrape_instance.get_production.side_effect = Exception("Scraping failed")

    with patch('app.application.services.production_service.Config', return_value=mock_config_instance) as mock_config_class, \
         patch('app.application.services.production_service.UrlHandler', return_value=mock_url_handler_instance) as mock_url_handler_class, \
         patch('app.application.services.production_service.ProductionScrape', return_value=mock_production_scrape_instance) as mock_scrape_class, \
         patch('app.application.services.production_service.ProductionCSV', return_value=mock_production_csv_instance) as mock_csv_class:

        # Arrange
        service = ProductionService()
        test_year = 2023
        expected_config_name = "Production"
        expected_url_from_config = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
        expected_file_from_config = "./app/infrastructure/files/Producao.csv"
        expected_category_from_config = ""

        # Act
        result = service.get_production(year=test_year)

        # Assert
        # Verifica chamadas de Config e UrlHandler (devem ocorrer como no sucesso do scrape)
        mock_config_class.assert_called_once_with()
        mock_config_instance.get_config.assert_called_once_with(expected_config_name)
        mock_url_handler_class.assert_called_once_with()
        mock_url_handler_instance.url_handler.assert_called_once_with(expected_url_from_config, test_year)

        # Verifica se ProductionScrape foi chamado (e falhou)
        mock_scrape_class.assert_called_once_with()
        mock_production_scrape_instance.get_production.assert_called_once_with("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano=2023")

        # Verifica se ProductionCSV FOI chamado
        mock_csv_class.assert_called_once_with()
        mock_production_csv_instance.get_production_csv.assert_called_once_with(
            expected_file_from_config, expected_category_from_config, test_year
        )

        # Verifica o resultado (deve vir do CSV)
        assert len(result) == 2
        assert result[0].name == "Tinto CSV"
        assert result[0].quantity == 1000.0
        assert result[1].name == "Branco CSV"
        assert result[1].quantity == 700.0