from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from app.domain.value_objects.base_scrape import BaseScrapeValueObject


class BaseScrape:
    def __init__(self, url: str):
        self.url = url
        self.category = None

    def _initialize_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def _clean_numeric_data(self, text: str) -> float:
        try:
        
            if not text or text.lower().strip() in ("-", " "):
                return 0.0

            saida = float(
                text.lower()
                .replace(".", "")
                .replace(",", ".")
                .replace(" ", "")
                .replace("r$", "")
                .replace("kg", "")
                .replace("-", "0")
                .strip()
            )

            return saida
  
        except ValueError:
            raise

    def _get_category(self, cells: list[WebElement]) -> str:
        if cells[0].get_attribute("class") == "tb_item":
            self.category = cells[0].text

        return self.category

    def _get_name(self, cells: list[WebElement]) -> str:
        return cells[0].text

    def _find_table(self, driver: webdriver.Chrome) -> WebElement:
        try:
            table = driver.find_element(By.CSS_SELECTOR, "table.tb_dados")
            return table
        except Exception as e:
            raise Exception(f"Error finding table: {e}")

    def handle(self) -> list[BaseScrapeValueObject]:
        """
        Serviço que faz o scrape de dados genérico 
        utilizando a URL enviada via construtor
        o site é o da vinicultura da embrapa.
        Caso seja informado outro deverá ocorrer erros.

        Args:
            

        Returns:
            list[BaseScrapeValueObject]: Dados do usuário criado:
                {
                    category: str, # categoria do produto
                    name: str, # nome do produto
                    quantity: float, # quantidade do produto
                    value: float # valor do produto em dolar
                }

        Raises:
            

        """
        driver = self._initialize_driver()
        driver.get(self.url)

        table = self._find_table(driver)
        body = table.find_element(By.TAG_NAME, "tbody")
        rows = body.find_elements(By.TAG_NAME, "tr")

        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            category = self._get_category(cells)
            name = self._get_name(cells)
            if category != name:
                data.append(
                    BaseScrapeValueObject(
                        category=category,
                        name=name,
                        quantity=self._clean_numeric_data(cells[1].text),
                        value=(
                            self._clean_numeric_data(cells[1].text)
                            if len(cells) > 2
                            else 0.0
                        ),
                    ),
                )

        driver.quit()
        return data
