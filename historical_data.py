import git
from pathlib import Path
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import re
import pandas as pd

TODAYS_DATE = date.today()
GIT_PATH = Path(__file__).parent / 'tankerkoenig-data'

def git_pull_tankerkoenig() -> str:
    """Führt einen git pull aus um die Tankerkönig Daten (csv) zu aktualisieren

    Returns:
        str: git pull Nachricht
    """
    # git Klasse zum kommunizieren mit dem git binary
    g = git.cmd.Git(GIT_PATH)
    # Pull ausführen
    return g.pull()


def check_new_year():
    """Prüft ob heute der erste Tag des Jahres ist

    Returns:
        bool: True nur am 01 Jan jeden Jahres
    """

    month_day = TODAYS_DATE.strftime('%m-%d')

    # True zurückgeben wenn der erste Tag des Jahres ist
    if month_day == '01-01':
        return True
    else:
        return False


def get_csv_paths():
    """Wählt Pfade der csv Dateien, die sich in den Ordnern für dieses und letztes Jahr befinden.
    Ausnahme wenn die Funktion am Neujahrstag ausgeführt wird, da dann nur die Ordner für das Vorjahr benötigt werden.

    Returns:
        list: Liste mit allen Pfaden zu den csv Dateien
    """
    # Zu Neujahr wird nur der jeweilige Ordner zum Vorjahr benötigt
    if check_new_year():
        # Pfade zu den Ordnern für Preise und Stationen
        prices_dir_path = GIT_PATH / f'prices/{TODAYS_DATE.year-1}'
        stations_dir_path = GIT_PATH / f'stations/{TODAYS_DATE.year-1}'
        # Die Ordner haben weitere Unterordner. Für beide werden alle csv Pfade in einer Liste gespeichert zusammengefügt
        prices_paths = list(prices_dir_path.rglob('*.csv*'))
        stations_paths = list(stations_dir_path.rglob('*.csv*'))
        csv_paths = prices_paths + stations_paths
        return csv_paths

    # An jedem anderen Tag werden Ordner für je das aktuelle und das Vorjahr benötigt
    prices_dir_paths = [GIT_PATH / f'prices/{TODAYS_DATE.year-1}', GIT_PATH / f'prices/{TODAYS_DATE.year}']
    stations_dir_paths = [GIT_PATH / f'stations/{TODAYS_DATE.year-1}', GIT_PATH / f'stations/{TODAYS_DATE.year}']
    dir_paths = prices_dir_paths + stations_dir_paths

    csv_paths = []
    # Über alle Ordner Pfade iterieren und die Listen mit den csv Pfaden hinzufügen
    for dir in dir_paths:
        csv_paths.extend(list(dir.rglob('*.csv*')))
    return csv_paths


def one_year_data_limit(csv_paths: list) -> list:
    """Erstellt eine neue Liste mit den Pfaden, die ein Datum haben, welches höchstens ein Jahr zurück liegt

    Args:
        csv_paths (list): Enthält die Pfade, welche mit get_csv_paths generiert wurden

    Returns:
        list: Neue Liste mit gefilterten Pfaden
    """
    # Datum heute vor einem Jahr
    one_year_ago = TODAYS_DATE - relativedelta(years=1)

    # Keine Anpassung nötig wenn Neujahrstag ist
    if check_new_year():
        return csv_paths

    # regex muster für Datum
    pattern_date_time = r'([0-9]{4}-[0-9]{2}-[0-9]{2})'

    new_paths = []
    for path in csv_paths:
        # Gibt den letzten Teil (hinter letztem Backslash) des des Pfads als str zurück
        path_substr = path.parts[-1]
        # Davon mit regex das Datum filtern und in ein date Objekt verwandeln
        path_date = datetime.strptime(re.findall(pattern_date_time, path_substr)[0], '%Y-%m-%d').date()
        # Elemente mit Datum vor max. einem Jahr werden in die neue Liste aufgenommen
        if path_date >= one_year_ago:
            new_paths.append(path)

    return new_paths


def split_list(csv_paths: list) -> list:
    """Erstellt zwei Listen innerhalb einer Liste
    Die einzelnen Listen haben nur noch Preise oder Stationen

    Args:
        csv_paths (list): _description_

    Returns:
        list: _description_
    """
    prices_paths = []
    stations_paths = []

    for path in csv_paths:
        if 'prices' in path.parts[-1]:
            prices_paths.append(path)
        else:
            stations_paths.append(path)

    return prices_paths, stations_paths


def create_dataframe(prices_paths: list, stations_paths: list) -> pd.DataFrame:
    """Erstellt das Dataframe aus allen Paths
    Joint die Preis- und Stationsdaten über die uuid

    Args:
        splitted_csv_paths (list): Liste mit zwei Sublisten die jeweils ausschließlich Pfade zu Preis- bzw. Stationsdaten enthalten

    Returns:
        pd.DataFrame: Zusammengefügtes Dataframe
    """
    # Jeweils ein Dataframe erstellen
    df_prices = pd.concat((pd.read_csv(prices_path, parse_dates=['date']) for prices_path in prices_paths), ignore_index=True)
    df_stations = pd.concat((pd.read_csv(stations_path) for stations_path in stations_paths), ignore_index=True)

    # Auf uuids joinen
    df = df_prices.merge(df_stations, left_on = 'station_uuid', right_on = 'uuid', how = 'left')
    # Doppelte uuid entfernen
    df.drop(['uuid'], axis=1, inplace=True)

    return df


def main():
    print(git_pull_tankerkoenig())
    all_csv_paths = get_csv_paths()
    csv_paths = one_year_data_limit(all_csv_paths)
    prices_paths, stations_paths = split_list(csv_paths)
    df = create_dataframe(prices_paths[:2], stations_paths[:2])
    return df


if __name__ == '__main__':
    main()