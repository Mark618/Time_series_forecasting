import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
import joblib
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly, plot_yearly

from app import app

path = 'data/'
sales = pd.read_csv(path + 'sales_train.csv', parse_dates=["date"])
item_cat = pd.read_csv(path + 'item_categories.csv')
item = pd.read_csv(path + 'items.csv')
shop = pd.read_csv(path + 'shops.csv')


def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})
    return dict_list


def get_predict_data(shopid):
    ts = sales.loc[(sales['shop_id'] == shopid)].groupby(["date"])["total_sales"].sum()
    ts = ts.reset_index()
    trythis1 = ts.copy()
    trythis1.columns = ['ds', 'y']
    return trythis1


def get_model_input(state, holiday, dataset):
    if state == 'True':
        model11 = Prophet(yearly_seasonality=True)
    else:
        model11 = Prophet(yearly_seasonality=False)
    if holiday == 'True':
        model11.add_country_holidays(country_name='RU')
        model11.fit(dataset)
    else:
        model11.fit(dataset)
    return model11


def item_sold_graph(shopid):
    shop_item_grp = pd.DataFrame(
        sales.loc[(sales['shop_id'] == shopid)].groupby(['date_block_num', 'item_id'])[
            'item_cnt_day'].sum().reset_index())
    shop_item_test = pd.DataFrame(shop_item_grp.groupby(['item_id'])['item_cnt_day'].sum().reset_index())
    shop_item_test = shop_item_test.merge(item, how='left', on='item_id')
    shop_item_test = shop_item_test.merge(item_cat, how='left', on='item_category_id')
    shop_item_test.drop(['item_category_id'], axis=1, inplace=True)
    fig1 = px.bar(shop_item_test.sort_values('item_cnt_day', ascending=False).head(), x="item_cnt_day", y="item_name",
                  orientation='h',
                  color_discrete_sequence=['rgb(99, 166, 160)'],
                  title='Top 5 Item Sold(unit)')
    fig1.update_layout(plot_bgcolor="#FFFFFF",
                       xaxis=dict(title="Total Sales"),
                       yaxis=dict(title="")
                       )
    return fig1


def item_cat_sold_graph(shopid):
    shop_item_cat_grp = pd.DataFrame(
        sales.loc[(sales['shop_id'] == shopid)].groupby(['date_block_num', 'item_id'])[
            'item_cnt_day'].sum().reset_index())
    shop_item_cat_grp = shop_item_cat_grp.merge(item, how='left', on='item_id')
    shop_item_cat_grp = shop_item_cat_grp.merge(item_cat, how='left', on='item_category_id')
    shop_item_cat_test = pd.DataFrame(shop_item_cat_grp.groupby(['item_group'])['item_cnt_day'].sum().reset_index())
    fig1 = px.bar(shop_item_cat_test.sort_values('item_cnt_day', ascending=False).head(), x="item_cnt_day",
                  y="item_group", orientation='h',
                  color_discrete_sequence=['rgb(99, 166, 160)'],
                  title='Top 5 Item Category Sold(unit)')
    fig1.update_layout(plot_bgcolor="#FFFFFF",
                       xaxis=dict(title="Total Sales"),
                       yaxis=dict(title="Item Catgory Group")
                       )
    return fig1


def sales_per_graph(shopid):
    sales_comp = pd.DataFrame(
        sales.loc[(sales['shop_id'] == shopid)].groupby(['year', 'month'])['total_sales'].sum().reset_index())
    fig2 = px.line(sales_comp, x="month", y="total_sales", color='year',
                   color_discrete_sequence=px.colors.sequential.Mint_r, title='Sales Revenue')
    fig2.update_layout(plot_bgcolor="#FFFFFF",
                       xaxis=dict(title="Month"),
                       yaxis=dict(title="")
                       )
    return fig2


def weekly_graph(shopid):
    week_pre = pd.DataFrame(
        sales.loc[(sales['shop_id'] == shopid)].groupby(['date'])["total_sales"].sum().reset_index())
    week_pre['date'] = pd.to_datetime(week_pre['date'])
    week_pre = week_pre.set_index('date')
    ts_avg_sales = week_pre.resample('W').mean()
    ts_avg_sales.reset_index(inplace=True)
    fig3 = px.bar(ts_avg_sales, y='total_sales', x='date', text='total_sales',
                  color_discrete_sequence=px.colors.sequential.Mint_r, title='Average Weekly Sales Revenue')
    fig3.update_traces(textposition='outside')
    fig3.update_layout(plot_bgcolor="#FFFFFF",
                       xaxis=dict(title=""),
                       yaxis=dict(title=""),
                       bargap=0.15
                       )
    return fig3


