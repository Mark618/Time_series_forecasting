from app import app
from apps import forecast, performance_dash, shop_dash, homepage, error

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

server = app.server

app.layout = html.Div(
    [
        html.Nav(
            html.Div(
                className="nav-wrapper",
                children=[
                    html.A("Sales Forecast system", className="brand-logo", style={"padding-left": "15px"},
                           href="/apps/home"),
                    html.Ul(
                        className="right hide-on-med-and-down",
                        children=[
                            html.Li(html.A("Sales Performance", href="/apps/performance_dash")),
                            html.Li(html.A("Sales Forecast", href="/apps/forecast")),
                            html.Li(html.A("Shop Performance", href="/apps/shop_dash")),
                        ]
                    )
                ],
                style={"backgroundColor": "Teal"}

            ),
        ),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=[]),

    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/performance_dash':
        return performance_dash.layout
    elif pathname == '/apps/forecast':
        return forecast.layout
    elif pathname == '/apps/shop_dash':
        return shop_dash.layout
    elif pathname == '/apps/home':
        return homepage.layout
    elif pathname == '/apps/':
        return homepage.layout
    else:
        return error.layout


if __name__ == '__main__':
    app.run_server(debug=True)
