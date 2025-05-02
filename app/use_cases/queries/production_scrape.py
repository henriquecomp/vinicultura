from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from interfaces.schemas.responses.production_response import ProductionResponse


class ProductionScrape:
    def execute(self) -> list[ProductionResponse]:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")
        table = driver.find_element(By.CSS_SELECTOR, "table.tb_dados")
        body = table.find_element(By.TAG_NAME, "tbody")
        rows = body.find_elements(By.TAG_NAME, "tr")

        data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells[0].get_attribute("class") == "tb_item":
                grupo = cells[0].text

            data.append(
                ProductionResponse(
                    grupo=grupo,
                    nome=(
                        ""
                        if cells[0].get_attribute("class") == "tb_item"
                        else cells[0].text
                    ),
                    quantidade=float(
                        str(cells[1].text)
                        .replace(".", "")
                        .replace(" ", "")
                        .replace("kg", "")
                        .replace("-", "0")
                    ),
                )
            )

        driver.quit()
        return data
