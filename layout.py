import dash_bootstrap_components as dbc
from dash import dcc, html


def create_display(id_prefix, title):
    """
    Creates a display component with the given ID prefix and title.
    """
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.Div(title, className="card-title"),
                    html.Div(
                        id=f"{id_prefix}-operation-name", className="operation-name"
                    ),
                    html.Div(id=f"{id_prefix}-matrix", className="matrix-display"),
                ]
            ),
            dbc.CardBody(
                [
                    dcc.Graph(
                        id=f"{id_prefix}-graph",
                        config={"displayModeBar": False},
                        className="display-graph",
                    )
                ]
            ),
        ],
        className="display-card",
    )


def create_layout():
    return dbc.Container(
        [
            # Header
            dbc.Row(
                dbc.Col(
                    html.Div(
                        [
                            html.H1(
                                "Lineon", className="text-center text-primary mb-2"
                            ),
                            html.H5(
                                "Visualizing 2D Linear Transformations",
                                className="text-center text-info mb-4",  # Changed from text-light to text-info for better contrast
                                style={
                                    "text-shadow": "1px 1px 2px rgba(0,0,0,0.5)",  # Add subtle shadow for depth
                                    "letter-spacing": "0.5px",  # Slightly increase letter spacing
                                    "font-weight": "500",  # Medium weight for better visibility
                                },
                            ),
                        ]
                    )
                )
            ),
            # Matrix Input
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                "Matrix Input", className="text-white bg-secondary"
                            ),
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Input(
                                                id=f"a{i}{j}",
                                                type="number",
                                                value=1 if i == j else 0,
                                                className="form-control text-center",
                                                step=0.01,
                                            ),
                                            width=3,
                                        )
                                        for i in range(1, 3)
                                        for j in range(1, 3)
                                    ],
                                    justify="center",
                                )
                            ),
                        ],
                        className="bg-dark mb-4",
                    )
                )
            ),
            # Sidebar and Plots
            dbc.Row(
                [
                    # Sidebar
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Display Settings",
                                    className="text-white bg-secondary",
                                ),
                                dbc.CardBody(
                                    [
                                        # Display Buttons with more obvious selection state
                                        html.H6("Select Display", className="mb-2"),
                                        dbc.ButtonGroup(
                                            [
                                                dbc.Button(
                                                    f"Display {i}",
                                                    id=f"display-{i}-btn",
                                                    color="primary",
                                                    outline=True,
                                                    className="me-1 mb-2",
                                                    n_clicks=0,
                                                )
                                                for i in range(1, 5)
                                            ],
                                            className="mb-3 d-flex flex-wrap",
                                        ),
                                        # Selected Display Options
                                        html.Div(
                                            [
                                                # Display title
                                                html.H5(
                                                    "Settings for Display 1",
                                                    id="settings-title",
                                                    className="text-center mb-3",
                                                ),
                                                html.H6("Operation", className="mt-3"),
                                                dcc.Dropdown(
                                                    id="operation-dropdown",
                                                    options=[
                                                        {
                                                            "label": "None",
                                                            "value": "none",
                                                        },
                                                        {
                                                            "label": "Transpose",
                                                            "value": "transpose",
                                                        },
                                                        {
                                                            "label": "Symmetric",
                                                            "value": "symmetric",
                                                        },
                                                        {
                                                            "label": "Skew",
                                                            "value": "skew",
                                                        },
                                                        {
                                                            "label": "Inverse",
                                                            "value": "inverse",
                                                        },
                                                        {
                                                            "label": "Squared",
                                                            "value": "squared",
                                                        },
                                                        {
                                                            "label": "Cubed",
                                                            "value": "cubed",
                                                        },
                                                        {
                                                            "label": "Rotation",
                                                            "value": "rotation",
                                                        },
                                                        {
                                                            "label": "Stretch",
                                                            "value": "stretch",
                                                        },
                                                    ],
                                                    value="none",
                                                    className="mb-3",
                                                ),
                                                html.H6("Scaling", className="mt-3"),
                                                dcc.Dropdown(
                                                    id="scaling-dropdown",
                                                    options=[
                                                        {
                                                            "label": "Original",
                                                            "value": "original",
                                                        },
                                                        {
                                                            "label": "Normalized",
                                                            "value": "normalized",
                                                        },
                                                        {
                                                            "label": "Determinant-scaled",
                                                            "value": "determinant",
                                                        },
                                                        {
                                                            "label": "Halved",
                                                            "value": "halved",
                                                        },
                                                        {
                                                            "label": "Doubled",
                                                            "value": "doubled",
                                                        },
                                                    ],
                                                    value="original",
                                                    className="mb-3",
                                                ),
                                                html.H6("View Mode", className="mt-3"),
                                                dcc.Dropdown(
                                                    id="view-dropdown",
                                                    options=[
                                                        {
                                                            "label": "Map",
                                                            "value": "map",
                                                        },
                                                        {
                                                            "label": "Difference",
                                                            "value": "difference",
                                                        },
                                                        {
                                                            "label": "Normal",
                                                            "value": "normal",
                                                        },
                                                    ],
                                                    value="map",
                                                    className="mb-3",
                                                ),
                                                html.H6("Shape", className="mt-3"),
                                                dcc.Dropdown(
                                                    id="shape-dropdown",
                                                    options=[
                                                        {
                                                            "label": "Circle",
                                                            "value": "circle",
                                                        },
                                                        {
                                                            "label": "Square",
                                                            "value": "square",
                                                        },
                                                        {
                                                            "label": "Hexagon",
                                                            "value": "hexagon",
                                                        },
                                                    ],
                                                    value="circle",
                                                    className="mb-3",
                                                ),
                                                html.H6(
                                                    "Number of Arrows", className="mt-3"
                                                ),
                                                dcc.Input(
                                                    id="num-arrows-input",
                                                    type="number",
                                                    value=12,
                                                    min=4,
                                                    max=100,
                                                    step=1,
                                                    className="form-control mb-3",
                                                ),
                                                html.H6(
                                                    "Display Options", className="mt-3"
                                                ),
                                                dbc.Checklist(
                                                    id="display-options",
                                                    options=[
                                                        {
                                                            "label": "Show Unmapped Arrows",
                                                            "value": "show_unmapped_arrows",
                                                        },
                                                        {
                                                            "label": "Show Mapped Arrows",
                                                            "value": "show_mapped_arrows",
                                                        },
                                                        {
                                                            "label": "Show Unmapped Outline",
                                                            "value": "show_unmapped_outline",
                                                        },
                                                        {
                                                            "label": "Show Mapped Outline",
                                                            "value": "show_mapped_outline",
                                                        },
                                                        {
                                                            "label": "Show Unmapped Reference Arrows",
                                                            "value": "show_unmapped_reference",
                                                        },
                                                        {
                                                            "label": "Show Mapped Reference Arrows",
                                                            "value": "show_mapped_reference",
                                                        },
                                                    ],
                                                    value=[
                                                        "show_unmapped_arrows",
                                                        "show_mapped_arrows",
                                                        "show_unmapped_outline",
                                                        "show_mapped_outline",
                                                    ],
                                                    className="mb-3",
                                                ),
                                                # Hidden div to store active display
                                                html.Div(
                                                    id="active-display",
                                                    style={"display": "none"},
                                                    children="1",
                                                ),
                                                # Storage for each display's settings
                                                dcc.Store(
                                                    id=f"display-1-settings",
                                                    data={
                                                        "operation": "none",
                                                        "scaling": "original",
                                                        "view": "map",
                                                        "shape": "circle",
                                                        "num_arrows": 12,
                                                        "display_options": [
                                                            "show_unmapped_arrows",
                                                            "show_mapped_arrows",
                                                            "show_unmapped_outline",
                                                            "show_mapped_outline",
                                                        ],
                                                    },
                                                ),
                                                dcc.Store(
                                                    id=f"display-2-settings",
                                                    data={
                                                        "operation": "none",
                                                        "scaling": "original",
                                                        "view": "map",
                                                        "shape": "circle",
                                                        "num_arrows": 12,
                                                        "display_options": [
                                                            "show_unmapped_arrows",
                                                            "show_mapped_arrows",
                                                            "show_unmapped_outline",
                                                            "show_mapped_outline",
                                                        ],
                                                    },
                                                ),
                                                dcc.Store(
                                                    id=f"display-3-settings",
                                                    data={
                                                        "operation": "none",
                                                        "scaling": "original",
                                                        "view": "map",
                                                        "shape": "circle",
                                                        "num_arrows": 12,
                                                        "display_options": [
                                                            "show_unmapped_arrows",
                                                            "show_mapped_arrows",
                                                            "show_unmapped_outline",
                                                            "show_mapped_outline",
                                                        ],
                                                    },
                                                ),
                                                dcc.Store(
                                                    id=f"display-4-settings",
                                                    data={
                                                        "operation": "none",
                                                        "scaling": "original",
                                                        "view": "map",
                                                        "shape": "circle",
                                                        "num_arrows": 12,
                                                        "display_options": [
                                                            "show_unmapped_arrows",
                                                            "show_mapped_arrows",
                                                            "show_unmapped_outline",
                                                            "show_mapped_outline",
                                                        ],
                                                    },
                                                ),
                                            ],
                                            id="sidebar-options",
                                            className="text-light",
                                        ),
                                    ]
                                ),
                            ],
                            className="bg-dark",
                        ),
                        width=3,
                    ),
                    # Plots
                    dbc.Col(
                        dbc.Row(
                            [
                                dbc.Col(
                                    create_display(f"display-{i}", f"Display {i}"),
                                    width=6,
                                )
                                for i in range(1, 5)
                            ],
                            className="g-3",
                        ),
                        width=9,
                    ),
                ]
            ),
        ],
        fluid=True,
        className="p-4",
    )
