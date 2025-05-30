from bs4 import BeautifulSoup
import requests
from app.domain.value_objects.base_scrape import BaseScrapeValueObject


class BaseScrape:
    def __init__(self, url: str):
        self.url = url
        self.category = None

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

    def _find_table(self, soup: BeautifulSoup) -> BeautifulSoup:
        try:
            table = soup.find("table", class_="tb_dados")
            if not table:
                raise Exception("Tabela não encontrada.")
            return table
        except Exception as e:
            raise Exception(f"Erro ao procurar tabela: {e}")

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
        try:         
            response = requests.get(self.url, timeout=3600)            
            response.raise_for_status()
            html_content = response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao acessar a URL {self.url}")

        
        soup = BeautifulSoup(html_content, 'html.parser')
        table = self._find_table(soup)
        
        body = table.find("tbody")
        if not body:
            raise Exception("Não encontrei o corpo do html.")

        rows = body.find_all("tr")

        data_list = []
        current_category = None

        for row in rows:
            cells = row.find_all("td")

            if not cells:
                continue

            first_cell_classes = cells[0].get('class', []) 
            if "tb_item" in first_cell_classes:
                current_category = cells[0].get_text(strip=True)
            
            name = cells[0].get_text(strip=True)            

            if current_category != name:
                if len(cells) > 1: 
                    quantity_text = cells[1].get_text(strip=True)
                    quantity = self._clean_numeric_data(quantity_text)                        
                    value = 0.0 
                    if len(cells) > 2: 
                        value_text_source = cells[2].get_text(strip=True)
                        value = self._clean_numeric_data(value_text_source)
                    
                    data_list.append(
                        BaseScrapeValueObject(
                            category=current_category,
                            name=name,
                            quantity=quantity,
                            value=value,
                        )
                    )
                    pass

        return data_list