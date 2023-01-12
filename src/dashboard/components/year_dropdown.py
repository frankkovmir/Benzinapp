from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(
    os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"))
)
from ids import YEAR_DROPDOWN, SELECT_ALL_YEARS_BUTTON
from loader import DataSchema


def render_year_dropdown(app: Dash, data: pd.DataFrame) -> html.Div:

    all_years = list(data[DataSchema.YEAR].unique())

    @app.callback(Output(YEAR_DROPDOWN, "value"), Input(SELECT_ALL_YEARS_BUTTON, "n_clicks"))
    def select_all_years(_: int) -> list:
        return all_years

    # div gefüllt mit Infos zum Header, Dropdown Menü und Button
    div = html.Div(
        children=[
            html.H6("Jahr"),
            dcc.Dropdown(
                id=YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in all_years],
                value=all_years,
                placeholder="Jahr auswählen",
                multi=True,
            ),
            html.Button(
                className="year-dropdown-button",
                children=["Alle auswählen"],
                id=SELECT_ALL_YEARS_BUTTON,
            ),
        ]
    )

    return div
