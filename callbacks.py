import numpy as np
from dash import ALL, MATCH, Input, Output, State, callback_context, html
from dash.exceptions import PreventUpdate

from utils import apply_operation, apply_scaling, create_plot, prepare_plot_data


def register_callbacks(app):
    # Update button styles based on active display
    @app.callback(
        [Output(f"display-{i}-btn", "outline") for i in range(1, 5)],
        [Input("active-display", "children")],
    )
    def update_button_styles(active_display):
        active_display = int(active_display) if active_display else 1
        return [i != active_display for i in range(1, 5)]

    # Update settings title based on active display
    @app.callback(
        Output("settings-title", "children"), [Input("active-display", "children")]
    )
    def update_settings_title(active_display):
        return f"Settings for Display {active_display}"

    # Update active display when buttons are clicked
    @app.callback(
        Output("active-display", "children"),
        [Input(f"display-{i}-btn", "n_clicks") for i in range(1, 5)],
        [State("active-display", "children")],
    )
    def update_active_display(*args):
        n_clicks = args[:-1]
        active_display = args[-1]

        ctx = callback_context
        if not ctx.triggered:
            return active_display

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        display_id = button_id.split("-")[1]

        return display_id

    # Load settings when active display changes
    @app.callback(
        [
            Output("operation-dropdown", "value"),
            Output("scaling-dropdown", "value"),
            Output("view-dropdown", "value"),
            Output("shape-dropdown", "value"),
            Output("num-arrows-input", "value"),
            Output("display-options", "value"),
        ],
        [Input("active-display", "children")],
        [State(f"display-{i}-settings", "data") for i in range(1, 5)],
    )
    def load_display_settings(active_display, *settings_data):
        active_idx = int(active_display) - 1
        settings = settings_data[active_idx]

        return [
            settings["operation"],
            settings["scaling"],
            settings["view"],
            settings["shape"],
            settings["num_arrows"],
            settings["display_options"],
        ]

    # Save settings for Display 1
    @app.callback(
        Output("display-1-settings", "data"),
        [
            Input("operation-dropdown", "value"),
            Input("scaling-dropdown", "value"),
            Input("view-dropdown", "value"),
            Input("shape-dropdown", "value"),
            Input("num-arrows-input", "value"),
            Input("display-options", "value"),
        ],
        [
            State("active-display", "children"),
            State("display-1-settings", "data"),
        ],
    )
    def save_display_1_settings(
        operation,
        scaling,
        view,
        shape,
        num_arrows,
        display_options,
        active_display,
        current_settings,
    ):
        if active_display != "1":
            raise PreventUpdate

        current_settings.update(
            {
                "operation": operation,
                "scaling": scaling,
                "view": view,
                "shape": shape,
                "num_arrows": num_arrows if num_arrows else 12,
                "display_options": display_options if display_options else [],
            }
        )

        return current_settings

    # Save settings for Display 2
    @app.callback(
        Output("display-2-settings", "data"),
        [
            Input("operation-dropdown", "value"),
            Input("scaling-dropdown", "value"),
            Input("view-dropdown", "value"),
            Input("shape-dropdown", "value"),
            Input("num-arrows-input", "value"),
            Input("display-options", "value"),
        ],
        [
            State("active-display", "children"),
            State("display-2-settings", "data"),
        ],
    )
    def save_display_2_settings(
        operation,
        scaling,
        view,
        shape,
        num_arrows,
        display_options,
        active_display,
        current_settings,
    ):
        if active_display != "2":
            raise PreventUpdate

        current_settings.update(
            {
                "operation": operation,
                "scaling": scaling,
                "view": view,
                "shape": shape,
                "num_arrows": num_arrows if num_arrows else 12,
                "display_options": display_options if display_options else [],
            }
        )

        return current_settings

    # Save settings for Display 3
    @app.callback(
        Output("display-3-settings", "data"),
        [
            Input("operation-dropdown", "value"),
            Input("scaling-dropdown", "value"),
            Input("view-dropdown", "value"),
            Input("shape-dropdown", "value"),
            Input("num-arrows-input", "value"),
            Input("display-options", "value"),
        ],
        [
            State("active-display", "children"),
            State("display-3-settings", "data"),
        ],
    )
    def save_display_3_settings(
        operation,
        scaling,
        view,
        shape,
        num_arrows,
        display_options,
        active_display,
        current_settings,
    ):
        if active_display != "3":
            raise PreventUpdate

        current_settings.update(
            {
                "operation": operation,
                "scaling": scaling,
                "view": view,
                "shape": shape,
                "num_arrows": num_arrows if num_arrows else 12,
                "display_options": display_options if display_options else [],
            }
        )

        return current_settings

    # Save settings for Display 4
    @app.callback(
        Output("display-4-settings", "data"),
        [
            Input("operation-dropdown", "value"),
            Input("scaling-dropdown", "value"),
            Input("view-dropdown", "value"),
            Input("shape-dropdown", "value"),
            Input("num-arrows-input", "value"),
            Input("display-options", "value"),
        ],
        [
            State("active-display", "children"),
            State("display-4-settings", "data"),
        ],
    )
    def save_display_4_settings(
        operation,
        scaling,
        view,
        shape,
        num_arrows,
        display_options,
        active_display,
        current_settings,
    ):
        if active_display != "4":
            raise PreventUpdate

        current_settings.update(
            {
                "operation": operation,
                "scaling": scaling,
                "view": view,
                "shape": shape,
                "num_arrows": num_arrows if num_arrows else 12,
                "display_options": display_options if display_options else [],
            }
        )

        return current_settings

    # Update operation names and matrices for each display
    for i in range(1, 5):

        @app.callback(
            [
                Output(f"display-{i}-operation-name", "children"),
                Output(f"display-{i}-matrix", "children"),
            ],
            [
                Input(f"display-{i}-settings", "data"),
                Input(f"a11", "value"),
                Input(f"a12", "value"),
                Input(f"a21", "value"),
                Input(f"a22", "value"),
            ],
        )
        def update_display_info(settings, a11, a12, a21, a22, display_id=i):
            # Get the matrix
            base_matrix = np.array(
                [
                    [a11 if a11 is not None else 1, a12 if a12 is not None else 0],
                    [a21 if a21 is not None else 0, a22 if a22 is not None else 1],
                ]
            )

            # Apply the operation to get the actual matrix for this display
            matrix = base_matrix.copy()
            operation = settings.get("operation", "none")

            if operation != "none":
                matrix = apply_operation(matrix, operation)
                operation_name = operation.capitalize()
            else:
                operation_name = "Original"

            # Apply scaling if needed
            scaling = settings.get("scaling", "original")
            if scaling != "original":
                matrix = apply_scaling(matrix, scaling)
                operation_name += f" ({scaling.capitalize()})"

            # Format the matrix for display
            matrix_text = format_matrix(matrix)

            return operation_name, matrix_text

    # Main callback to update all plots with synchronized axes
    @app.callback(
        [Output(f"display-{i}-graph", "figure") for i in range(1, 5)],
        [
            # Matrix inputs
            Input(f"a{i}{j}", "value")
            for i in range(1, 3)
            for j in range(1, 3)
        ]
        + [
            # Control inputs for updates
            Input(f"display-{i}-settings", "data")
            for i in range(1, 5)
        ],
    )
    def update_displays(*inputs):
        # Extract inputs
        matrix_values = inputs[:4]
        display_settings = inputs[4:8]

        # Ensure we have valid matrix values (default to identity if any are None)
        matrix_values = [float(val) if val is not None else 0 for val in matrix_values]
        if all(val == 0 for val in matrix_values):
            # If all values are 0, use identity to avoid singularity
            matrix_values = [1, 0, 0, 1]

        # Create 2x2 matrix
        base_matrix = np.array(matrix_values).reshape(2, 2)

        # First pass: Calculate all plot data to determine the overall axes range
        all_plot_data = []
        all_points_x = []
        all_points_y = []

        # Calculate all plot data and collect points for axis calculation
        for settings in display_settings:
            # Apply operation and scaling based on individual display settings
            matrix = base_matrix.copy()
            matrix = apply_operation(matrix, settings["operation"])
            matrix = apply_scaling(matrix, settings["scaling"])

            # Prepare plot data
            plot_data = prepare_plot_data(
                matrix,
                settings["shape"],
                settings["num_arrows"],
                settings["view"],
                settings["display_options"],
            )

            all_plot_data.append(plot_data)

            # Collect points for axis range calculation - include ALL relevant points
            # Consider all points that will be shown in the plot
            for key in ["unmapped_points", "mapped_points"]:
                if len(plot_data[key]) > 0:
                    all_points_x.extend(plot_data[key][:, 0])
                    all_points_y.extend(plot_data[key][:, 1])

            # Also consider arrow endpoints for mapped reference arrows which may extend beyond the shape
            for key in ["mapped_ref_arrows"]:
                if key in plot_data:
                    for _, _, x1, y1 in plot_data[key]:
                        all_points_x.append(x1)
                        all_points_y.append(y1)

        # Calculate the global axis range if we have points
        global_axis_range = None
        if all_points_x and all_points_y:
            x_min, x_max = min(all_points_x), max(all_points_x)
            y_min, y_max = min(all_points_y), max(all_points_y)

            # Make sure range is square (equal x and y range)
            x_range = x_max - x_min
            y_range = y_max - y_min
            max_range = max(x_range, y_range)

            # Center the range and add minimal padding (10% instead of 20%)
            padding = max_range * 0.05  # Reduced padding for larger display area
            x_center = (x_max + x_min) / 2
            y_center = (y_max + y_min) / 2

            # Make sure we always include the origin with sufficient padding
            # This ensures reference vectors are always visible
            min_range = 2.2  # Minimum range to ensure the unit circle fits
            max_range = max(max_range, min_range)

            global_axis_range = {
                "x": [
                    x_center - max_range / 2 - padding,
                    x_center + max_range / 2 + padding,
                ],
                "y": [
                    y_center - max_range / 2 - padding,
                    y_center + max_range / 2 + padding,
                ],
            }

        # Second pass: Create figures with the global axis range
        figures = []
        for i, (plot_data, settings) in enumerate(zip(all_plot_data, display_settings)):
            # Create figure with global axis range
            fig = create_plot(plot_data, settings["display_options"], global_axis_range)
            figures.append(fig)

        return figures


def format_matrix(matrix):
    """Format a 2x2 matrix for display with one decimal place, on two lines with HTML."""
    return html.Div(
        [
            html.Div(f"[ {matrix[0][0]:.1f}  {matrix[0][1]:.1f} ]"),
            html.Div(f"[ {matrix[1][0]:.1f}  {matrix[1][1]:.1f} ]"),
        ],
        style={"lineHeight": "1.1"},
    )
