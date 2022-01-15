from jbi100_app.data import get_data, test_data
from jbi100_app.main import app
import jbi100_app.views.menu as menu
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

from jbi100_app.views.stackedplot import Stackedplot
from jbi100_app.views.twinhistogram import Twinhistogram

use_all_data = True

if __name__ == '__main__':
    # Create data
    if use_all_data:
        [cdf, vdf, adf] = get_data()
    else:
        cdf = test_data()

    # Instantiate custom views
    plot1 = Stackedplot("Annual costs over time", 'casualty_type', cdf, 'cost (£)')
    plot2 = Stackedplot("Vehicles over time", 'vehicle_type', vdf, 'total')
    plot3 = Twinhistogram("Casualty comparison histogram", 'casualty_type', cdf, 7, 'cost (£)')
    plot4 = Twinhistogram("Vehicle comparison histogram", 'vehicle_type', vdf, 10, 'total')
    plot5 = Stackedplot("Accidents over time", 'number_of_vehicles', adf, 'total')
    plot6 = Twinhistogram("Accident comparison histogram", 'did_police_officer_attend_scene_of_accident', adf, 8,
                          'total')

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=[
                    menu.generate_description_card(),
                    html.Br(),
                    html.Div(id="control_card")
                ],
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[],
            ),
        ],
    )

    # Define menu creation with callback
    @app.callback(
        Output(component_id="control_card", component_property="children"), [
            Input(component_id="select-plot", component_property="value"),
        ])
    def make_control_layout(plot_num):
        return menu.generate_control_card(plot_num)

    # Define behaviour when selecting new plot number
    @app.callback(
        Output(component_id="right-column", component_property="children"), [
            Input(component_id="select-plot", component_property="value"),
        ])
    def init_plot(plot_num):
        if plot_num == 1:
            return plot1
        elif plot_num == 2:
            return plot2
        elif plot_num == 3:
            return plot3
        elif plot_num == 4:
            return plot4
        elif plot_num == 5:
            return plot5
        elif plot_num == 6:
            return plot6

    # Define interactions when updating control card values
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

    @app.callback(
        Output(plot5.html_id, "figure"), [
            Input("select-category-5", "value"),
        ])
    def update_plot_5(selected_category):
        return plot5.update(selected_category)

    @app.callback(
        Output(plot6.html_id, "figure"), [
            Input("select-value-6", "value"),
            Input("select-category-6", "value"),
            Input("select-year-6", "value"),
        ])
    def update_plot_6(selected_value, selected_category, selected_year):
        return plot6.update(selected_value, selected_category, selected_year)

    app.run_server(debug=False, dev_tools_ui=False)
