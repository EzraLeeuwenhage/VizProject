from jbi100_app.data import get_data
from jbi100_app.main import app
import jbi100_app.views.menu as menu
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

from jbi100_app.views.stackedplot import Stackedplot
from jbi100_app.views.twinhistogram import Twinhistogram

import jbi100_app.page1 as page1
import jbi100_app.page2 as page2
import jbi100_app.page4 as page4

if __name__ == '__main__':
    # Create data
    cdf = get_data()

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
            return page1.layout()
        elif plot_num == 2:
            return page2.layout()
        elif plot_num == 3:
            return plot3
        elif plot_num == 4:
            return page4.layout()

    app.run_server(debug=False, dev_tools_ui=False)
