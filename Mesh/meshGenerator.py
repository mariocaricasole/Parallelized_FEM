import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from shapely.geometry import Point, Polygon
import sys

if __name__ == "__main__":
    # import vertices defining the contour of the figure and build polyshape area
    if(len(sys.argv) < 2):
        print("Filename needed")
        sys.exit()

    N = int(input("Enter number of grid points: "))
    filename = sys.argv[1]
    vertices = np.loadtxt(filename, unpack=True).T
    polygon = Polygon(vertices)
    boundary = polygon.boundary

    # Generate a grid of points within the bounding box of the polygon
    min_x, min_y, max_x, max_y = polygon.bounds
    x = np.linspace(min_x, max_x, N)
    y = np.linspace(min_y, max_y, N)
    xx, yy = np.meshgrid(x, y)
    grid_points = np.vstack((xx.ravel(), yy.ravel())).T

    # Filter points to keep only those inside the polygon
    inside_points = np.array([point for point in grid_points if (polygon.contains(Point(point)) or boundary.contains(Point(point)))])

    # Combine the boundary vertices and interior points
    all_points = np.vstack((vertices, inside_points))

    # Perform Delaunay triangulation
    tri = Delaunay(all_points)

    # Plot the results
    plt.triplot(all_points[:, 0], all_points[:, 1], tri.simplices)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
