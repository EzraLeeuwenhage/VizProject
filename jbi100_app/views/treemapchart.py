from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

from jbi100_app.views.shared import field_to_title


# Treemap chart of multiple attributes, area determined by cost
# https://plotly.com/python/treemaps/
class TreeMapChart(html.Div):
    def __init__(self, name, value_label='cost'):
        self.html_id = name.lower().replace(" ", "-")
        self.value_label = value_label
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
    def update(self, df, category_features, normalize=False):
        print("start: updating plot")
        start = time.time()
        if normalize:
            # a normalized version that makes the squares proportional to how often they are in df
            # i.e. make uncommon entries bigger, more common smaller
            # thus it is easier to see relative costs, removed from sample size
            # a large size tells you, GIVEN such a category occurred, it is relatively more costly
            df['norm_factor'] = [1] * len(df)
            for cat in category_features:
                freqs = dict(df[cat].value_counts())
                # scale up / down norm_cost depending on the right frequency
                total = sum(freqs.values())
                # expected number per class if they were uniformly distributed
                expectation = 1 / len(freqs)
                for key in freqs:
                    ratio = freqs[key] / total
                    # ratio * correction = expectation
                    correction = expectation / ratio
                    df.loc[df[cat] == key, 'norm_factor'] *= correction
            df['norm_cost'] = df.apply(
                lambda row: row['norm_factor'] * row[self.feature_y], axis=1)
            df.loc[:, 'norm_cost'] /= df['norm_cost'].sum()

            # TODO: fix the colors between the graphs, e.g. by sorting the values
            fig = px.treemap(df,
                            path=[px.Constant("all")] + category_features,
                            values='norm_cost',
                            ) 
            # df.drop("norm_factor")
            # df.drop("norm_cost")
        else:
            fig = px.treemap(df,
                            path=[px.Constant("all")] + category_features,
                            values=self.feature_y,
                            ) 
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

        print(f"done: updating {self.html_id} plot in {time.time() - start:.2f}s")
        return fig
