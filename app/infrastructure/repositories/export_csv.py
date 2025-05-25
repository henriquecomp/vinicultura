from app.application.DTOs.export_response import ExportResponse
import pandas as pd


class ExportCSV:

    def get_export_by_year_csv(
        self, file_path, category, year
    ) -> list[ExportResponse]:
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                ExportResponse(
                    category=category,
                    country=str(row["País"]),
                    quantity=int(row[f"Qtd {year}"]),
                    value=int(row[f"Val {year}"])
                )
            )

        return data
