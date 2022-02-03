from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

from jbi100_app.views.shared import field_to_title


# Horizontal segmented bar chart with categorical features and color divisions
# if year is passed then only use that year (must be a number)
# https://plotly.com/python/horizontal-bar-charts/
class HorizontalBar(html.Div):
    def __init__(self, name, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_year = 'accident_year'
        self.feature_y = 'cost'

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    # Value feature for colors, category feature for bars
    # https://plotly.com/python/bar-charts/
    def update(self, category_feature):
        print("start: updating plot")
        start = time.time()
        df = self.df
        fig = px.histogram(df, x=category_feature, y='cost')
        print(f"done: updating {self.html_id} plot in {time.time() - start:.2f}s")
        return fig
