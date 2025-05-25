from app.application.DTOs.import_response import ImportResponse
import pandas as pd


class ImportCSV:

    def get_import_by_year_csv(
        self, file_path, category, year
    ) -> list[ImportResponse]:
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                ImportResponse(
                    category=category,
                    country=str(row["País"]),
                    quantity=int(row[f"Qtd {year}"]),
                    value=int(row[f"Val {year}"])
                )
            )

        return data
