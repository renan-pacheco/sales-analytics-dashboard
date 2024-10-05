import dash
# import dash_auth

# Define the global font for the app:
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

# Instantiate the app:
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)

# Instantiate the server:
app.scripts.config.server_locally = True
server = app.server