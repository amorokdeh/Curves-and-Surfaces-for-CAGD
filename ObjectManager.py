import numpy as np
from matplotlib import style
import matplotlib.pyplot as plt
import trimesh

global vertices, vertex_colors, faces, colors
vertices = []
vertex_colors = []
faces = []
colors = []

color_mapping = {
"blue": (0, 0, 255),
"green": (0, 255, 0),
"brown": (165, 42, 42)
}

#For mesh simplification
def load_obj(file_path):
    mesh = trimesh.load_mesh(file_path)
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.faces)
    return vertices, faces

#For Perlin noise
def updateObject(triangles):
    global faces, colors
    faces = triangles
    colors = []
    for face in faces:
        _, _, zs = zip(*face)
        avg_z = sum(zs) / len(zs)
        if avg_z < 0.4:  # Water
            colors.append("blue")
        elif avg_z < 0.7:  # Grass
            colors.append("green")
        else:  # Earth
            colors.append("brown")

#For Perlin noise
def exportObject(filepath):
    # Define empty lists for vertices, vertex colors, and faces
    vertices = []
    vertex_colors = []
    triangles = []

    # Iterate over triangles
    for triangle, color in zip(faces, colors):
        # Get vertices of the triangle
        xs, ys, zs = zip(*triangle)
        triangle_vertices = list(zip(xs, ys, zs))

        # Add vertices to the vertex list
        vertices.extend(triangle_vertices)

        # Add vertex colors to the vertex color list
        vertex_colors.extend([color] * 3)

        # Generate face indices for the triangle
        num_vertices = len(vertices)
        face_indices = [num_vertices - 3, num_vertices - 2, num_vertices - 1]
        triangles.append(face_indices)
    # Convert lists to numpy arrays
    vertices = np.array(vertices)
    vertex_colors = np.array(vertex_colors)
    triangles = np.array(triangles)
    
    with open(filepath, "w") as f:
        # Write vertices
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        # Write vertex colors
        for color in vertex_colors:
            if isinstance(color, str):
                # Convert color name to RGB value
                rgb = color_mapping.get(color, (0, 0, 0))
                color_values = " ".join(str(c) for c in rgb)
            else:
                color_values = " ".join(str(c) for c in color)
            f.write(f"vc {color_values}\n")

        # Write faces
        for face in triangles:
            face_indices = " ".join(str(index + 1) for index in face)
            f.write(f"f {face_indices}\n")

    print(f"The object has been exported as '{filepath}'.obj")

#For mesh simplification
def export_obj(file_path, vertices, faces):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(file_path)

#For Perlin noise
def drawObject():
    print("Run GUI")
    style.use("seaborn-poster")  #'ggplot' , 'grayscale'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plt.axis("off")
    # ax.grid(False)

    # Plot Triangles
    ## Sahara##
    # for triangle in triangles:
    #     xs, ys, zs = zip(*triangle)
    #     ax.plot_trisurf(xs, ys, zs, cmap=terrain_cmap)

    # Colored Terrain
    for face, color in zip(faces, colors):
        xs, ys, zs = zip(*face)
        ax.plot_trisurf(xs, ys, zs, color=color)
    print("The Number Of Faces Are: " + str(len(faces)))

    ax.set_xlabel("X", fontsize=20, color="red", fontweight="bold")
    ax.set_ylabel("Y", fontsize=20, color="red", fontweight="bold")
    ax.set_zlabel("Z", fontsize=20, color="red", fontweight="bold")

    plt.show()

#For mesh simplification
def visualize_mesh(vertices, faces):
    print("Run GUI")
    style.use("seaborn-poster")  #'ggplot' , 'grayscale'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plt.axis("off")

    # Calculate average Z coordinate for each face
    avg_z = np.mean(vertices[faces], axis=1)[:, 2]

    # Assign colors based on average Z
    colors = []
    for z in avg_z:
        if z < 0.4:
            colors.append("blue")
        elif z < 0.7:
            colors.append("green")
        else:
            colors.append("brown")

    # Plot the mesh with colors
    ax.plot_trisurf(
        vertices[:, 0],
        vertices[:, 1],
        vertices[:, 2],
        triangles=faces,
        edgecolor='k'
    )
    # Set facecolors using the colors array
    ax.collections[0].set_facecolor(colors)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()