import pytest
from unittest.mock import patch, MagicMock, call
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from app.infrastructure.external_services.base_scrape import BaseScrape
from app.domain.value_objects.base_scrape import BaseScrapeValueObject


def test_clean_numeric_data():
    """Testa a limpeza e conversão de dados numéricos."""
    scraper = BaseScrape(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")

    assert scraper._clean_numeric_data("1.234,56") == 1234.56
    assert scraper._clean_numeric_data("500,3 KG") == 500.3
    assert scraper._clean_numeric_data("R$ 75,50") == 75.50
    assert scraper._clean_numeric_data("-") == 0.0

    with pytest.raises(ValueError):
        scraper._clean_numeric_data("invalid_text")


def test_get_category():
    """Testa a lógica de obtenção de categoria."""
    scraper = BaseScrape(url="hhttp://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")
    mock_cell_item = MagicMock(spec=WebElement)
    mock_cell_item.get_attribute.return_value = "tb_item"
    mock_cell_item.text = "VINHO DE MESA"

    mock_cell_dados = MagicMock(spec=WebElement)
    mock_cell_dados.get_attribute.return_value = "tb_dados"
    mock_cell_dados.text = "Tinto"

    # Cenário 1: Célula é um item de categoria
    category = scraper._get_category([mock_cell_item, MagicMock()])
    assert category == "VINHO DE MESA"
    assert (
        scraper.category == "VINHO DE MESA"
    )  # Verifica se o estado interno foi atualizado

    # Cenário 2: Célula não é item de categoria, deve usar categoria anterior
    scraper.category = "EXISTING CATEGORY"  # Define um estado anterior
    category_dados = scraper._get_category([mock_cell_dados, MagicMock()])
    assert category_dados == "EXISTING CATEGORY"


def test_get_name():
    """Testa a lógica de obtenção de nome."""
    scraper = BaseScrape(url="http://dummy.com")
    mock_cell = MagicMock(spec=WebElement)
    mock_cell.text = " Cabernet Sauvignon "

    name = scraper._get_name(
        [mock_cell, MagicMock()]
    )  # Passa uma lista de células mockadas
    assert name == " Cabernet Sauvignon "  # _get_name não faz strip no seu código atual


@pytest.fixture
def mock_driver():
    """Fixture para mockar o driver do Selenium e seus métodos."""
    driver = MagicMock()

    # Mock para a tabela e suas partes
    mock_table_element = MagicMock(spec=WebElement)
    mock_tbody_element = MagicMock(spec=WebElement)

    # Mock para as linhas e células
    # Linha 1 (Categoria)
    mock_row1_cell1 = MagicMock(spec=WebElement)
    mock_row1_cell1.get_attribute.return_value = "tb_item"  # É uma célula de categoria
    mock_row1_cell1.text = "VINHOS DE MESA"
    mock_row1_cell2 = MagicMock(spec=WebElement)
    mock_row1_cell2.text = "1.234"  # Quantidade
    mock_row1 = MagicMock(spec=WebElement)
    mock_row1.find_elements.return_value = [mock_row1_cell1, mock_row1_cell2]

    # Linha 2 (Produto sob a categoria da Linha 1)
    mock_row2_cell1 = MagicMock(spec=WebElement)
    mock_row2_cell1.get_attribute.return_value = "tb_dados"  # Não é célula de categoria
    mock_row2_cell1.text = "Tinto"
    mock_row2_cell2 = MagicMock(spec=WebElement)
    mock_row2_cell2.text = "5.678,90"
    mock_row2_cell3 = MagicMock(
        spec=WebElement
    )  # Para simular uma terceira célula de 'valor'
    mock_row2_cell3.text = "10.000,50"
    mock_row2 = MagicMock(spec=WebElement)
    mock_row2.find_elements.return_value = [
        mock_row2_cell1,
        mock_row2_cell2,
        mock_row2_cell3,
    ]

    # Linha 3 (Outra categoria)
    mock_row3_cell1 = MagicMock(spec=WebElement)
    mock_row3_cell1.get_attribute.return_value = "tb_item"
    mock_row3_cell1.text = "ESPUMANTES"
    mock_row3_cell2 = MagicMock(spec=WebElement)
    mock_row3_cell2.text = "100"
    mock_row3 = MagicMock(spec=WebElement)
    mock_row3.find_elements.return_value = [mock_row3_cell1, mock_row3_cell2]

    mock_tbody_element.find_elements.return_value = [mock_row1, mock_row2, mock_row3]
    mock_table_element.find_element.return_value = mock_tbody_element
    driver.find_element.return_value = mock_table_element  # Isso é para _find_table

    return driver


# Patch para webdriver.Chrome e ChromeDriverManager
@patch("app.infrastructure.external_services.base_scrape.webdriver.Chrome")
@patch("app.infrastructure.external_services.base_scrape.ChromeDriverManager")
def test_handle_success(mock_driver_manager, mock_chrome_webdriver, mock_driver):
    """Testa o método handle em um cenário de sucesso com dados mockados."""
    # Configura os mocks para serem retornados quando chamados
    mock_chrome_webdriver.return_value = (
        mock_driver  # _initialize_driver chamará webdriver.Chrome(...)
    )
    mock_driver_manager.return_value.install.return_value = (
        "/mocked/driver/path"  # Para Service()
    )

    # Arrange
    test_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    scraper = BaseScrape(url=test_url)

    # Act
    results = scraper.handle()

    # Assert
    # Verifica se o driver foi inicializado e a URL foi acessada
    mock_chrome_webdriver.assert_called_once() 
    mock_driver.get.assert_called_once_with(test_url)

    # Verifica se a tabela foi procurada corretamente
    mock_driver.find_element.assert_called_with(By.CSS_SELECTOR, "table.tb_dados")

    assert len(results) == 1
    assert isinstance(results[0], BaseScrapeValueObject)
    assert (
        results[0].category == "VINHOS DE MESA"
    ) 
    assert results[0].name == "Tinto"
    assert results[0].quantity == 5678.90
    assert results[0].value == 5678.90 

    # Verifica se o driver foi fechado
    mock_driver.quit.assert_called_once()


@patch("app.infrastructure.external_services.base_scrape.webdriver.Chrome")
@patch("app.infrastructure.external_services.base_scrape.ChromeDriverManager")
def test_handle_find_table_raises_exception(
    mock_driver_manager, mock_chrome_webdriver, mock_driver
):
    """Testa o tratamento de erro quando a tabela não é encontrada."""
    mock_chrome_webdriver.return_value = mock_driver
    mock_driver_manager.return_value.install.return_value = "/mocked/driver/path"

    mock_driver.find_element.side_effect = Exception("Table not found by CSS selector")

    scraper = BaseScrape(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")

    with pytest.raises(
        Exception, match="Error finding table: Table not found by CSS selector"
    ):
        scraper.handle()

    mock_driver.get.assert_called_once_with("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")
    mock_driver.find_element.assert_called_once_with(By.CSS_SELECTOR, "table.tb_dados")
