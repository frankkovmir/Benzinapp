"""Der Code zum Erstellen des Dashboards ist angelehnt an das Tutorial vom Youtuber ArjanCodes
Quelle: https://www.youtube.com/watch?v=XOFrvzWFM7Y&t=438s&ab_channel=ArjanCodes"""

from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from pathlib import Path
import webbrowser
import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'components')))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')))
from layout import create_layout
from loader import load_data



path = Path().absolute()
DATA_PATH = f'{path}\historical_data\historical_data.csv'
# def start_dashboard():
try:
    data = load_data(DATA_PATH)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = 'Historische Daten Dashboard'
    app.layout = create_layout(app, data)
    app.run()
    webbrowser.open_new('http://127.0.0.1:8050')
except Exception as e:
    print(e)