# 3D Cartesian coordinate plotter

A browser-based tool for displaying labelled points in three-dimensional Cartesian space.

The tool was designed primarily for viewing three-dimensional multidimensional scaling (MDS) solutions exported from statistical software such as SPSS. It can also display any data consisting of item labels and three numerical coordinates.

The application runs entirely through a web browser. Users do not need to install Python.

## Input format

Upload a CSV file containing at least four columns:

1. item label;
2. X coordinate (Dimension 1);
3. Y coordinate (Dimension 2);
4. Z coordinate (Dimension 3).

For example:

```text
Item,Dimension 1,Dimension 2,Dimension 3
Apple,1.20,0.80,0.25
Banana,1.05,1.10,0.10
Orange,0.80,0.95,0.35
```

The application uses the columns according to their position, so the column headings may have different names. Coordinate values must be numerical, with no blank cells.

An example coordinate file can be downloaded from within the application.

## Using the graph

After uploading a valid CSV file:

* drag the graph to rotate it;
* use the mouse wheel to zoom;
* hover over a point to see its label and coordinates;
* use the checkbox to show or hide labels beside the points;
* use the camera button above the graph to download it as a PNG image.

## MDS workflow

A suggested workflow is:

1. create a similarity or dissimilarity matrix from the raw sorting data;
2. conduct the multidimensional scaling analysis in SPSS;
3. export the three-dimensional MDS coordinates as a CSV file;
4. upload the coordinate file to this application;
5. rotate and inspect the resulting three-dimensional solution.

This application displays existing coordinates. It does not calculate an MDS solution.

## Author

Original Python plotting program written by Michael Pilling (2024).

Browser-based Streamlit version developed from the original program.
