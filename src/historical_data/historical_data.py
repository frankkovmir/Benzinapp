from datetime import date, datetime, timedelta
import git
import os
import pandas as pd
from pathlib import Path
import re
import shutil

TODAYS_DATE = date.today()
TANKERKOENIG_PATH = Path(__file__).parents[2] / "data" / "tankerkoenig-data"
DATA_PATH = TANKERKOENIG_PATH.parent


def git_pull_tankerkoenig() -> str:
    """Führt einen git pull aus um die Tankerkönig Daten (csv) zu aktualisieren

    Returns:
        str: git pull Nachricht
    """
    # git Klasse zum kommunizieren mit dem git binary
    g = git.cmd.Git(TANKERKOENIG_PATH)
    # Pull ausführen
    return g.pull()


def get_csv_paths():
    """Wählt Pfade der csv Dateien, die sich in den Preis- und Stationsordnern befinden.

    Returns:
        list: Liste mit allen Pfaden zu den csv Dateien
    """
    # Pfade zu den Ordnern für Preise und Stationen
    prices_dir_path = TANKERKOENIG_PATH / f"prices"
    stations_dir_path = TANKERKOENIG_PATH / f"stations"

    # Die Ordner haben weitere Unterordner. Für beide werden alle csv Pfade in einer Liste gespeichert zusammengefügt
    prices_paths = list(prices_dir_path.rglob("*.csv*"))
    stations_paths = list(stations_dir_path.rglob("*.csv*"))
    csv_paths = prices_paths + stations_paths

    return csv_paths


def split_list(csv_paths: list) -> list:
    """Erstellt zwei Listen aus einer Liste mit Preis- und Stations-CSV-Pfaden
    Die einzelnen Listen beinhalten nur noch ausschließlich Pfade zu den Preis- bzw. Stations-CSVs

    Args:
        csv_paths (list): alle CSV Pfade der benötigten Daten

    Returns:
        list: zwei Listen
    """
    prices_paths = []
    stations_paths = []

    for path in csv_paths:
        if "prices" in path.parts[-1]:
            prices_paths.append(path)
        else:
            stations_paths.append(path)

    return prices_paths, stations_paths


def join_dataframes(prices_path: str, stations_path: str) -> pd.DataFrame:
    """Erstellt ein gemeinsames Dataframe mit Daten aus je einer Preis und Stations CSV
    Joint die Preis- und Stationsdaten über die uuid

    Args:
        prices_path (str): Pfad zur Preis CSV
        stations_path (str): Pfad zur Stations CSV

    Returns:
        pd.DataFrame: Zusammengefügtes Dataframe
    """
    # Jeweils ein Dataframe erstellen
    df_prices = pd.read_csv(prices_path, parse_dates=["date"])
    df_stations = pd.read_csv(stations_path, dtype={"post_code": "str"})

    # Auf uuids joinen
    df = df_prices.merge(df_stations, left_on="station_uuid", right_on="uuid", how="left")
    # Doppelte uuid entfernen
    df = df.drop(["uuid"], axis=1)

    return df


def create_bundesland_attribute(post_code: pd.Series) -> pd.Series:
    """Erstellt neues Attribut 'bundesland' mithilfe der PLZ und der Excel Datei, die deutsche PLZ zu den jeweiligen Bundesländern verbindet.

    Args:
        df (pd.Series): Spalte eines Dataframes mit PLZ Attribut

    Returns:
        pd.Series: Neue Spalte mit Bundesländern
    """
    # Dictionary mit PLZ als Key und Bundesland als Value
    plz_dict = dict(
        pd.read_excel(
            DATA_PATH / "Liste-der-PLZ-in-Excel-Karte-Deutschland-Postleitzahlen.xlsx",
            dtype={"PLZ": "str"},
            usecols=["PLZ", "Bundesland"],
        ).values
    )
    bundeslaender = post_code.map(plz_dict)

    return bundeslaender


def check_historical_data() -> bool:
    """Prüft ob bereits ein Datensatz für historische Daten vorhanden ist

    Returns:
        bool: True wenn der Datensatz bereits existiert
    """
    file_exists = os.path.exists(DATA_PATH / "historical_data.csv")
    return file_exists


def create_historical_dataframe(prices_paths: list, stations_paths: list) -> pd.DataFrame:
    """Erstellt ein aggregiertes Dataframe,
    wobei nach Bundesländern gruppiert wird und Mittelwerte für die Preise berechnet werden.

    Args:
        prices_paths (list): Liste mit den Pfaden der Preisdaten
        stations_paths (list): Liste mit den Pfaden der Stationsdaten

    Returns:
        pd.DataFrame: Aggregiertes Dataframe
    """
    # leeres df wird mit täglich aggregierten Werten gefüllt
    df = pd.DataFrame()

    for prices_path, stations_path in zip(prices_paths, stations_paths):
        # df mit gesamten Daten für einen Tag
        df_one_day = join_dataframes(prices_path, stations_path)
        # Bundesland Attribut hinzufügen
        df_one_day["bundesland"] = create_bundesland_attribute(df_one_day["post_code"])
        # Datum aus einer Spalte entnehmen
        date = df_one_day.iloc[0]["date"].date()
        # df nach Bundesländern gruppieren und Mittelwerte berechnen
        df_grouped = df_one_day.groupby("bundesland")[["diesel", "e5", "e10"]].mean().reset_index()
        # weitere Zeile für Bundesweite Mittelwerte
        bundesweit = pd.DataFrame(
            {
                "bundesland": "bundesweit",
                "diesel": df_one_day["diesel"].mean(),
                "e5": df_one_day["e5"].mean(),
                "e10": df_one_day["e10"].mean(),
            },
            index=[0],
        )
        df_grouped = pd.concat([df_grouped, bundesweit], ignore_index=True)
        # Datum hinzufügen
        df_grouped["date"] = date
        # Aggregierte Daten zum Dataframe hinzufügen
        df = pd.concat([df, df_grouped], ignore_index=True)

    return df


