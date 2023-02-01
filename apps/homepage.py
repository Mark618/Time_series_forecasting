from app import app

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1("Aim", style={"color": "#004d40"}),
                                html.H5(
                                    [
                                        "To develop a predictive model by using sales data that can predict the sale "
                                        "of the products in the upcoming month or years based on indicator data and "
                                        "show the result. "
                                    ]
                                    , style={"color": "#004d40"})
                            ],
                            className='col l5 s12', style={"padding-right": "15px"}
                        ),
                        html.Div(
                            [
                                html.Img(src=app.get_asset_url('undraw_predictive_analytics_kf9n.svg'),
                                         className="responsive-img")
                            ],
                            className='col l7 s12'
                        )
                    ],
                    className='container'
                )
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(src=app.get_asset_url('undraw_business_decisions_gjwy.svg'),
                                         className="responsive-img")
                            ],
                            className='col l7 s12'
                        ),
                        html.Div(
                            [
                                html.H1("How it helps?", style={"color": "#004d40"}),
                                html.H5(
                                    [
                                        "This sales predictive model provides an alternative solution for business "
                                        "which allows them to forecast their sales performance and visualize the data "
                                        "based on past historical data using FBprophet. "
                                    ]
                                    , style={"color": "#004d40", "text-align": "justify"})
                            ],
                            className='col l5 s12'
                        ),

                    ],
                    className='container'
                )
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [

                        html.Div(
                            [
                                html.H1("Benefits", style={"color": "#004d40"}),
                                html.H5(
                                    [
                                        html.Ul(
                                            [
                                                html.Li("Prevent human error in sales forecast"),
                                                html.Br(),
                                                html.Li("Better visualization of the sales result"),
                                                html.Br(),
                                                html.Li("Helpful in planning future activities"),
                                            ]
                                        )
                                    ]
                                    , style={"color": "#004d40", "text-align": "justify"})
                            ],
                            className='col l5 s12'
                        ),
                        html.Div(
                            [
                                html.Img(src=app.get_asset_url('undraw_Business_analytics_re_tfh3.svg'),
                                         className="responsive-img")
                            ],
                            className='col l7 s12'
                        ),

                    ],
                    className='container'
                )
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(src=app.get_asset_url('undraw_dashboard_nklg.svg'),
                                         className="responsive-img")
                            ],
                            className='col l7 s12'
                        ),
                        html.Div(
                            [
                                html.H1("Sales Dashboard", style={"color": "#004d40"}),
                                html.H5(
                                    [
                                        "Give you an overview of all your shop so you can easily manage every sales, "
                                        "marketing or service interaction. "
                                    ]
                                    , style={"color": "#004d40", "text-align": "justify"})
                            ],
                            className='col l5 s12'
                        ),

                    ],
                    className='container'
                )
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [

                        html.Div(
                            [
                                html.H1("Responsive", style={"color": "#004d40"}),
                                html.H5(
                                    [
                                        "View your result anywhere on any devices!"
                                    ]
                                    , style={"color": "#004d40", "text-align": "justify"})
                            ],
                            className='col l5 s12'
                        ),
                        html.Div(
                            [
                                html.Img(src=app.get_asset_url('undraw_Devices_re_dxae.svg'),
                                         className="responsive-img")
                            ],
                            className='col l7 s12'
                        ),

                    ],
                    className='container'
                )
            ],
            className='row'
        ),
        html.Footer(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H5("Contact", className="white-text"),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    [
                                                        html.Span("mail", className="small material-icons"),
                                                        html.Span("tp044716@mail.apu.edu.my")
                                                    ],
                                                )
                                            ]
                                        )
                                    ],
                                    className="col s12 l6"
                                )
                            ],
                            className="row"
                        )
                    ],
                    className="container"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                "© 2020 | Copyright All rights reserverd | Please use one of the browsers: Google "
                                "Chrome / Mozila / Microsoft IE 9 or higher. "
                            ],
                            className="container"
                        )
                    ],
                    className="footer-copyright"
                )
            ],
            className="page-footer teal darken-2"
        )

    ]
)
