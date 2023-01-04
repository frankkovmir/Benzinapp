"""Der Code zum Erstellen des Dashboards ist angelehnt an das Tutorial vom Youtuber ArjanCodes
Quelle: https://www.youtube.com/watch?v=XOFrvzWFM7Y&t=438s&ab_channel=ArjanCodes"""

from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from pathlib import Path
import sys
import os
import multiprocessing
import time


sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'components')))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')))
from layout import create_layout
from loader import load_data

DATA_PATH = Path(__file__).parents[1] / 'historical_data.csv'

def test():

    data = load_data(DATA_PATH)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = 'Historische Daten Dashboard'
    app.layout = create_layout(app, data)
    app.run()


if __name__ == "__main__":
    try:
        p = multiprocessing.Process(target=test, name="test")
        p.start()
        time.sleep(600000)

        # Terminate foo
        p.terminate()

        # Cleanup
        p.join()
    except:
        p.terminate()