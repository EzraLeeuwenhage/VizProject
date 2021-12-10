from jbi100_app.data import get_data
from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

from jbi100_app.views.stackedplot import Stackedplot
from jbi100_app.views.twinhistogram import Twinhistogram


if __name__ == '__main__':
    # Create data
    [cdf, vdf] = get_data()

    # Instantiate custom views
    plot1 = Stackedplot("Annual costs over time", 'casualty_type', cdf, 'cost (£)')
    plot2 = Stackedplot("Vehicles over time", 'vehicle_type', vdf, 'total')
    plot3 = Twinhistogram("Casualty comparison histogram", 'casualty_type', cdf, 7, 'cost (£)')
    plot4 = Twinhistogram("Vehicle comparison histogram", 'vehicle_type', vdf, 7, 'total')

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    plot1,
                    plot2,
                    plot3,
                    plot4,
                ],
            ),
        ],
    )

    # Define interactions
    @app.callback(
        Output(plot1.html_id, "figure"), [
        Input("select-category-1", "value"),
    ])
    def update_plot_1(selected_category):
        return plot1.update(selected_category)

    @app.callback(
        Output(plot2.html_id, "figure"), [
        Input("select-category-2", "value"),
    ])
    def update_plot_2(selected_category):
        return plot2.update(selected_category)

    @app.callback(
        Output(plot3.html_id, "figure"), [
        Input("select-value-3", "value"),
        Input("select-category-3", "value"),
        Input("select-year-3", "value"),
    ])
    def update_plot_3(selected_value, selected_category, selected_year):
        return plot3.update(selected_value, selected_category, selected_year)

    @app.callback(
        Output(plot4.html_id, "figure"), [
        Input("select-value-4", "value"),
        Input("select-category-4", "value"),
        Input("select-year-4", "value"),
    ])
    def update_plot_4(selected_value, selected_category, selected_year):
        return plot4.update(selected_value, selected_category, selected_year)


    app.run_server(debug=False, dev_tools_ui=False)