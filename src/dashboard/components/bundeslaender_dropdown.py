from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
)
from ids import BUNDESLAND_DROPDOWN, SELECT_ALL_BUNDESLAENDER_BUTTON
from loader import DataSchema


def render_bundeslaender_dropdown(app: Dash, data: pd.DataFrame) -> html.Div:
    """Zuständig zum Rendern des Bundesländer-Dropdowns und verarbeiten der Daten

    Args:
        app (Dash): Dash app, die in main erstellt wird
        data (pd.DataFrame): Historische Daten

    Returns:
        html.Div: Bundesländer-Dropdown als Div
    """
    # alle Bundesländer des historischen Datensatzes als Liste
    all_bundeslaender = list(data[DataSchema.BUNDESLAND].unique())
    # Kommunikation über Callsbacks in Dash, ändert die Werte im dcc.Dropdown
    @app.callback(
        Output(BUNDESLAND_DROPDOWN, "value"), Input(SELECT_ALL_BUNDESLAENDER_BUTTON, "n_clicks")
    )  # bedeutet wenn geklickt wird und die Nummer sich ändert, wird dieser Callback gecallt

    # Argumente die in dieser Funktion landen sind die Inputs (n_clicks) aber der eigentliche Wert interessiert nicht
    # Callback soll nur gecallt werden wenn Button gedrückt wird
    def select_all_bundeslaender(_: int) -> list:
        return all_bundeslaender

    # div gefüllt mit Infos zum Header, Dropdown Menü und Button
    div = html.Div(
        children=[
            html.H6("Bundesland"),
            dcc.Dropdown(
                id=BUNDESLAND_DROPDOWN,
                options=[
                    {"label": bundesland, "value": bundesland} for bundesland in all_bundeslaender
                ],
                value=all_bundeslaender,
                placeholder="Bundesland auswählen",
                multi=True,
            ),
            html.Button(
                className="bundesland-dropdown-button",
                children=["Alle auswählen"],
                id=SELECT_ALL_BUNDESLAENDER_BUTTON,
            ),
        ]
    )

    return div
