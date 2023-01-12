from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')))
from ids import LINE_CHART, BUNDESLAND_DROPDOWN, YEAR_DROPDOWN, FUEL_DROPDOWN
from loader import DataSchema

def render_line_chart(app: Dash, data: pd.DataFrame) -> html.Div:

    @app.callback(Output(LINE_CHART, 'children'),
                  [Input(YEAR_DROPDOWN, 'value'),
                   Input(BUNDESLAND_DROPDOWN, 'value'),
                   Input(FUEL_DROPDOWN, 'value')])

    def update_line_chart(years: list, bundeslaender: list, fuels: list) -> html.Div:
        # df filtern nach den Bundesländern und Jahren die im Dropdown ausgewählt sind
        filtered_df = data.query('year in @years and bundesland in @bundeslaender')
        if filtered_df.shape[0] == 0:
            return html.Div('Keine Daten ausgewählt oder Daten nicht verfügbar.')

        # Plot erstellen
        fig = px.line(filtered_df,
                      x=DataSchema.DATE,
                      y=[fuel.lower() for fuel in fuels],
                      color=DataSchema.BUNDESLAND,
                      labels={
                          DataSchema.DATE: 'Datum',
                          DataSchema.VALUE: 'Kraftstoffpreis [€]',
                          DataSchema.BUNDESLAND: 'Bundesland',
                          'variable': 'Kraftstoff'
                      })
        return html.Div(dcc.Graph(figure=fig), id=LINE_CHART)

    return html.Div(id=LINE_CHART)

