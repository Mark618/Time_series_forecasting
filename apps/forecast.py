import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly, plot_yearly
import joblib
from app import app


# external_stylesheets = ['assets/materialize.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Sales Forecasting', meta_tags=[{
#     'name': 'viewport',
#     'content': 'width=device-width, initial-scale=1.0'
# }], external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"])

path = 'data/'
m_path = 'model/'
sales = pd.read_csv(path + 'sales_train.csv')
item_cat = pd.read_csv(path + 'item_categories.csv')
item = pd.read_csv(path + 'items.csv')
shop = pd.read_csv(path + 'shops.csv')
grouped = pd.read_csv(path + 'grouped_item.csv')
p_model = joblib.load(m_path+'prophet2_model')
p_model_h = joblib.load(m_path+'prophet_model')


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


# fig = sn.pointplot(x='month', y='item_cnt_day', hue='year', data=grouped)
def generate_table(dataframe, max_rows=10):
    return html.Div(className='row', children=html.Div(className='responsive-table', children=(html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ]))))


def prohetdata():
    ts = sales.groupby(["date_block_num"])["item_cnt_day"].sum()
    ts.index = pd.date_range(start='2013-01-01', end='2015-10-01', freq='MS')
    ts = ts.reset_index()
    ts.columns = ['ds', 'y']
    return ts


def model_param(yearly_seasonality, data):
    if yearly_seasonality == 'True':
        model = p_model
    else:
        model = p_model_h
    return model


fig = px.line(grouped, x="month", y="item_cnt_day", color="year",
              title="Item sales",
              labels={"salary": "Annual Salary (in thousands)"}  # customize axis label
              )

p_data = prohetdata()
# model1 = model_param(True, p_data)
# future = model1.make_future_dataframe(periods=12, freq='MS')
# # now lets make the forecasts
# forecast = model1.predict(future)
# print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12))


layout = html.Div(
    [
        html.Div(
            className='row',
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5(
                                    "Number of days Forecasted",
                                    className="",
                                    style={'text-align': 'center', "font-family": 'Open Sans'}
                                ),
                                html.Br(),
                                dcc.Slider(
                                    id='num_month_forecast',
                                    min=1,
                                    max=12,
                                    step=None,
                                    marks={
                                        1: '30',
                                        3: '90',
                                        6: '180',
                                        12: '365'
                                    },
                                    value=3,
                                    className=''
                                ),
                                html.H5("Year Seasonality",
                                        style={'text-align': 'center', "font-family": 'Open Sans'}),
                                dcc.Dropdown(
                                    id='radio_state',
                                    options=[
                                        {'label': 'Enable', 'value': 'True'},
                                        {'label': 'Disable', 'value': 'False'}
                                    ],
                                    value='True',
                                    # labelStyle={"display": "inline-block"},
                                    className="input-field",
                                ),
                            ],
                            className='card',
                            # style={'height': '20vh'}
                        ),
                        html.Div(
                            [
                                html.H5("Seasonal Component",
                                        style={"text-align": "center", "padding": '5px', "font-family": 'Open Sans'}),
                                html.Br(),
                                html.Div(
                                    [
                                        dcc.Graph(id='seasonal_com', animate=False, responsive=True)
                                    ],
                                    # style={'height': '90vh'}
                                )
                            ],
                            className='card',
                            style={'height': '65vh'}
                        )
                    ],
                    className='col l4 s12 m6',
                    # style={'backgroundColor': 'blue'}
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Sales Forecast with Prophet",
                                        style={"text-align": "center", "padding": '5px', "font-family": 'Open Sans'}),
                                html.Br(),
                                html.Div(
                                    [
                                        dcc.Graph(id='sales_year', animate=True, responsive=True)
                                    ],
                                    style={'height': '80vh'}
                                ),

                            ],
                            # style={'height': '95vh'},
                            className='card'
                        )
                    ],
                    className='col l8 s12 m6',
                    # style={'backgroundColor': 'cyan', 'height': '90vh'}
                ),
                # html.Div(
                #     [
                #
                #     ],
                #     className='col l4',
                #     # style={'backgroundColor': 'cyan', 'height': '100%'}
                # )
            ], ),
    ]
)


# @app.callback(
#     dash.dependencies.Output('radio-output-container', 'children'),
#     [dash.dependencies.Input('radio_state', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)


@app.callback(
    [dash.dependencies.Output('sales_year', 'figure'),
     dash.dependencies.Output('seasonal_com', 'figure')],
    [dash.dependencies.Input('num_month_forecast', 'value'),
     dash.dependencies.Input('radio_state', 'value')])
def update_my_graph(value, radio_state):
    model1 = model_param(radio_state, p_data)
    future = model1.make_future_dataframe(periods=value, freq='MS')
    forecast = model1.predict(future)
    p_fig = plot_plotly(model1, forecast, xlabel='Year_Month', ylabel='Total Sales')
    p_com_fig = plot_components_plotly(model1, forecast)
    # p_com_fig.update_layout(autosize=True)
    p_fig.update_layout(plot_bgcolor="#FFFFFF")
    p_fig.update_xaxes(showline=True, linecolor='teal')
    p_fig.update_yaxes(showline=True, linecolor='teal')
    p_com_fig.update_layout(plot_bgcolor="#FFFFFF")
    p_com_fig.update_xaxes(showline=True, linecolor='teal')
    p_com_fig.update_yaxes(showline=True, linecolor='teal')
    return p_fig, p_com_fig


# @app.callback(
#     dash.dependencies.Output('slider-output-container', 'children'),
#     [dash.dependencies.Input('num_day_forecast', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)


# if __name__ == "__main__":
#     app.run_server(debug=True)
