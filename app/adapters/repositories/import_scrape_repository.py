from use_cases.entities.import_target import ImportTarget


class ImportScrapeRepository:

    def get_import_target(self) -> list[ImportTarget]:
        return [
            ImportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_05",
                "Vinhos de Mesa",
            ),
            ImportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05",
                "Espumantes",
            ),
            ImportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05",
                "Uvas Frescas",
            ),
            ImportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05",
                "Uvas Passas",
            ),
            ImportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05",
                "Suco de Uva",
            ),
        ]
