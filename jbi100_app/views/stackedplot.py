from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

from jbi100_app.views.shared import field_to_title


# Stacked line graph over time, with categorical feature and cost
# https://plotly.com/python/filled-area-plots/
class Stackedplot(html.Div):
    def __init__(self, name, feature, df, value_label='cost'):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_color = feature
        self.feature_x = 'accident_year'
        self.feature_y = 'cost'
        self.value_label = value_label

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, feature):
        print("start: updating plot")
        start = time.time()
        self.feature_color = feature
        costs = {}
        for val in self.df[self.feature_color].unique():
            costs[val] = {}
            for year in sorted(self.df[self.feature_x].unique()):
                costs[val][year] = self.df[
                    (self.df[self.feature_x] == year) &
                    (self.df[self.feature_color] == val)
                    # TODO & filter out unknown values (9?)
                ][self.feature_y].sum()
        fig = px.area(pd.DataFrame(costs),
                      labels={'value': field_to_title(self.value_label),
                              'index': field_to_title(self.feature_x),
                              'variable': field_to_title(self.feature_color)})
        print(f"done: updating {self.html_id} plot in {time.time() - start:.2f}s")
        return fig
