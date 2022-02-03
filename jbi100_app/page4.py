from jbi100_app.data import get_data
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from jbi100_app.main import app
from dash import dcc, html
from jbi100_app.views.radialplot import RadialPlot, Sections

from jbi100_app.views.stackedplot import Stackedplot
from jbi100_app.views.treemapchart import TreeMapChart

from jbi100_app.config import category_list4

cdf = get_data()
plot1 = Stackedplot("Annual cost over time", 'casualty_type', cdf, 'cost (£)')
plot2 = RadialPlot("Cost by month", cdf, Sections.month)
plot3 = RadialPlot("Cost by day of week", cdf, Sections.week)
plot4 = RadialPlot("Cost by hour of day", cdf, Sections.hour)

@app.callback(
    Output(plot1.html_id, "figure"), [
        Input("page4-plot1-category", "value"),
    ])
def update_plot_1(selected_category):
    return plot1.update(selected_category)

@app.callback(
    Output(plot2.html_id, "figure"), [
        Input("page4-plot1-category", "value"),
    ])
def update_plot_2(selected_category):
    return plot2.update(selected_category)

@app.callback(
    Output(plot3.html_id, "figure"), [
        Input("page4-plot1-category", "value"),
    ])
def update_plot_3(selected_category):
    return plot3.update(selected_category)

@app.callback(
    Output(plot4.html_id, "figure"), [
        Input("page4-plot1-category", "value"),
    ])
def update_plot_4(selected_category):
    return plot4.update(selected_category)

def layout():
    categories = category_list4
    plot1_menu = html.Div(
        className="inline-control-card",
        children=[
            dcc.Dropdown(
                id="page4-plot1-category",
                options=[{"label": i, "value": i} for i in categories],
                value=categories[0],
            ),
        ], style={"textAlign": "float-left"}
    )

    return html.Div(
        className="center-plots",
        children=[
            html.Div(children=["Time-focused views"]),
            plot1_menu,
            plot1,
            plot2,
            plot3,
            plot4,
        ],
    )
