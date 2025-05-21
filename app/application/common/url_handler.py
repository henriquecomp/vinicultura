class UrlHandler:
    def url_handler(self, url: str, year: int) -> str:
        """
        Método que trata a URL para realizar a raspagem de dados no site da embrapa
        conforme parametros de entrada no endpoint

        Args:
            url: str, # Url onde deseja raspar os dados
            year: str, # Caso contenha o ano, concatena na URL para filtrar e raspar os dados

        Returns:
            str: Url tratada para o componente de raspagem de dados consumir.           

        Raises:
            
        """         
        urlQuery = url
        if year is not None:
            urlQuery = f"{url}&ano={year}"

        return urlQuery
