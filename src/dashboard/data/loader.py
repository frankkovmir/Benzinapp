import pandas as pd


class DataSchema:
    DIESEL_PRICE = "diesel"
    E5_PRICE = "e5"
    E10_PRICE = "e10"
    BUNDESLAND = "bundesland"
    DATE = "date"
    YEAR = "year"
    VALUE = "value"


def load_data(path: str) -> pd.DataFrame:
    """Historischen Datensatz als Pandas Dataframe laden
    und Spalte für 'Jahr' erstellen

    Args:
        path (str): Pfad zum historischen Datensatz

    Returns:
        pd.DataFrame: Historischer Datensatz als Dataframe
    """
    # Dataframe laden
    df = pd.read_csv(path, parse_dates=[DataSchema.DATE])
    # neue Spalten für Jahr erstellen damit darauf gefiltert werden kann
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)

    return df