def initial_data_load():
    """Erstellt das Dataframe für die historischen Daten,
    die für das Dashboard verwendet werden
    """
    # alle CSV Pfade von ggf. 2 Jahren
    all_csv_paths = get_csv_paths()
    # Pfade für Preise und Stationen aufteilen
    prices_paths, stations_paths = split_list(all_csv_paths)
    # Dataframe erstellen
    df = create_historical_dataframe(prices_paths, stations_paths)
    df.to_csv(DATA_PATH / "historical_data.csv", encoding="utf-8", index=False)
    print("Historischer Datensatz wurde erstellt.")


def remove_old_data():
    """Überprüft ob in den Ordnern für Preise und Stationen Daten vorhanden sind,
    die ein Datum haben, welches weiter zurückliegt als der 24.01.19.
    Diese Daten müssen entfernt werden, da Stationsdaten erst ab diesem Zeitpunkt vorhanden sind.
    """
    # regex Muster für Datum
    pattern = r"\d{4}-\d{2}-\d{2}"

    dirs = ["prices", "stations"]
    for dir in dirs:
        # Preis- oder Stations-Ordner
        path = TANKERKOENIG_PATH / dir

        # Preis Daten im Jan 19 Ordner löschen, die älter als 24.01 sind
        if dir == "prices":
            jan_19_dir = path / "2019" / "01"
            files = os.listdir(jan_19_dir)
            date_limit = date(2019, 1, 24)
            for file in files:
                file_date = datetime.strptime(re.findall(pattern, file)[0], "%Y-%m-%d").date()
                if file_date < date_limit:
                    os.remove(jan_19_dir / file)

        # prices und stations haben multiple Unterordner die nur das jeweilige Jahr als Bezeichnung haben
        years_dirs = os.listdir(path)
        # Stations-Ordner hat außer den Unterordnern eine weitere Datei mit den aktuellen Stationen
        if dir == "stations":
            if "stations.csv" in years_dir:
                years_dirs.remove("stations.csv")

        for years_dir in years_dirs:
            # Ordner aus dem Jahr 2018 oder älter können komplett entfernt werden
            if int(years_dir) <= 2018:
                dir_to_remove = path / years_dir
                shutil.rmtree(dir_to_remove, ignore_errors=True)
                print(f"{dir_to_remove} erfolgreich gelöscht")


def check_historical_data_version() -> bool:
    """Prüft ob der Datensatz aktuell ist (neueste Daten immer vom Vortag)

    Returns:
        bool: True wenn der Datensatz aktuell ist
    """
    df = pd.read_csv(DATA_PATH / "historical_data.csv", parse_dates=["date"])
    # letztes Datum im Datensatz
    recent_date = df["date"].iloc[-1].date()
    # aktueller Datensatz hat Daten vom Vortag, timedelta.days muss also 1 sein
    if (TODAYS_DATE - recent_date).days == 1:
        return True
    else:
        return False


def list_date_difference() -> list:
    """Erstellt eine Liste mit Daten (hier plural Datum) mit allen Tagen nach
    dem letzten Datum im historischen Datensatz bis heute

    Returns:
        list: Liste mit den Daten, jedes Objekt in der Liste ist ein datetime.date
    """
    df = pd.read_csv(DATA_PATH / "historical_data.csv", parse_dates=["date"])
    # letztes Datum im Datensatz
    recent_date = df["date"].iloc[-1].date()
    # Liste mit allen Tagen nach recent_date bis gestern
    dates = [recent_date + timedelta(days=i) for i in range(1, (TODAYS_DATE - recent_date).days)]

    return dates


def update_historical_data():
    """Updatet den historischen Datensatz. Alle Daten der Tage seit dem letzten Update,
    die noch nicht aggregiert sind, werden dem Datensatz angehängt.
    """
    # Historischen Datensatz laden
    df = pd.read_csv(DATA_PATH / "historical_data.csv", parse_dates=["date"])
    # Alle Daten (Datum) die der historische Datensatz zurückliegt
    dates = list_date_difference()
    # zugehörige Pfade der benötigten CSV Dateien werden in Listen gespeichert
    prices_paths = []
    stations_paths = []

    for date in dates:
        year, month, day = date.year, date.month, date.day
        prices_path = (
            TANKERKOENIG_PATH
            / "prices"
            / str(year)
            / f"{month:02}"
            / f"{year}-{month:02}-{day:02}-prices.csv"
        )
        stations_path = (
            TANKERKOENIG_PATH
            / "stations"
            / str(year)
            / f"{month:02}"
            / f"{year}-{month:02}-{day:02}-stations.csv"
        )
        prices_paths.append(prices_path)
        stations_paths.append(stations_path)

    # neuen Teildatensatz erstellen der an den alten angefügt wird
    new_data = create_historical_dataframe(prices_paths, stations_paths)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_PATH / "historical_data.csv", encoding="utf-8", index=False)
    print("Historischer Datensatz wurde aktualisiert.")


def main():
    # Alte Daten löschen falls vorhanden
    remove_old_data()
    # Tankerkoenig Daten aktualisieren
    print(git_pull_tankerkoenig())
    # Historischen Datensatz erstellen falls nicht vorhanden
    # (Dauer: ca. 50min Stand: 03.01.23, getestet mit 8-Kerner Ryzen 7 5800x und CL16 3600MHz RAM)
    if not check_historical_data():
        initial_data_load()
    # Datensatz aktualisieren falls nicht aktuell
    if not check_historical_data_version():
        update_historical_data()


if __name__ == "__main__":
    main()
