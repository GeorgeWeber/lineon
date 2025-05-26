import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from callbacks import register_callbacks
from layout import create_layout

# Initialize the app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
)  # Added this option
app.title = "Lineon"

# Set the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
