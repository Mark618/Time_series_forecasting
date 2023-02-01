import dash
import os
from flask import send_from_directory

external_stylesheets = ['/assets/materialize.css', 'https://fonts.googleapis.com/icon?family=Material+Icons']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Sales Forecasting', meta_tags=[{
    'name': 'viewport',
    'content': 'width=device-width, initial-scale=1.0'
}], external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"],
                url_base_pathname='/apps/')

app.config.suppress_callback_exceptions = True
server = app.server


@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
