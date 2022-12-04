import git
from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta

TODAYS_DATE = date.today()
GIT_PATH = Path(__file__).parent / 'tankerkoenig-data'

def git_pull_tankerkoenig() -> str:
    """Führt einen git pull aus um die Tankerkönig Daten (csv) zu aktualisieren

    Returns:
        str: git pull Nachricht
    """
    # Pfad zum Tankerkönig Repository
    GIT_PATH = Path(__file__).parent / 'tankerkoenig-data'

    # git Klasse zum kommunizieren mit dem git binary
    g = git.cmd.Git(GIT_PATH)

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

def one_year_data_limit(prices_paths: list, stations_paths: list) -> list:
    
    one_year_ago = TODAYS_DATE - relativedelta(years=1)
    pass

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

