from dash import dcc, html
import plotly.express as px
import pandas as pd
import time
import numpy as np


class TenaryScatter(html.Div):
    def __init__(self, name, cdf):
        self.html_id = name.lower().replace(" ", "-")
        self.cdf = cdf

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, categories, values, month_or_year='month'):
        start = time.time()
        print("start: updating plot")
        start = time.time()
        df = self.cdf

        # calculate the frequencies of values for categories compared to total
        by_time = []
        # TODO: also group by severity
        if month_or_year == 'month':
            for month in range(1, 13):
                # take the proportion equal to given value in this year
                month_df = df[df['datetime'].dt.month == month]
                total_rows = len(month_df)
                mapping = {
                    key: len(month_df[month_df[key] == value]) / total_rows
                    for (key, value) in zip(categories, values)
                }
                mapping['label'] = str(month)
                by_time.append(mapping)
        else:
            for yr in sorted(df['accident_year'].unique()):
                # take the proportion equal to given value in this year
                month_df = df[df['datetime'].dt.year == yr]
                total_rows = len(month_df)
                mapping = {
                    key: len(month_df[month_df[key] == value]) / total_rows
                    for (key, value) in zip(categories, values)
                }
                mapping['label'] = str(yr)
                by_time.append(mapping)

        # start updating plot based on new data
        # https://plotly.com/python/ternary-plots/
        fig = px.scatter_ternary(by_time, a=categories[0], b=categories[1], c=categories[2],
        hover_name='label'
                                 )
        print(f"done: joining dfs {self.html_id} plot in {time.time() - start:.2f}s")

        return fig
