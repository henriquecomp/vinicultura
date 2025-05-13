import json
import jmespath
from application.DTOs.config_response import ConfigResponse


class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = {}
        self._load_config()

    def _load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            print(f"Arquivo de configuração {self.config_file} não encontrado.")
        except json.JSONDecodeError:
            print(f"Não foi possível decodificar o arquivo {self.config_file}.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def get_config(self, name: str) -> list[ConfigResponse]:
        safe_name = name.replace("'", "\\'")
        query = f"[?name == '{safe_name}'].item[]"
        results = jmespath.search(query, self.config)
        data = []
        for item in results:
            data.append(
                ConfigResponse(
                    category=item["category"],
                    url=item["url"], 
                    file=item["file"]
                )
            )
        return data
