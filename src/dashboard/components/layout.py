from dash import Dash, html
import pandas as pd
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
from bundeslaender_dropdown import render_bundeslaender_dropdown
from year_dropdown import render_year_dropdown
from fuel_dropdown import render_fuel_dropdown
from line_chart import render_line_chart


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    """Erstellt das Layout für die Dash Applikation

    Args:
        app (Dash): Dash app

    Returns:
        html.Div: Div mit gefüllten Informationen
    """
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="fuel-dropdown-container", children=[render_fuel_dropdown(app, data)]
            ),
            html.Div(
                className="bundeslaender-dropdown-container",
                children=[render_bundeslaender_dropdown(app, data)],
            ),
            html.Div(
                className="year-dropdown-container", children=[render_year_dropdown(app, data)]
            ),
            render_line_chart(app, data),
        ],
    )
