import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app import app

path = 'data/'
sales = pd.read_csv(path + 'sales_train.csv', parse_dates=["date"])
item_cat = pd.read_csv(path + 'item_categories.csv')
item = pd.read_csv(path + 'items.csv')
shop = pd.read_csv(path + 'shops.csv')

grouped = pd.DataFrame(sales.groupby(['date_block_num', 'shop_id'])['item_cnt_day'].sum().reset_index())
shop_test = pd.DataFrame(grouped.groupby(['shop_id'])['item_cnt_day'].sum().reset_index())
shop_test = shop_test.merge(shop, how='left', on='shop_id')

item_grp = pd.DataFrame(sales.groupby(['date_block_num', 'item_id'])['item_cnt_day'].sum().reset_index())
item_test = pd.DataFrame(item_grp.groupby(['item_id'])['item_cnt_day'].sum().reset_index())
item_test = item_test.merge(item, how='left', on='item_id')
item_test = item_test.merge(item_cat, how='left', on='item_category_id')
item_test.drop(['item_category_id'], axis=1, inplace=True)

sales_comp = pd.read_csv(path + 'grouped.csv')

dailysales = pd.DataFrame(sales.groupby(['date'])['total_sales'].sum().reset_index())
dailysales.set_index('date', inplace=True)
weekly_resampled_data = dailysales.resample('W').mean()
weekly_resampled_data.reset_index(inplace=True)

# Cumulative Sales
cumulative_sales = pd.DataFrame(sales.groupby(['year', 'month'])['total_sales'].sum().reset_index())
cumulative_sales['cumulative'] = cumulative_sales.total_sales.cumsum()
sales_sum = cumulative_sales[cumulative_sales['year'] == 2015]

fig = px.pie(shop_test.sort_values('item_cnt_day', ascending=False).head(5), values='item_cnt_day',
             names='shop_name', color_discrete_sequence=px.colors.sequential.Mint, title='Top 5 Item Sold by Shop',
             labels={'shop_name': 'Shop Name', 'item_cnt_day': 'Item count day'}
             )
fig.update_traces(textposition='inside', textinfo='percent+label')

fig1 = px.bar(item_test.sort_values('item_cnt_day', ascending=False).head(), x="item_name", y="item_cnt_day",
              color_discrete_sequence=['rgb(99, 166, 160)'],
              title='Top 5 Item Sold(unit)')
fig1.update_layout(plot_bgcolor="#FFFFFF",
                   # xaxis=dict(title="Total Sales"),
                   yaxis=dict(title=""),
                   xaxis=dict(title="")
                   )

fig2 = px.line(sales_comp, x="month", y="total_sales", color='year',
               color_discrete_sequence=px.colors.sequential.Mint_r, title='Sales Revenue')
fig2.update_layout(plot_bgcolor="#FFFFFF",
                   xaxis=dict(title="Month"),
                   yaxis=dict(title="")
                   )

fig3 = px.bar(weekly_resampled_data, y='total_sales', x='date', text='total_sales',
              color_discrete_sequence=px.colors.sequential.Mint_r, title='Average Weekly Sales Revenue')
fig3.update_traces(textposition='outside')
fig3.update_layout(plot_bgcolor="#FFFFFF",
                   xaxis=dict(title=""),
                   yaxis=dict(title=""),
                   bargap=0.15
                   )

fig4 = px.bar(cumulative_sales[cumulative_sales['year'] == 2013], x="month", y='cumulative', text='cumulative',
              color_discrete_sequence=px.colors.sequential.Mint_r, title='Cumulative Sales for Year 2015')
fig4.update_traces(textposition='outside')
fig4.update_layout(plot_bgcolor="#FFFFFF",
                   xaxis=dict(title="Month"),
                   yaxis=dict(title=""),
                   bargap=0.15
                   )

# external_stylesheets = ['../assets/materialize.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Sales Forecasting', meta_tags=[{
#     "name": "viewport", "content": "width=device-width"
# }], external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"])

layout = html.Div(
    children=[
        html.Div(
            className='row',
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    shop.shop_id.count(),
                                                    className="card-title",
                                                    style={'text-align': 'center'}
                                                ),
                                                html.Div(
                                                    "Total No of Store",
                                                    className='container',
                                                    style={'text-align': 'center'})
                                            ],
                                            className='card-content'
                                        ),
                                    ],
                                    className='card'
                                )
                            ],
                            className='col s12 m6 l2'
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    sales_sum.total_sales.sum().round(2),
                                                    className="card-title",
                                                    style={'text-align': 'center'}
                                                ),
                                                html.Div(
                                                    "This Year Sales",
                                                    className='container',
                                                    style={'text-align': 'center'})
                                            ],
                                            className='card-content'
                                        ),
                                    ],
                                    className='card'
                                )
                            ],
                            className='col s12 m6 l2'
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    weekly_resampled_data.total_sales.mean().round(2),
                                                    className="card-title",
                                                    style={'text-align': 'center'}
                                                ),
                                                html.Div(
                                                    "Average Weekly Sales Revenue",
                                                    className='container',
                                                    style={'text-align': 'center'})
                                            ],
                                            className='card-content'
                                        ),
                                    ],
                                    className='card'
                                )
                            ],
                            className='col s12 m6 l3'
                        ),

                    ],
                ),
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(figure=fig),

                                            ],
                                        ),
                                    ],
                                    className='card-content'
                                ),
                            ],
                            className='card large'
                        ),
                    ],
                    className='col s12 m6 l4'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(figure=fig2, responsive=True),
                                            ],
                                        ),
                                    ],
                                    className='card-content'
                                ),
                            ],
                            className='card large'
                        )
                    ],
                    className='col s12 m6 l8'
                ),
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(figure=fig1),

                                            ],
                                        ),
                                    ],
                                    className='card-content'
                                ),
                            ],
                            className='card large'
                        ),
                    ],
                    className='col s12 m6 l5'
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(figure=fig3, responsive=True),
                                            ],
                                        ),
                                    ],
                                    className='card-content'
                                ),
                            ],
                            className='card large'
                        )
                    ],
                    className='col s12 m6 l7'
                ),
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(figure=fig4),

                                            ],
                                        ),
                                    ],
                                    className='card-content'
                                ),
                            ],
                            className='card large'
                        ),
                    ],
                    className='col s12 m6 l12'
                ),
            ]
        )
    ]

)

# if __name__ == "__main__":
#     app.run_server(debug=True)
