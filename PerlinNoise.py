import numpy as np
from ObjectManager import *


# Cubic Interpolation Function
def interpolate(t, a, b):
    # This Is the Old Interpolation Function 1983

    # f = 3.0 * t**2 - 2.0 * t**3

    # This Is the Improved Interpolation Function 2002

    f = 6.0 * t**5 - 15.0 * t**4 + 10.0 * t**3
    return a + f * (b - a)


def perlin_noise(x, y, amplitude):
    x0, y0 = int(x), int(y)
    x1, y1 = x0 + 1, y0 + 1

    # Gradient Vectors
    np.random.seed(x0 * 395 + y0 + 455)
    G0 = np.random.randn(2)
    np.random.seed(x1 * 395 + y0 + 455)
    G1 = np.random.randn(2)
    np.random.seed(x0 * 395 + y1 + 455)
    G2 = np.random.randn(2)
    np.random.seed(x1 * 395 + y1 + 455)
    G3 = np.random.randn(2)

    # Distance Vectors
    S0 = np.array([x - x0, y - y0])
    S1 = np.array([x - x1, y - y0])
    S2 = np.array([x - x0, y - y1])
    S3 = np.array([x - x1, y - y1])

    # Dot Products
    dot0 = np.dot(G0, S0)
    dot1 = np.dot(G1, S1)
    dot2 = np.dot(G2, S2)
    dot3 = np.dot(G3, S3)

    # Interpolation
    i1 = interpolate(x - x0, dot0, dot1)
    i2 = interpolate(x - x0, dot2, dot3)
    interpolated_dot = interpolate(y - y0, i1, i2)

    # Generate The Final Perlin Noise Value
    perlin_noise = interpolated_dot + amplitude

    return perlin_noise


# Parameters
global meshWidth, meshHeight, freq, amplitude
meshWidth = 50  # Number Of Vertices In X Direction
meshHeight = 40  # Number Of Vertices In Y Direction
freq = 0.1  # To Controll The Frequency Of The Noise
amplitude = 0.5  # To Adjusts The Amplitude OF The Noise

def generate_terrain(meshWidth, meshHeight, freq, amplitude):
    print("Generate terrain")
    # Generate Perlin noise grid
    noise_grid = np.zeros((meshHeight, meshWidth))
    for y in range(meshHeight):
        for x in range(meshWidth):
            noise_grid[y, x] = perlin_noise(x * freq, y * freq, amplitude)

    # Generate Mesh Of Triangles
    global triangles
    triangles = []
    for y in range(meshHeight - 1):
        for x in range(meshWidth - 1):
            # Create triangles for each cell
            v1 = (x, y, noise_grid[y, x])
            v2 = (x + 1, y, noise_grid[y, x + 1])
            v3 = (x, y + 1, noise_grid[y + 1, x])
            v4 = (x + 1, y + 1, noise_grid[y + 1, x + 1])

            # Mesh As Squares
            # triangles.append([v1, v2, v3, v4])

            ## To Generate A Mesh As Triagles ##

            # List Triangle 1
            triangles.append([v1, v2, v3])

            # List Triangle 2
            triangles.append([v2, v4, v3])

# Visualization
def runPerlinNoise():
    updateObject(triangles)
    exportObject("terrain.obj")
    drawObject()