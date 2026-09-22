

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="3D Cartesian coordinate plotter",
    page_icon="📍",
    layout="wide",
)


EXAMPLE_DATA = """Item,Dimension 1,Dimension 2,Dimension 3
Apple,1.20,0.80,0.25
Banana,1.05,1.10,0.10
Orange,0.80,0.95,0.35
Cat,-0.20,-1.10,0.80
Dog,-0.35,-0.90,1.10
Rabbit,-0.05,-1.25,0.95
Car,-1.10,0.40,-0.85
Bus,-0.90,0.65,-1.05
Bicycle,-1.25,0.20,-0.70
"""


def read_csv(uploaded_file):
    """Read a CSV, including files saved with a common Windows encoding."""
    try:
        return pd.read_csv(uploaded_file)
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="cp1252")


st.title("3D Cartesian coordinate plotter")

st.write(
    """
    Upload coordinates from a three-dimensional solution to create an
    interactive plot. You can rotate the graph by dragging it, zoom with the
    mouse wheel, and hover over a point to inspect its coordinates.
    """
)

with st.expander("Required CSV format", expanded=True):
    st.markdown(
        """
        The first four columns of the CSV file must contain:

        1. the item label;
        2. the X coordinate (Dimension 1);
        3. the Y coordinate (Dimension 2);
        4. the Z coordinate (Dimension 3).

        The coordinate columns must contain numbers and must not contain blank
        cells. Column headings can have any names because columns are selected
        according to their position.
        """
    )
    st.download_button(
        "Download example coordinate CSV",
        data=EXAMPLE_DATA,
        file_name="example_3d_coordinates.csv",
        mime="text/csv",
    )


uploaded_file = st.file_uploader(
    "Upload a CSV file containing 3D coordinates",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        data = read_csv(uploaded_file)
    except Exception as error:
        st.error(f"The CSV file could not be read: {error}")
    else:
        if data.shape[1] < 4:
            st.error(
                "The file must contain at least four columns: an item label "
                "followed by X, Y and Z coordinates."
            )
        elif data.empty:
            st.error("The file does not contain any data rows.")
        else:
            plot_data = data.iloc[:, :4].copy()
            plot_data.columns = ["Item", "X", "Y", "Z"]

            for coordinate in ["X", "Y", "Z"]:
                plot_data[coordinate] = pd.to_numeric(
                    plot_data[coordinate], errors="coerce"
                )

            missing_coordinates = plot_data[["X", "Y", "Z"]].isna()

            if missing_coordinates.any().any():
                problem_rows = (missing_coordinates.any(axis=1)).sum()
                st.error(
                    f"The file contains non-numeric or blank coordinates in "
                    f"{problem_rows} row(s). Please correct these values and "
                    "upload the file again."
                )
            elif plot_data["Item"].isna().any():
                st.error("Every row must have an item label in the first column.")
            else:
                plot_data["Item"] = plot_data["Item"].astype(str)

                st.subheader("Uploaded coordinates")
                st.dataframe(plot_data, use_container_width=True, hide_index=True)

                show_labels = st.checkbox(
                    "Show labels beside every point",
                    value=True,
                )

                figure = px.scatter_3d(
                    plot_data,
                    x="X",
                    y="Y",
                    z="Z",
                    text="Item" if show_labels else None,
                    color="Z",
                    color_continuous_scale="RdBu_r",
                    hover_name="Item",
                    title="Three-dimensional coordinate plot",
                )

                figure.update_traces(
                    marker={"size": 6, "opacity": 0.9},
                    textposition="top center",
                )
                figure.update_layout(
                    scene={
                        "xaxis_title": "Dimension 1",
                        "yaxis_title": "Dimension 2",
                        "zaxis_title": "Dimension 3",
                        "aspectmode": "cube",
                    },
                    coloraxis_colorbar={"title": "Dimension 3"},
                    margin={"l": 0, "r": 0, "b": 0, "t": 50},
                )

                st.plotly_chart(
                    figure,
                    use_container_width=True,
                    config={
                        "displaylogo": False,
                        "toImageButtonOptions": {
                            "format": "png",
                            "filename": "3d_coordinate_plot",
                            "scale": 2,
                        },
                    },
                )

                st.caption(
                    "Drag to rotate. Use the mouse wheel to zoom. The camera "
                    "button above the graph downloads an image."
                )


st.divider()
st.caption("Original program by Michael Pilling (2024). Browser version, 2026.")

