class UrlHandler:
    def url_handler(self, url: str, year: int) -> str:
        urlQuery = ""
        if year is not None:
            urlQuery = f"{url}&ano={year}"

        return urlQuery
