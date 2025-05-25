from app.application.DTOs.production_response import ProductionResponse
import pandas as pd


class ProductionCSV:

    def get_production_csv(
        self, file_path, category, year
    ) -> list[ProductionResponse]:
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                ProductionResponse(
                    category=category,
                    name=str(row["produto"]),
                    quantity=int(row[f"{year}"])
                )
            )

        return data
    