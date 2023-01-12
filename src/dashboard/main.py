"""Der Code zum Erstellen des Dashboards ist angelehnt an das Tutorial vom Youtuber ArjanCodes
Quelle: https://www.youtube.com/watch?v=XOFrvzWFM7Y&t=438s&ab_channel=ArjanCodes"""

from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from pathlib import Path
import sys
import os

sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "components"))
)
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")))
from layout import create_layout
from loader import load_data
from colorama import init as colorama_init

DATA_PATH = Path(__file__).parents[2] / "data" / "historical_data.csv"

try:
    colorama_init()
    print("~" * 80)
    print(
        "\x1b[6;30;42m"
        + "This Dashboard is running from the Application 'Fuel Guru'.\nCopyright: Sam Barjesteh, "
        "Hicham Ben Ayoub, "
        "Frank Kovmir, Sven Simon Szczesny."
        "\nAny kind of distribution is prohibited without previous consent." + "\x1b[0m"
    )
    print("~" * 80)
    print("\n" * 3)
    data = load_data(DATA_PATH)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Historische Daten Dashboard"
    app.layout = create_layout(app, data)
    app.run()
except Exception as e:
    print(e)
