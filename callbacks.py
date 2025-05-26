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

    # Update matrix selection button styles - modify to update immediately
    @app.callback(
        [
            Output(f"matrix-{matrix_id}-btn", "outline")
            for matrix_id in ["A", "B", "C", "D"]
        ],
        [
            Input("active-display", "children"),
            # Input from each matrix button directly instead of using the temp trigger
            Input("matrix-A-btn", "n_clicks"),
            Input("matrix-B-btn", "n_clicks"),
            Input("matrix-C-btn", "n_clicks"),
            Input("matrix-D-btn", "n_clicks"),
        ],
        [State(f"display-{i}-settings", "data") for i in range(1, 5)],
    )
    def update_matrix_button_styles(active_display, *args):
        if not active_display:
            return [False, True, True, True]  # Default to matrix A selected

        ctx = callback_context
        button_clicks = args[:4]  # Get button click counts
        settings_data = args[4:]  # Get settings data

        # Default to showing current selection from settings
        active_idx = int(active_display) - 1
        settings = settings_data[active_idx]
        selected_matrix = settings.get("matrix", "A")  # Default to A if not specified

        # Check if the trigger was one of the matrix buttons
        if ctx.triggered and any(
            f"matrix-{m}-btn" in ctx.triggered[0]["prop_id"]
            for m in ["A", "B", "C", "D"]
        ):
            # If so, extract which matrix was clicked from the trigger ID
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            selected_matrix = button_id.split("-")[1]  # Extract "A", "B", "C", or "D"

        # Return the current selection state
        return [matrix_id != selected_matrix for matrix_id in ["A", "B", "C", "D"]]

    # Handle matrix button clicks - update to set the matrix immediately
    @app.callback(
        Output("temp-trigger", "children"),
        [
            Input(f"matrix-{matrix_id}-btn", "n_clicks")
            for matrix_id in ["A", "B", "C", "D"]
        ],
        [State("active-display", "children")],
    )
    def handle_matrix_button_click(*args):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        matrix_id = button_id.split("-")[1]
        active_display = args[-1]

        return f"{active_display}:{matrix_id}"

    # Update display settings with selected matrix - add allow_duplicate=True
    @app.callback(
        [
            Output(f"display-{i}-settings", "data", allow_duplicate=True)
            for i in range(1, 5)
        ],
        [Input("temp-trigger", "children")],
        [State(f"display-{i}-settings", "data") for i in range(1, 5)],
        prevent_initial_call=True,  # Prevent initial callback to avoid conflicts
    )
    def update_display_matrix(trigger, *settings_data):
        if not trigger:
            raise PreventUpdate

        try:
            active_display, matrix_id = trigger.split(":")
            active_idx = int(active_display) - 1
        except (ValueError, AttributeError):
            raise PreventUpdate

        # Copy all settings
        new_settings = list(settings_data)

        # Update only the active display's matrix setting
        new_settings[active_idx] = {**new_settings[active_idx], "matrix": matrix_id}

        return new_settings

    # Add a hidden div for temporary trigger storage
    app.layout.children.append(html.Div(id="temp-trigger", style={"display": "none"}))

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
        Output("display-1-settings", "data", allow_duplicate=True),
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
        prevent_initial_call=True,  # Prevent initial callback to avoid conflicts
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
        Output("display-2-settings", "data", allow_duplicate=True),
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
        prevent_initial_call=True,  # Prevent initial callback to avoid conflicts
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
        Output("display-3-settings", "data", allow_duplicate=True),
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
        prevent_initial_call=True,  # Prevent initial callback to avoid conflicts
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
        Output("display-4-settings", "data", allow_duplicate=True),
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
        prevent_initial_call=True,  # Prevent initial callback to avoid conflicts
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
    # Fix the loop with a function factory to avoid callback duplication
    def create_display_info_callback(display_id):
        @app.callback(
            [
                Output(f"display-{display_id}-operation-name", "children"),
                Output(f"display-{display_id}-matrix", "children"),
            ],
            [
                Input(f"display-{display_id}-settings", "data"),
                # Input matrix values for all matrices
                Input("A-a11", "value"),
                Input("A-a12", "value"),
                Input("A-a21", "value"),
                Input("A-a22", "value"),
                Input("B-a11", "value"),
                Input("B-a12", "value"),
                Input("B-a21", "value"),
                Input("B-a22", "value"),
                Input("C-a11", "value"),
                Input("C-a12", "value"),
                Input("C-a21", "value"),
                Input("C-a22", "value"),
                Input("D-a11", "value"),
                Input("D-a12", "value"),
                Input("D-a21", "value"),
                Input("D-a22", "value"),
            ],
        )
        def update_display_info(settings, *matrix_values):
            # Get the selected matrix and its values
            matrix_id = settings.get("matrix", "A")  # Default to A

            # Find the base index for the selected matrix values
            matrix_idx = {"A": 0, "B": 4, "C": 8, "D": 12}[matrix_id]

            # Get the 2x2 matrix values for the selected matrix
            a11 = matrix_values[matrix_idx]
            a12 = matrix_values[matrix_idx + 1]
            a21 = matrix_values[matrix_idx + 2]
            a22 = matrix_values[matrix_idx + 3]

            # Create matrix with defaults if values are None
            base_matrix = np.array(
                [
                    [a11 if a11 is not None else 1, a12 if a12 is not None else 0],
                    [a21 if a21 is not None else 0, a22 if a22 is not None else 1],
                ]
            )

            # Apply operations as before
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

            # Include the matrix ID in the operation name
            operation_name = f"{matrix_id}: {operation_name}"

            # Format the matrix for display
            matrix_text = format_matrix(matrix)

            return operation_name, matrix_text

        return update_display_info

    # Create a separate callback for each display
    for i in range(1, 5):
        create_display_info_callback(i)

    # Main callback to update all plots with synchronized axes
    @app.callback(
        [Output(f"display-{i}-graph", "figure") for i in range(1, 5)],
        [
            # Input matrix values for all matrices
            Input("A-a11", "value"),
            Input("A-a12", "value"),
            Input("A-a21", "value"),
            Input("A-a22", "value"),
            Input("B-a11", "value"),
            Input("B-a12", "value"),
            Input("B-a21", "value"),
            Input("B-a22", "value"),
            Input("C-a11", "value"),
            Input("C-a12", "value"),
            Input("C-a21", "value"),
            Input("C-a22", "value"),
            Input("D-a11", "value"),
            Input("D-a12", "value"),
            Input("D-a21", "value"),
            Input("D-a22", "value"),
        ]
        + [
            # Control inputs for updates
            Input(f"display-{i}-settings", "data")
            for i in range(1, 5)
        ],
    )
    def update_displays(*inputs):
        # Extract inputs
        matrix_values = inputs[:16]  # All matrix inputs
        display_settings = inputs[16:20]  # Display settings

        # Create a dictionary of base matrices
        base_matrices = {
            "A": get_matrix_from_values(matrix_values[0:4]),
            "B": get_matrix_from_values(matrix_values[4:8]),
            "C": get_matrix_from_values(matrix_values[8:12]),
            "D": get_matrix_from_values(matrix_values[12:16]),
        }

        # First pass: Calculate all plot data to determine the overall axes range
        all_plot_data = []
        all_points_x = []
        all_points_y = []

        # Calculate all plot data and collect points for axis calculation
        for settings in display_settings:
            # Get the selected matrix for this display
            matrix_id = settings.get("matrix", "A")
            base_matrix = base_matrices[matrix_id]

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


def get_matrix_from_values(values):
    """Helper function to create a 2x2 matrix from 4 values with defaults."""
    a11, a12, a21, a22 = values

    # Use defaults if values are None
    a11 = a11 if a11 is not None else 1
    a12 = a12 if a12 is not None else 0
    a21 = a21 if a21 is not None else 0
    a22 = a22 if a22 is not None else 1

    # Ensure we have a valid matrix (default to identity if all zeros)
    if all(val == 0 for val in [a11, a12, a21, a22]):
        a11 = a22 = 1

    return np.array([[a11, a12], [a21, a22]])


def format_matrix(matrix):
    """Format a 2x2 matrix for display with one decimal place, on two lines with HTML."""
    return html.Div(
        [
            html.Div(f"[ {matrix[0][0]:.1f}  {matrix[0][1]:.1f} ]"),
            html.Div(f"[ {matrix[1][0]:.1f}  {matrix[1][1]:.1f} ]"),
        ],
        style={"lineHeight": "1.1"},
    )
