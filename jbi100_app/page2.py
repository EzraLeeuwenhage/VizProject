from unicodedata import category
from jbi100_app.data import get_data
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from jbi100_app.main import app
from dash import dcc, html
from jbi100_app.views.horizontalbar import HorizontalBar
from jbi100_app.views.twinhistogram import Twinhistogram

from jbi100_app.views.stackedplot import Stackedplot
from jbi100_app.views.treemapchart import TreeMapChart

from jbi100_app.config import category_list4

cdf = get_data()

# On page 2, you can select a category and look at a bar chart of each of its values
plot1 = HorizontalBar("Cost by value", cdf)
# Or compare a particular value by numerical category
plot2 = Twinhistogram("Comparison Value", cdf, 7)

# Define interactions when updating control card values
@app.callback(
    Output(plot1.html_id, "figure"), [
        Input("plot-level-1", "value"),
    ])
def update_plot_1(selected_category):
    return plot1.update(selected_category)

@app.callback(
    Output("plot2-value-select", "children"), [
        Input("plot-level-1", "value"),
    ])
def update_value_select(category_feature):
    counts = dict(cdf[category_feature].value_counts())
    # Get a list of values sorted from most common to least common
    values = sorted(counts, key=lambda x: -counts[x])
    return [
        html.Label("Value selection"),
        dcc.Dropdown(
            id="plot2-value-select-dcc",
            options=[{"label": i, "value": i} for i in values],
            value=values[0])
    ]

@app.callback(
    Output(plot2.html_id, "figure"), [
        Input("plot-level-1", "value"),
        Input("plot-level-2", "value"),
        Input("plot2-value-select-dcc", "value"),
    ])
def update_plot_2(category_feature, value_feature, category_value):
    return plot2.update(value_feature, category_feature, category_value)

def layout():
    categories = category_list4
    # default is "severity"
    def category_menu(id, default=0):
        return html.Div(children=[
            html.Label("Attribute selection " + str(id)),
            dcc.Dropdown(
                id="plot-level-" + str(id),
                options=[{"label": i, "value": i} for i in categories],
                value=categories[default]
            ),
        ])

    plot1_menu = html.Div(
        className="inline-control-card",
        children=[
            category_menu(1),
        ], style={"textAlign": "float-left"}
    )

    plot2_menu = html.Div(
        className="inline-control-card",
        children=[
            # Default is 'age'
            category_menu(2, 3),
            html.Div(children=[], id="plot2-value-select")
        ], style={"textAlign": "float-left"}
    )

    return html.Div(
        className="center-plots",
        children=[
            html.Div(children=["Distribution of Cost on Attributes"]),
            plot1_menu,
            plot1,
            plot2_menu,
            plot2,
        ],
    )
