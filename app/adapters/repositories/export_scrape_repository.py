from use_cases.entities.export_target import ExportTarget


class ExportScrapeRepository:

    def get_export_target(self) -> list[ExportTarget]:
        return [
            ExportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_06",
                "Vinhos de Mesa",
            ),
            ExportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06",
                "Espumantes",
            ),
            ExportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06",
                "Uvas Frescas",
            ),
            ExportTarget(
                "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_06",
                "Suco de Uva",
            ),
        ]
