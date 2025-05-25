from enum import Enum


class ProcessingEnum(str, Enum):
    VINIFERAS = "Viniferas"
    AMERICANAS_E_HIBRIDAS = "Americanas e Hibridas"
    UVAS_DE_MESA = "Uvas de Mesa"
    SEM_CLASSIFICACAO = "Sem Classificacao"