def weekly_value(shopid):
    week_pre = pd.DataFrame(
        sales.loc[(sales['shop_id'] == shopid)].groupby(['date'])["total_sales"].sum().reset_index())
    week_pre['date'] = pd.to_datetime(week_pre['date'])
    week_pre = week_pre.set_index('date')
    ts_avg_sales = week_pre.resample('W').mean()
    ts_avg_sales.reset_index(inplace=True)
    avg_value = ts_avg_sales.total_sales.mean()
    return avg_value


def sales_value(shopid):
    ts = pd.DataFrame(sales.loc[(sales['shop_id'] == shopid)].groupby(["date"])["total_sales"].sum())
    ts = ts.reset_index()
    ts['date'] = pd.to_datetime(ts['date'])
    ts['cumulative'] = ts.total_sales.cumsum()
    s_value = ts.total_sales.sum().round(2)
    return s_value


# print(get_predict_data(12))
# model = get_model_input(True, True, get_predict_data(12))
# future = model.make_future_dataframe(periods=1, freq='M')
# forecast = model.predict(future)
# p_fig = plot_plotly(model, forecast, xlabel='Year_Month', ylabel='Total Sales')
# p_com_fig = plot_components_plotly(model, forecast)
# p_fig.show()

# external_stylesheets = ['../assets/materialize.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Sales Forecasting', meta_tags=[{
#     'name': 'viewport',
#     'content': 'width=device-width, initial-scale=1.0'
# }], external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"])

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.A("Model Controls", className="card-title", style={"color": "#004d40"}),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.A("Shop ID", className="card-title",
                                                               style={"color": "#004d40", 'text-align': 'center'}),
                                                        dcc.Dropdown(id='shop_select',
                                                                     options=get_options(shop['shop_id'].unique()),
                                                                     value=0,
                                                                     # style={'backgroundColor': 'white'},
                                                                     className='input-field'
                                                                     ),
                                                    ],
                                                    className='card-content'
                                                )
                                            ],
                                            className=""
                                        ),
                                    ],
                                    className='col l2 s12'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.A("Yearly seasonality", className="card-title",
                                                               style={"color": "#004d40", 'text-align': 'center'}),
                                                        dcc.Dropdown(
                                                            id='year_state',
                                                            options=[
                                                                {'label': 'Enable', 'value': 'True'},
                                                                {'label': 'Disable', 'value': 'False'}
                                                            ],
                                                            value='True',
                                                            # labelStyle={"display": "inline-block"},
                                                            className="input-field",
                                                        ),
                                                    ],
                                                    className='card-content'
                                                )
                                            ],
                                            className=""
                                        ),
                                    ],
                                    className='col l4 s12'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.A("Holiday", className="card-title",
                                                               style={"color": "#004d40", 'text-align': 'center'}),
                                                        dcc.Dropdown(
                                                            id='holiday_state',
                                                            options=[
                                                                {'label': 'Enable', 'value': 'True'},
                                                                {'label': 'Disable', 'value': 'False'}
                                                            ],
                                                            value='True',
                                                            className="input-field",
                                                        ),
                                                    ],
                                                    className='card-content'
                                                )
                                            ],
                                            className=""
                                        ),
                                    ],
                                    className='col l4 s12'
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            html.A("Shop Name", className="card-title",
                                                                   style={"color": "#004d40"}),
                                                            className="card-title",
                                                            style={'text-align': 'center'}
                                                        ),
                                                        html.Div(
                                                            id="shop_name",
                                                            className='container',
                                                            style={'text-align': 'center', "color": "#004d40"})
                                                    ],
                                                    className='card-content'
                                                )
                                            ],
                                            className=""
                                        ),
                                    ],
                                    className='col l2 s12'
                                ),
                            ],
                            className='card-content', style={"align": "center"}
                        )
                    ],
                    className='card col l12 s12'
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
                                dcc.Graph(id='shop_seasonal_com', animate=False, responsive=True)
                            ]
                        )
                    ],
                    className="card col l4 s12 "
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='sales_month', animate=False, responsive=True)
                            ],
                            # style={'height': '80vh'}
                        ),
                    ],
                    className='card col l8 s12'
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
                                html.Div(
                                    [
                                        html.Div(
                                            html.A("Latest Sales Data", className="card-title",
                                                   style={"color": "#004d40"}),
                                            className="card-title",
                                            style={'text-align': 'center'}
                                        ),
                                        html.Div(
                                            id="shop_latest_data",
                                            className='container',
                                            style={'text-align': 'center',"font-size": "32px",'width': '140px'})

                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col s12 l3'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.A("Sales Revenue", className="card-title",
                                                   style={"color": "#004d40"}),
                                            className="card-title",
                                            style={'text-align': 'center'}
                                        ),
                                        html.Div(
                                            id="shop_sales_data",
                                            className='container',
                                            style={'text-align': 'center', "color": "#004d40", "font-size": "24px"})

                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col s12 l3'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.A("Average Weekly Sales", className="card-title",
                                                   style={"color": "#004d40"}),
                                            className="card-title",
                                            style={'text-align': 'center'}
                                        ),
                                        html.Div(
                                            id="shop_weekly_avg_data",
                                            className='container',
                                            style={'text-align': 'center', "color": "#004d40", "font-size": "24px"})

                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col s12 l3'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.A("Forecast Sales(Next Month)", className="card-title",
                                                   style={"color": "#004d40"}),
                                            className="card-title",
                                            style={'text-align': 'center'}
                                        ),
                                        html.Div(
                                            id="forecast_value",
                                            className='container',
                                            style={'text-align': 'center', "color": "#004d40", "font-size": "24px"})

                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col s12 l3'
                ),

            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='top_5_item', animate=False)
                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col l5 s12 '
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='weekly_avg', animate=False)
                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col l7 s12 '
                ),
            ],
            className='row'
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='top_5_cat_item', animate=False)
                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col l5 s12'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='sales_graph', animate=False)
                                    ],
                                    className='card-content'
                                )
                            ],
                            className='card'
                        )
                    ],
                    className='col l7 s12'
                ),
            ],
            className='row'
        )

    ],

)


