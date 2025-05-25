from app.application.DTOs.commercialization_response import CommercializationResponse
import pandas as pd


class CommercializationCSV:

    def get_commercialization_csv(
        self, file_path, category, year
    ) -> list[CommercializationResponse]:
        df = pd.read_csv(file_path, delimiter=";")
        data = []
        for _, row in df.iterrows():
            data.append(
                CommercializationResponse(
                    category=category,
                    name=str(row["Produto"]),
                    quantity=int(row[f"{year}"])
                )
            )

        return data
