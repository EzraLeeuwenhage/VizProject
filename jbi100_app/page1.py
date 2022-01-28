from jbi100_app.data import get_data
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from jbi100_app.main import app
from dash import dcc, html

from jbi100_app.views.stackedplot import Stackedplot
from jbi100_app.views.treemapchart import TreeMapChart

from jbi100_app.config import category_list4

cdf = get_data()
plot1 = Stackedplot("Annual costs over time", 'casualty_type', cdf, 'cost (£)')
plotx = TreeMapChart("High-level cost breakdown by casualty")
plotx_norm = TreeMapChart("Cost normalized by expected frequency by casualty")

# Define interactions when updating control card values
@app.callback(
    Output(plot1.html_id, "figure"), [
        Input("select-category-1", "value"),
    ])
def update_plot_1(selected_category):
    return plot1.update(selected_category)

@app.callback(
    Output(plotx.html_id, "figure"), [
        Input("plotx-level-1", "value"),
        Input("plotx-level-2", "value"),
        Input("plotx-level-3", "value"),
        Input("plotx-level-4", "value"),
    ])
def update_plot_x(*args):
    tree_levels = [level for level in args if level != NONE]
    return plotx.update(cdf, tree_levels)

@app.callback(
    Output(plotx_norm.html_id, "figure"), [
        Input("plotx-level-1", "value"),
        Input("plotx-level-2", "value"),
        Input("plotx-level-3", "value"),
        Input("plotx-level-4", "value"),
    ])
def update_plot_x_norm(*args):
    tree_levels = [level for level in args if level != NONE]
    return plotx_norm.update(cdf, tree_levels, True)

NONE = "None"

def layout():
    categories = [NONE] + category_list4
    def tree_level(id):
        return html.Div(children=[
            html.Label("Level " + str(id)),
            dcc.Dropdown(
                id="plotx-level-" + str(id),
                options=[{"label": i, "value": i} for i in categories],
                # first level is "severity"
                value=categories[6] if id == 1 else categories[0],
            ),
        ])

    plotx_menu = html.Div(
        className="inline-control-card",
        children=[
            tree_level(1),
            tree_level(2),
            tree_level(3),
            tree_level(4),
        ], style={"textAlign": "float-left"}
    )

    return html.Div(
        className="center-plots",
        children=[
            html.Div(children=["Home page plots :)"]),
            plotx_menu,
            plotx,
            plotx_norm,
            plot1,
        ],
    )
