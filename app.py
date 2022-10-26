import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("Car_sales.csv")


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Car Price and Sales Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🏎️", className="header-emoji"),
                html.H1(
                    children="Car Sales Analytics", className="header-title"
                ),
                html.P(
                    children="Based on 2021 data set we can analyze how many models of each model were sold at what price.",
                    className="header-description",
                ),
                html.P(children="This data set is being taken from the Analytixlabs, 2019", className="header-description",)
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Make", className="menu-title"),
                        dcc.Dropdown(
                            id="make-filter",
                            options=[
                                {"label": make, "value": make}
                                for make in np.sort(data.Manufacturer.unique())
                            ],
                            value="Acura",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # html.Div(
                #     children=[
                #         html.Div(children="Model", className="menu-title"),
                #         dcc.Dropdown(
                #             id="model-filter",
                #             options=[
                #                 {"label": model, "value": model}
                #                 for model in data.Model.unique()
                #             ],
                #             value="Integra",
                #             clearable=False,
                #             searchable=False,
                #             className="dropdown",
                #         ),
                #     ],
                # ),
                # html.Div(
                #     children=[
                #         html.Div(
                #             children="Date Range", className="menu-title"
                #         ),
                #         dcc.DatePickerRange(
                #             id="date-range",
                #             min_date_allowed=data.Date.min().date(),
                #             max_date_allowed=data.Date.max().date(),
                #             start_date=data.Date.min().date(),
                #             end_date=data.Date.max().date(),
                #         ),
                #     ]
                # ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)


@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("make-filter", "value"),
        # Input("model-filter", "value"),
        # Input("date-range", "start_date"),
        # Input("date-range", "end_date"),
    ],
)
def update_charts(make):
    print(make)
    mask = (
        (data.Manufacturer == make)
        # & (data.Model == model)
        
    )
    print(mask)
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Model"],
                 "y": filtered_data["Price_in_thousands"],
                 "type": "bar",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price by Model (Thousands)",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": filtered_data["Model"],
                "y": filtered_data["Sales_in_thousands"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {"text": "Sales (Thousands)", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$","fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)
