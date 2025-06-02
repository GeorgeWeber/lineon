import numpy as np
import plotly.graph_objects as go
import scipy.linalg  # Add this import for polar decomposition


def apply_operation(matrix, operation):
    """Apply matrix operation based on selection."""
    if operation == "none":
        return matrix
    elif operation == "transpose":
        return matrix.T
    elif operation == "symmetric":
        return (matrix + matrix.T) / 2
    elif operation == "skew":
        return (matrix - matrix.T) / 2
    elif operation == "inverse":
        try:
            return np.linalg.inv(matrix)
        except np.linalg.LinAlgError:
            # Return identity matrix if inverse doesn't exist
            return np.eye(2)
    elif operation == "squared":
        return matrix @ matrix
    elif operation == "cubed":
        return matrix @ matrix @ matrix
    elif operation == "rotation":
        # Rotation component from polar decomposition (orthogonal)
        try:
            u, p = scipy.linalg.polar(matrix)
            return u  # orthogonal component (rotation)
        except:
            return np.eye(2)
    elif operation == "stretch":
        # Stretch component from polar decomposition (positive-semidefinite)
        try:
            u, p = scipy.linalg.polar(matrix)
            return p  # positive semi-definite component (stretch)
        except:
            return np.eye(2)
    elif operation == "volumetric":
        # Volumetric part: 1/2 tr(M) * identity
        trace = np.trace(matrix)
        return 0.5 * trace * np.eye(2)
    elif operation == "deviatoric":
        # Deviatoric part: M - 1/2 tr(M) * identity
        trace = np.trace(matrix)
        return matrix - 0.5 * trace * np.eye(2)
    elif operation == "subtract_identity":
        # Subtract identity matrix
        return matrix - np.eye(2)

    return matrix


def apply_scaling(matrix, scaling):
    """Apply scaling to matrix based on selection."""
    if scaling == "original":
        return matrix
    elif scaling == "normalized":
        try:
            norm = np.linalg.norm(matrix)
            if norm > 0:
                return matrix / norm
        except:
            pass
    elif scaling == "determinant":
        try:
            det = np.linalg.det(matrix)
            if abs(det) > 1e-10:  # Avoid division by zero or very small values
                return matrix / det
        except:
            pass
    elif scaling == "halved":
        return matrix / 2
    elif scaling == "doubled":
        return matrix * 2
    return matrix


