from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
from collections import namedtuple

from jbi100_app.views.shared import field_to_title

SectionsClass = namedtuple('SectionsClass', ['week', 'month', 'hour'])
Sections = SectionsClass('week', 'month', 'hour')

# Stacked radial plot, where areas are determined by 'value' label, colored by category,
# and arranged by section (month or day of week)
# https://plotly.com/python/wind-rose-charts/
class RadialPlot(html.Div):
    def __init__(self, name, df, section, value_label='cost'):
        self.html_id = name.lower().replace(" ", "-")
        self.feature_x = 'accident_year'
        self.feature_y = 'cost'
        self.value_label = value_label
        self.section_name = f"section_{section}"
        if section == Sections.week:
            df[self.section_name] = df['datetime'].dt.weekday
        elif section == Sections.month:
            df[self.section_name] = df['datetime'].dt.month
        elif section == Sections.hour:
            df[self.section_name] = df['datetime'].dt.hour
        self.df = df


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
        df = self.df

        # TODO: the python freak in me wants to write as a listcomp
        data = []
        for color in sorted(df[feature].unique()):
            for sec in sorted(df[self.section_name].unique()):
                data.append((color, sec, df[(df[self.section_name] == sec) & (df[feature] == color)][self.feature_y].sum()))
        fig_df = pd.DataFrame(data, columns=[feature, self.section_name, self.feature_y])
        fig_df[self.section_name] = fig_df[self.section_name].astype(str)
        fig_df[feature] = fig_df[feature].astype(str)
        fig = px.bar_polar(fig_df, r=self.feature_y, theta=self.section_name, color=feature)
        print(f"done: updating {self.html_id} plot in {time.time() - start:.2f}s")
        return fig
