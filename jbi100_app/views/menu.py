from dash import dcc, html
from ..config import category_list1, category_list2, category_list3, num_plots


def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        children=[
            html.H5("Group 55"),
            html.Div(
                id="intro",
                children="Insurance adjuster analysis dashboard",
            ),
            dcc.Dropdown(
                id="select-plot",
                options=[{"label": i, "value": i} for i in (range(1, num_plots + 1))],
                value=1
            ),
            html.Br(),
        ],
    )


def generate_control_card(plot_num):
    """
    :return: A Div containing controls for graphs.
    """
    if plot_num == 1:
        return html.Div(
            id="control-card",
            children=[
                html.Label("Category plot 1"),
                dcc.Dropdown(
                    id="select-category-1",
                    options=[{"label": i, "value": i} for i in category_list1],
                    value=category_list1[0],
                ),
                html.Br(),
            ], style={"textAlign": "float-left"}
        )

    if plot_num == 2:
        return html.Div(
            id="control-card",
            children=[
                html.Label("Category plot 2"),
                dcc.Dropdown(
                    id="select-category-2",
                    options=[{"label": i, "value": i} for i in category_list2],
                    value=category_list2[0],
                ),
                html.Br(),
            ], style={"textAlign": "float-left"}
        )

    if plot_num == 3:
        return html.Div(
            id="control-card",
            children=[
                html.Label("Value metric of plot 3"),
                dcc.Dropdown(
                    id="select-value-3",
                    options=[{"label": i, "value": i} for i in category_list1],
                    value=category_list1[0],
                ),
                html.Br(),
                html.Label("Categorization for plot 3"),
                dcc.Dropdown(
                    id="select-category-3",
                    options=[{"label": i, "value": i} for i in category_list1],
                    value=category_list1[0],
                ),
                html.Br(),
                html.Label("Year of plot 3"),
                dcc.Dropdown(
                    id="select-year-3",
                    options=[{"label": i, "value": i} for i in range(2010, 2021)],
                    value=2015,
                ),
                html.Br(),
            ], style={"textAlign": "float-left"}
        )

    if plot_num == 4:
        return html.Div(
            id="control-card",
            children=[
                html.Label("Value metric of plot 4"),
                dcc.Dropdown(
                    id="select-value-4",
                    options=[{"label": i, "value": i} for i in category_list2],
                    value=category_list2[0],
                ),
                html.Br(),
                html.Label("Categorization plot 4"),
                dcc.Dropdown(
                    id="select-category-4",
                    options=[{"label": i, "value": i} for i in category_list2],
                    value=category_list2[0],
                ),
                html.Br(),
                html.Label("Year of plot 4"),
                dcc.Dropdown(
                    id="select-year-4",
                    options=[{"label": i, "value": i} for i in range(2010, 2021)],
                    value=2012,
                ),
                html.Br(),
            ], style={"textAlign": "float-left"}
        )

    if plot_num == 5:
        return html.Div(
            id="control-card",
            children=[
                html.Label("Category plot 5"),
                dcc.Dropdown(
                    id="select-category-5",
                    options=[{"label": i, "value": i} for i in category_list3],
                    value=category_list3[0],
                ),
                html.Br(),
            ], style={"textAlign": "float-left"}
        )

    if plot_num == 6:
        return html.Div(
            id="control-card",
            children=[
                html.Label("Value metric of plot 6"),
                dcc.Dropdown(
                    id="select-value-6",
                    options=[{"label": i, "value": i} for i in category_list3],
                    value=category_list3[0],
                ),
                html.Br(),
                html.Label("Categorization plot 6"),
                dcc.Dropdown(
                    id="select-category-6",
                    options=[{"label": i, "value": i} for i in category_list3],
                    value=category_list3[0],
                ),
                html.Br(),
                html.Label("Year of plot 6"),
                dcc.Dropdown(
                    id="select-year-6",
                    options=[{"label": i, "value": i} for i in range(2010, 2021)],
                    value=2012,
                ),
                html.Br(),
            ], style={"textAlign": "float-left"}
        )
