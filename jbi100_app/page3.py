from unicodedata import category
from jbi100_app.views.tenary_scatter import TenaryScatter
from dash.dependencies import Input, Output
from jbi100_app.main import app
from dash import dcc, html
from jbi100_app.page1 import cdf
from jbi100_app.config import category_list4

plot_month = TenaryScatter("Tenary plot per month per severity", cdf)
plot_year = TenaryScatter("Tenary plot per year per severity", cdf)

categories = category_list4

# Define interactions when updating control card values
@app.callback(
    Output(plot_month.html_id, "figure"), [
        Input("select-cat1-type", "value"),
        Input("select-cat1-value", "value"),
        Input("select-cat2-type", "value"),
        Input("select-cat2-value", "value"),
        Input("select-cat3-type", "value"),
        Input("select-cat3-value", "value"),
    ])
def update_plot(type1, value1, type2, value2, type3, value3):
    return plot_month.update([type1, type2, type3], [value1, value2, value3])


@app.callback(
    Output(plot_year.html_id, "figure"), [
        Input("select-cat1-type", "value"),
        Input("select-cat1-value", "value"),
        Input("select-cat2-type", "value"),
        Input("select-cat2-value", "value"),
        Input("select-cat3-type", "value"),
        Input("select-cat3-value", "value"),
    ])
def update_plot2(type1, value1, type2, value2, type3, value3):
    return plot_year.update([type1, type2, type3], [value1, value2, value3], 'year')


@app.callback(
    Output("select-cat1-value-div", "children"), [
        Input("select-cat1-type", "value"),
    ])
def update_value_select1(category_feature):
    counts = dict(cdf[category_feature].value_counts())
    # Get a list of values sorted from most common to least common
    values = sorted(counts, key=lambda x: -counts[x])
    return [
        dcc.Dropdown(
            id="select-cat1-value",
            options=[{"label": i, "value": i} for i in values],
            value=values[0])
    ]


@app.callback(
    Output("select-cat2-value-div", "children"), [
        Input("select-cat2-type", "value"),
    ])
def update_value_select2(category_feature):
    counts = dict(cdf[category_feature].value_counts())
    # Get a list of values sorted from most common to least common
    values = sorted(counts, key=lambda x: -counts[x])
    return [
        dcc.Dropdown(
            id="select-cat2-value",
            options=[{"label": i, "value": i} for i in values],
            value=values[0])
    ]


@app.callback(
    Output("select-cat3-value-div", "children"), [
        Input("select-cat3-type", "value"),
    ])
def update_value_select3(category_feature):
    counts = dict(cdf[category_feature].value_counts())
    # Get a list of values sorted from most common to least common
    values = sorted(counts, key=lambda x: -counts[x])
    return [
        dcc.Dropdown(
            id="select-cat3-value",
            options=[{"label": i, "value": i} for i in values],
            value=values[0])
    ]


def layout():
    def make_cat_menu(number):
        return html.Div(
            children=[
                html.Label("Select category " + str(number)),
                dcc.Dropdown(
                    id="select-cat" + str(number) + "-type",
                    options=[{"label": i, "value": i} for i in categories],
                    value=categories[number + 20],
                ),
                html.Div(children=[], id="select-cat" + str(number) + "-value-div")
            ]
        )

    control_div = html.Div(
        className="control-card",
        children=[
            make_cat_menu(1),
            make_cat_menu(2),
            make_cat_menu(3),
        ], style={"textAlign": "float-left"}
    )

    return html.Div(
        className="center-plots",
        children=[
            html.Div(children=["Attribute Correlation to Severity Grouped By Year"]),
            plot_month,
            plot_year,
            control_div,
        ],
    )