@app.callback(
    [dash.dependencies.Output('sales_month', 'figure'),
     dash.dependencies.Output('shop_seasonal_com', 'figure'),
     dash.dependencies.Output('shop_name', 'children'),
     dash.dependencies.Output('shop_latest_data', 'children'),
     dash.dependencies.Output('shop_sales_data', 'children'),
     dash.dependencies.Output('shop_weekly_avg_data', 'children'),
     dash.dependencies.Output('forecast_value', 'children'),
     dash.dependencies.Output('top_5_item', 'figure'),
     dash.dependencies.Output('weekly_avg', 'figure'),
     dash.dependencies.Output('top_5_cat_item', 'figure'),
     dash.dependencies.Output('sales_graph', 'figure')
     ],
    [dash.dependencies.Input('shop_select', 'value'),
     dash.dependencies.Input('year_state', 'value'),
     dash.dependencies.Input('holiday_state', 'value')])
def update_shop_graph(shopid, yearstate, holidaystate):
    model = get_model_input(yearstate, holidaystate, get_predict_data(shopid))
    future = model.make_future_dataframe(periods=1, freq='M')
    forecast = model.predict(future)
    p_fig = plot_plotly(model, forecast, xlabel='Year_Month', ylabel='Total Sales')
    p_com_fig = plot_components_plotly(model, forecast)
    p_com_fig.update_layout(autosize=True)
    p_fig.update_layout(plot_bgcolor="#FFFFFF")
    p_fig.update_xaxes(showline=True, linecolor='teal')
    p_fig.update_yaxes(showline=True, linecolor='teal')
    p_com_fig.update_layout(plot_bgcolor="#FFFFFF")
    p_com_fig.update_xaxes(showline=True, linecolor='teal')
    p_com_fig.update_yaxes(showline=True, linecolor='teal')
    shop_name = shop['shop_name'].loc[(shop['shop_id'] == shopid)]
    ts = pd.DataFrame(sales.loc[(sales['shop_id'] == shopid)].groupby(["date"])["total_sales"].sum())
    ts = ts.reset_index()
    ts['date'] = pd.to_datetime(ts['date'])
    la_date = ts['date'].dt.date.tail(1)
    sales_val = sales_value(shopid).round(2)
    average_val = weekly_value(shopid).round(2)
    next_month_sales = forecast['yhat'].tail(1).round(2)
    item_fig = item_sold_graph(shopid)
    item_cat_fig = item_cat_sold_graph(shopid)
    weekly_fig = weekly_graph(shopid)
    sales_fig = sales_per_graph(shopid)

    return p_fig, p_com_fig, shop_name, la_date, sales_val, average_val, next_month_sales, item_fig, weekly_fig,item_cat_fig, sales_fig


# if __name__ == "__main__":
#     app.run_server(debug=True)
