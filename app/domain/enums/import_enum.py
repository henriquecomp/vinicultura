from enum import Enum


class ImportEnum(str, Enum):
    VINHOS_DE_MESA = "Vinhos de Mesa"
    ESPUMANTES = "Espumantes"
    UVAS_FRESCAS = "Uvas Frescas"
    UVAS_PASSAS = "Uvas Passas"
    SUCO_DE_UVA = "Suco de Uva"
