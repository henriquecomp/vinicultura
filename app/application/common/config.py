import json
import jmespath
import logging
from application.DTOs.config_response import ConfigResponse

logger = logging.getLogger(__name__)



class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = {}
        self._load_config()

    def _load_config(self):
        """
        Método privado no qual carrega as configurações de URLs
        Atribui na self.config o json decodificado das configurações das URLs

        Args:
            

        Returns:
            

        Raises:
            HTTPException: Se o usuário ou senha forem inválidos.
        """
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            raise Exception(status_code=500, detail="Houve uma falha crítica do sistema ao ler um arquivo de configuração!")            
        except json.JSONDecodeError:
            raise Exception(status_code=500, detail="Houve uma falha crítica do sistema ao decodificar o arquivo de configuração!")                    
        except Exception as e:
            raise Exception(status_code=500, detail="Houve uma falha crítica do sistema ao ler/decodificar o arquivo de configuração!")            
            

    def get_config(self, name: str) -> list[ConfigResponse]:
        """
        Método que retorna os dados de uma configuração solicitada.    

        Args:
            name: str, # Nome da sessão que deseja recuperar as informações

        Returns:
            list: Uma lista de configurações seguindo a estrutura:
                [
                    {
                        "category": str, # categoria do produto
                        "url": str, # Url da sessão solicitada
                        "file": str, # Caminho do arquivo caso haja alguma falha de raspagem de dados    
                    }
                ]            

        Raises:
            
        """        
        safe_name = name.replace("'", "\\'")
        query = f"[?name == '{safe_name}'].item[]"
        results = jmespath.search(query, self.config)
        data = []
        for item in results:
            data.append(
                ConfigResponse(
                    category=item["category"], url=item["url"], file=item["file"]
                )
            )
        return data
