from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from interfaces.schemas.responses.export_response import ExportResponse
from adapters.repositories.export_scrape_repository import ExportScrapeRepository


class ExportScrape:

    def execute(
        self,
    ) -> list[ExportResponse]:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        repository = ExportScrapeRepository()
        targets = repository.get_export_target()

        data = []

        for target in targets:
            driver.get(target.url)
            table = driver.find_element(By.CSS_SELECTOR, "table.tb_dados")
            body = table.find_element(By.TAG_NAME, "tbody")
            rows = body.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                data.append(
                    ExportResponse(
                        grupo=target.grupo,
                        pais=str(cells[0].text),
                        quantidade=float(
                            str(cells[1].text)
                            .replace(".", "")
                            .replace(" ", "")
                            .replace("kg", "")
                            .replace("-", "0")
                        ),
                        valor=float(
                            str(cells[2].text)
                            .replace(".", "")
                            .replace(" ", "")
                            .replace("kg", "")
                            .replace("-", "0")
                        ),
                    )
                )

        driver.quit()
        return data
