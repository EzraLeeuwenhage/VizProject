from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

from jbi100_app.views.shared import field_to_title


# Back-to-back histogram, also called a pyramid chart
# https://stackoverflow.com/questions/67719166/how-to-plot-pyramid-population-chart-with-plotly
class Twinhistogram(html.Div):
    def __init__(self, name, df, n_buckets, value_label='cost'):
        self.html_id = name.lower().replace(" ", "-")
        self.n_buckets = n_buckets
        self.value_label = value_label
        self.df = df
        self.feature_y = 'cost'

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, value_feature, category_feature, category_value):
        print("start: updating plot")
        start = time.time()
        df = self.df
        # then split by binary filter (most frequent of feature vs. the rest)
        mode = category_value
        df_a = df[df[category_feature] == mode]
        df_b = df[df[category_feature] != mode]
        # filter out all values of negative 1
        df_a = df_a[df_a[value_feature] >= 0]
        df_b = df_b[df_b[value_feature] >= 0]
        # remove outliers?: top 0.01% of the data
        df_a = df_a[df_a[value_feature] < df_a[value_feature].quantile(.999)]
        df_b = df_b[df_b[value_feature] < df_b[value_feature].quantile(.999)]

        # then based on the category's cost values make histogram
        # determine histogram buckets
        min_value = min(df_a[value_feature].min(), df_b[value_feature].min())
        max_value = max(df_a[value_feature].max(), df_b[value_feature].max())
        value_range = max_value - min_value
        bucket_size = value_range / self.n_buckets
        buckets1 = [0] * self.n_buckets
        buckets2 = [0] * self.n_buckets
        for b in range(self.n_buckets):
            begin = b * bucket_size + min_value
            end = (b + 1) * bucket_size + min_value
            buckets1[b] = df_a[
                (df_a[value_feature] >= begin) &
                (df_a[value_feature] < end)
            ][self.feature_y].sum()
            buckets2[b] = df_b[
                (df_b[value_feature] >= begin) &
                (df_b[value_feature] < end)
            ][self.feature_y].sum()
        
        # normalize everything to a fraction of the total
        total = sum(buckets1) + sum(buckets2)
        buckets1 = [b / total for b in buckets1]
        buckets2 = [b / total for b in buckets2]
        max_fraction = max(buckets1 + buckets2)
        n_ticks = 9

        xticks = [i * (2 * max_fraction) / (n_ticks + 1) - max_fraction for i in range(n_ticks)]
        ylabels = [f'{i * bucket_size + min_value:.0f} - {(i + 1) * bucket_size + min_value - 1:.0f}' for i in range(self.n_buckets)]
        layout = go.Layout(
            yaxis=go.layout.YAxis(
                title=field_to_title(value_feature),
                ticktext=ylabels, tickvals=list(range(self.n_buckets))),
            xaxis=go.layout.XAxis(
                range=[-max_fraction, max_fraction],
                tickvals=xticks,
                ticktext=[f'{abs(t):.2f}' for t in xticks],
                title=f'Fraction of {self.value_label}'),
            legend_title_text=f'{field_to_title(category_feature)}',
            barmode='overlay',
            bargap=0.1)

        data = [go.Bar(y=list(range(self.n_buckets)),
                       x=buckets1,
                       orientation='h',
                       name=f'{mode}',
                       hoverinfo='x',
                       marker=dict(color='powderblue')
                       ),
                go.Bar(y=list(range(self.n_buckets)),
                # negate values to draw them to the left
                       x=[-b for b in buckets2],
                       orientation='h',
                       name=f'not {mode}',
                       hoverinfo='x',
                       marker=dict(color='seagreen')
                       )]
        print(f"done: updating {self.html_id} plot in {time.time() - start:.2f}s")
        return go.Figure(layout=layout, data=data)
