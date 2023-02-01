from app import app

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    [
        html.Br(),
        html.Img(src=app.get_asset_url('undraw_page_not_found_su7k.svg'),
                 className="responsive-img")
    ]
    , className="center"
)
