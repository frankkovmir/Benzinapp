from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from ids import FUEL_DROPDOWN, SELECT_ALL_FUELS_BUTTON


def render_fuel_dropdown(app: Dash, data: pd.DataFrame) -> html.Div:

    all_fuels = ["Diesel", "E5", "E10"]

    @app.callback(Output(FUEL_DROPDOWN, "value"), Input(SELECT_ALL_FUELS_BUTTON, "n_clicks"))
    def select_all_fuels(_: int) -> list:
        return all_fuels

    # div gefüllt mit Infos zum Header, Dropdown Menü und Button
    div = html.Div(
        children=[
            html.H6("Kraftstoff"),
            dcc.Dropdown(
                id=FUEL_DROPDOWN,
                options=[{"label": fuel, "value": fuel} for fuel in all_fuels],
                value=all_fuels,
                placeholder="Kraftstoff auswählen",
                multi=True,
            ),
            html.Button(
                className="fuel-dropdown-button",
                children=["Alle auswählen"],
                id=SELECT_ALL_FUELS_BUTTON,
            ),
        ]
    )

    return div