def generate_shape_points(shape_type, num_points):
    """Generate points for the selected shape."""
    if shape_type == "circle":
        theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        x = np.cos(theta)
        y = np.sin(theta)
    elif shape_type == "square":
        # Ensure at least 4 points (corners)
        n = max(num_points, 4)
        # Distribute points among the 4 sides
        points_per_side = n // 4
        remaining = n % 4

        # Generate corner points
        corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])

        points = []
        for i in range(4):
            start = corners[i]
            end = corners[(i + 1) % 4]
            # Number of points on this side (including start, excluding end)
            n_side = points_per_side + (1 if i < remaining else 0)
            for j in range(n_side):
                t = j / n_side
                point = start + t * (end - start)
                points.append(point)

        points = np.array(points)
        x, y = points[:, 0], points[:, 1]
    elif shape_type == "hexagon":
        # Ensure at least 6 points (corners)
        n = max(num_points, 6)
        theta = np.linspace(0, 2 * np.pi, 6, endpoint=False)
        corners = np.column_stack((np.cos(theta), np.sin(theta)))

        points = []
        for i in range(6):
            start = corners[i]
            end = corners[(i + 1) % 6]
            # Distribute remaining points
            n_side = (n // 6) + (1 if i < (n % 6) else 0)
            for j in range(n_side):
                t = j / n_side
                point = start + t * (end - start)
                points.append(point)

        points = np.array(points)
        x, y = points[:, 0], points[:, 1]
    else:
        # Default to circle
        theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        x = np.cos(theta)
        y = np.sin(theta)

    return np.column_stack((x, y))


def get_reference_vectors():
    """Return the reference unit vectors."""
    return np.array([[1, 0], [0, 1]])


def prepare_plot_data(matrix, shape_type, num_points, view_mode, display_options):
    """Prepare all data for plotting."""
    # Generate unmapped shape points
    unmapped_points = generate_shape_points(shape_type, num_points)

    # Map the points using the matrix
    mapped_points = unmapped_points @ matrix.T

    # Get reference vectors
    unmapped_ref = get_reference_vectors()
    mapped_ref = unmapped_ref @ matrix.T

    # Calculate arrows based on view mode
    if view_mode == "map":
        # Direct mapping: arrows start at origin
        unmapped_arrows = [(0, 0, x, y) for x, y in unmapped_points]
        mapped_arrows = [(0, 0, x, y) for x, y in mapped_points]

        # Points for outlines (tips of arrows)
        outline_unmapped_points = unmapped_points
        outline_mapped_points = mapped_points

    elif view_mode == "difference":
        # Difference: arrows start at unmapped points, show difference vector
        unmapped_arrows = [(0, 0, x, y) for x, y in unmapped_points]
        mapped_arrows = [
            (x1, y1, x2, y2)
            for (x1, y1), (x2, y2) in zip(unmapped_points, mapped_points)
        ]

        # Points for outlines (tips of arrows = unmapped points + difference)
        outline_unmapped_points = unmapped_points
        outline_mapped_points = mapped_points

    else:  # normal
        # Normal: arrows start at unmapped points
        unmapped_arrows = [(0, 0, x, y) for x, y in unmapped_points]

        # For normal mode, arrows start at unmapped point tips and extend by the mapped vector
        mapped_arrows = [
            (x1, y1, x1 + x2, y1 + y2)
            for (x1, y1), (x2, y2) in zip(unmapped_points, mapped_points)
        ]

        # Points for outlines (tips of mapped arrows = unmapped points + mapped vectors)
        outline_unmapped_points = unmapped_points
        outline_mapped_points = np.array(
            [
                [x1 + x2, y1 + y2]
                for (x1, y1), (x2, y2) in zip(unmapped_points, mapped_points)
            ]
        )

    # Reference arrows always start at origin
    unmapped_ref_arrows = [(0, 0, x, y) for x, y in unmapped_ref]
    mapped_ref_arrows = [(0, 0, x, y) for x, y in mapped_ref]

    return {
        "unmapped_points": outline_unmapped_points,
        "mapped_points": outline_mapped_points,
        "unmapped_arrows": unmapped_arrows,
        "mapped_arrows": mapped_arrows,
        "unmapped_ref_arrows": unmapped_ref_arrows,
        "mapped_ref_arrows": mapped_ref_arrows,
    }


def create_plot(plot_data, display_options, axis_range=None):
    """Create a plotly figure with all elements."""
    fig = go.Figure()

    # Add elements based on display options
    if "show_unmapped_arrows" in display_options:
        for x0, y0, x1, y1 in plot_data["unmapped_arrows"]:
            # Calculate arrow properties
            dx = x1 - x0
            dy = y1 - y0
            arrow_length = np.sqrt(dx**2 + dy**2)

            if arrow_length > 0:
                # Reduce arrowhead size by about half
                arrowhead_size = 0.05  # Changed from 0.1
                arrowhead_ratio = 1.0 - (arrowhead_size / arrow_length)
                # Calculate the actual line endpoint (slightly before the vector end)
                x_line_end = x0 + dx * arrowhead_ratio
                y_line_end = y0 + dy * arrowhead_ratio

                # Add line (stopping short of the end to make room for arrowhead)
                fig.add_trace(
                    go.Scatter(
                        x=[x0, x_line_end],
                        y=[y0, y_line_end],
                        mode="lines",
                        line=dict(color="rgba(200, 200, 200, 0.6)", width=1.5),
                        showlegend=False,
                    )
                )

                # Add arrowhead at the end of the vector
                # Calculate angle in degrees for arrowhead direction
                angle_degrees = np.degrees(np.arctan2(dy, dx))

                # Create a custom triangle for the arrowhead
                arrowhead_width = 0.04  # Changed from 0.08 (half the width)

                # Calculate triangle points for the arrowhead (oriented correctly)
                angle_rad = np.radians(angle_degrees)
                cos_a = np.cos(angle_rad)
                sin_a = np.sin(angle_rad)

                # Calculate arrowhead points
                arrow_x = [
                    x1,  # Tip
                    x1 - arrowhead_size * cos_a + arrowhead_width * sin_a,  # Back right
                    x1 - arrowhead_size * cos_a - arrowhead_width * sin_a,  # Back left
                    x1,  # Back to tip to close the shape
                ]
                arrow_y = [
                    y1,  # Tip
                    y1 - arrowhead_size * sin_a - arrowhead_width * cos_a,  # Back right
                    y1 - arrowhead_size * sin_a + arrowhead_width * cos_a,  # Back left
                    y1,  # Back to tip to close the shape
                ]

                fig.add_trace(
                    go.Scatter(
                        x=arrow_x,
                        y=arrow_y,
                        fill="toself",
                        fillcolor="rgba(200, 200, 200, 0.9)",
                        line=dict(color="rgba(200, 200, 200, 1.0)"),
                        mode="lines",
                        showlegend=False,
                    )
                )

                # Add small marker at the starting point
                fig.add_trace(
                    go.Scatter(
                        x=[x0],
                        y=[y0],
                        mode="markers",
                        marker=dict(
                            size=3,
                            color="rgba(200, 200, 200, 0.7)",
                        ),
                        showlegend=False,
                    )
                )

    if "show_mapped_arrows" in display_options:
        for x0, y0, x1, y1 in plot_data["mapped_arrows"]:
            # Calculate arrow properties
            dx = x1 - x0
            dy = y1 - y0
            arrow_length = np.sqrt(dx**2 + dy**2)

            if arrow_length > 0:
                # Stop the line slightly short for the arrowhead
                arrowhead_size = 0.06  # Changed from 0.12
                arrowhead_ratio = 1.0 - (arrowhead_size / arrow_length)
                # Calculate the actual line endpoint (slightly before the vector end)
                x_line_end = x0 + dx * arrowhead_ratio
                y_line_end = y0 + dy * arrowhead_ratio

                # Add line
                fig.add_trace(
                    go.Scatter(
                        x=[x0, x_line_end],
                        y=[y0, y_line_end],
                        mode="lines",
                        line=dict(color="rgba(255, 100, 100, 0.6)", width=1.5),
                        showlegend=False,
                    )
                )

                # Add custom arrowhead at the end
                angle_degrees = np.degrees(np.arctan2(dy, dx))
                arrowhead_width = 0.045  # Changed from 0.09

                # Calculate triangle points for the arrowhead
                angle_rad = np.radians(angle_degrees)
                cos_a = np.cos(angle_rad)
                sin_a = np.sin(angle_rad)

                arrow_x = [
                    x1,  # Tip
                    x1 - arrowhead_size * cos_a + arrowhead_width * sin_a,  # Back right
                    x1 - arrowhead_size * cos_a - arrowhead_width * sin_a,  # Back left
                    x1,  # Back to tip to close the shape
                ]
                arrow_y = [
                    y1,  # Tip
                    y1 - arrowhead_size * sin_a - arrowhead_width * cos_a,  # Back right
                    y1 - arrowhead_size * sin_a + arrowhead_width * cos_a,  # Back left
                    y1,  # Back to tip to close the shape
                ]

                fig.add_trace(
                    go.Scatter(
                        x=arrow_x,
                        y=arrow_y,
                        fill="toself",
                        fillcolor="rgba(255, 100, 100, 0.9)",
                        line=dict(color="rgba(255, 100, 100, 1.0)"),
                        mode="lines",
                        showlegend=False,
                    )
                )

                # Add small marker at the starting point
                fig.add_trace(
                    go.Scatter(
                        x=[x0],
                        y=[y0],
                        mode="markers",
                        marker=dict(
                            size=3,
                            color="rgba(255, 100, 100, 0.7)",
                        ),
                        showlegend=False,
                    )
                )

    # Add outlines
    if "show_unmapped_outline" in display_options:
        x = plot_data["unmapped_points"][:, 0]
        y = plot_data["unmapped_points"][:, 1]
        # Close the loop
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line=dict(color="rgba(255, 255, 255, 0.8)", width=2),
                showlegend=False,
            )
        )

    if "show_mapped_outline" in display_options:
        x = plot_data["mapped_points"][:, 0]
        y = plot_data["mapped_points"][:, 1]
        # Close the loop
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                line=dict(color="rgba(255, 100, 100, 0.8)", width=2),
                showlegend=False,
            )
        )

    # Add reference vectors with better arrowheads
    if "show_unmapped_reference" in display_options:
        # X-axis reference (green)
        x0, y0, x1, y1 = plot_data["unmapped_ref_arrows"][0]
        dx = x1 - x0
        dy = y1 - y0
        arrow_length = np.sqrt(dx**2 + dy**2)

        # Stop line short for arrowhead
        arrowhead_size = 0.075  # Changed from 0.15
        arrowhead_ratio = 1.0 - (arrowhead_size / arrow_length)
        x_line_end = x0 + dx * arrowhead_ratio
        y_line_end = y0 + dy * arrowhead_ratio

        fig.add_trace(
            go.Scatter(
                x=[x0, x_line_end],
                y=[y0, y_line_end],
                mode="lines",
                line=dict(color="rgba(50, 200, 50, 0.8)", width=2),
                showlegend=False,
            )
        )

        # Add custom arrowhead
        angle_degrees = np.degrees(np.arctan2(dy, dx))
        arrowhead_width = 0.055  # Changed from 0.11

        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        arrow_x = [
            x1,  # Tip
            x1 - arrowhead_size * cos_a + arrowhead_width * sin_a,  # Back right
            x1 - arrowhead_size * cos_a - arrowhead_width * sin_a,  # Back left
            x1,  # Back to tip to close the shape
        ]
        arrow_y = [
            y1,  # Tip
            y1 - arrowhead_size * sin_a - arrowhead_width * cos_a,  # Back right
            y1 - arrowhead_size * sin_a + arrowhead_width * cos_a,  # Back left
            y1,  # Back to tip to close the shape
        ]

        fig.add_trace(
            go.Scatter(
                x=arrow_x,
                y=arrow_y,
                fill="toself",
                fillcolor="rgba(50, 200, 50, 0.9)",
                line=dict(color="rgba(50, 200, 50, 1.0)"),
                mode="lines",
                showlegend=False,
            )
        )

        # Y-axis reference (blue)
        x0, y0, x1, y1 = plot_data["unmapped_ref_arrows"][1]
        dx = x1 - x0
        dy = y1 - y0
        arrow_length = np.sqrt(dx**2 + dy**2)

        # Stop line short for arrowhead
        arrowhead_ratio = 1.0 - (arrowhead_size / arrow_length)
        x_line_end = x0 + dx * arrowhead_ratio
        y_line_end = y0 + dy * arrowhead_ratio

        fig.add_trace(
            go.Scatter(
                x=[x0, x_line_end],
                y=[y0, y_line_end],
                mode="lines",
                line=dict(color="rgba(50, 50, 200, 0.8)", width=2),
                showlegend=False,
            )
        )

        # Add custom arrowhead
        angle_degrees = np.degrees(np.arctan2(dy, dx))

        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        arrow_x = [
            x1,  # Tip
            x1 - arrowhead_size * cos_a + arrowhead_width * sin_a,  # Back right
            x1 - arrowhead_size * cos_a - arrowhead_width * sin_a,  # Back left
            x1,  # Back to tip to close the shape
        ]
        arrow_y = [
            y1,  # Tip
            y1 - arrowhead_size * sin_a - arrowhead_width * cos_a,  # Back right
            y1 - arrowhead_size * sin_a + arrowhead_width * cos_a,  # Back left
            y1,  # Back to tip to close the shape
        ]

        fig.add_trace(
            go.Scatter(
                x=arrow_x,
                y=arrow_y,
                fill="toself",
                fillcolor="rgba(50, 50, 200, 0.9)",
                line=dict(color="rgba(50, 50, 200, 1.0)"),
                mode="lines",
                showlegend=False,
            )
        )

    if "show_mapped_reference" in display_options:
        # Mapped X-axis reference (green)
        x0, y0, x1, y1 = plot_data["mapped_ref_arrows"][0]
        dx = x1 - x0
        dy = y1 - y0
        arrow_length = np.sqrt(dx**2 + dy**2)

        # Stop line short for arrowhead
        arrowhead_size = 0.075  # Changed from 0.15
        arrowhead_ratio = 1.0 - (arrowhead_size / arrow_length)
        x_line_end = x0 + dx * arrowhead_ratio
        y_line_end = y0 + dy * arrowhead_ratio

        fig.add_trace(
            go.Scatter(
                x=[x0, x_line_end],
                y=[y0, y_line_end],
                mode="lines",
                line=dict(color="rgba(50, 200, 50, 0.8)", width=2),
                showlegend=False,
            )
        )

        # Add custom arrowhead
        angle_degrees = np.degrees(np.arctan2(dy, dx))
        arrowhead_width = 0.055  # Changed from 0.11

        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        arrow_x = [
            x1,  # Tip
            x1 - arrowhead_size * cos_a + arrowhead_width * sin_a,  # Back right
            x1 - arrowhead_size * cos_a - arrowhead_width * sin_a,  # Back left
            x1,  # Back to tip to close the shape
        ]
        arrow_y = [
            y1,  # Tip
            y1 - arrowhead_size * sin_a - arrowhead_width * cos_a,  # Back right
            y1 - arrowhead_size * sin_a + arrowhead_width * cos_a,  # Back left
            y1,  # Back to tip to close the shape
        ]

        fig.add_trace(
            go.Scatter(
                x=arrow_x,
                y=arrow_y,
                fill="toself",
                fillcolor="rgba(50, 200, 50, 0.9)",
                line=dict(color="rgba(50, 200, 50, 1.0)"),
                mode="lines",
                showlegend=False,
            )
        )

        # Mapped Y-axis reference (blue)
        x0, y0, x1, y1 = plot_data["mapped_ref_arrows"][1]
        dx = x1 - x0
        dy = y1 - y0
        arrow_length = np.sqrt(dx**2 + dy**2)

        # Stop line short for arrowhead
        arrowhead_ratio = 1.0 - (arrowhead_size / arrow_length)
        x_line_end = x0 + dx * arrowhead_ratio
        y_line_end = y0 + dy * arrowhead_ratio

        fig.add_trace(
            go.Scatter(
                x=[x0, x_line_end],
                y=[y0, y_line_end],
                mode="lines",
                line=dict(color="rgba(50, 50, 200, 0.8)", width=2),
                showlegend=False,
            )
        )

        # Add custom arrowhead
        angle_degrees = np.degrees(np.arctan2(dy, dx))

        angle_rad = np.radians(angle_degrees)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)

        arrow_x = [
            x1,  # Tip
            x1 - arrowhead_size * cos_a + arrowhead_width * sin_a,  # Back right
            x1 - arrowhead_size * cos_a - arrowhead_width * sin_a,  # Back left
            x1,  # Back to tip to close the shape
        ]
        arrow_y = [
            y1,  # Tip
            y1 - arrowhead_size * sin_a - arrowhead_width * cos_a,  # Back right
            y1 - arrowhead_size * sin_a + arrowhead_width * cos_a,  # Back left
            y1,  # Back to tip to close the shape
        ]

        fig.add_trace(
            go.Scatter(
                x=arrow_x,
                y=arrow_y,
                fill="toself",
                fillcolor="rgba(50, 50, 200, 0.9)",
                line=dict(color="rgba(50, 50, 200, 1.0)"),
                mode="lines",
                showlegend=False,
            )
        )

    # Set up layout with cleaner appearance (no gridlines or axes)
    layout = {
        "plot_bgcolor": "#222",
        "paper_bgcolor": "#222",
        "font": {"color": "white"},
        "xaxis": {
            "showgrid": False,  # Hide gridlines
            "zeroline": True,
            "zerolinecolor": "rgba(255, 255, 255, 0.2)",  # Fainter zero line
            "zerolinewidth": 1,
            "showticklabels": False,
            "showline": False,  # Hide axis line
            "showspikes": False,  # Hide spikes
            "visible": False,  # Hide axis completely
        },
        "yaxis": {
            "showgrid": False,  # Hide gridlines
            "zeroline": True,
            "zerolinecolor": "rgba(255, 255, 255, 0.2)",  # Fainter zero line
            "zerolinewidth": 1,
            "showticklabels": False,
            "showline": False,  # Hide axis line
            "showspikes": False,  # Hide spikes
            "visible": False,  # Hide axis completely
            "scaleanchor": "x",  # Force equal scaling with x-axis
            "scaleratio": 1,  # 1:1 aspect ratio
            "constrain": "domain",  # Constrain to domain
        },
        # Use minimal margins to maximize the plotting area
        "margin": {"l": 0, "r": 0, "t": 0, "b": 0, "pad": 0},
        "autosize": True,
    }

    # Apply axis range if provided
    if axis_range:
        layout["xaxis"]["range"] = axis_range["x"]
        layout["yaxis"]["range"] = axis_range["y"]

    fig.update_layout(layout)

    return fig
