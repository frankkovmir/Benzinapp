import pandas as pd



class DataSchema:
    DIESEL_PRICE = 'diesel'
    E5_PRICE = 'e5'
    E10_PRICE = 'e10'
    BUNDESLAND = 'bundesland'
    DATE = 'date'
    YEAR = 'year'

def load_data(path: str) -> pd.DataFrame:
    # Dataframe laden
    df = pd.read_csv(path, parse_dates=[DataSchema.DATE])
    # neue Spalten für Jahr und Monat erstellen damit darauf gefiltert werden kann
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)

    return df