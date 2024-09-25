import numpy as np
import time

global target_faces

target_faces = 3700

def compute_qem(vertices, faces):
    qem = np.zeros((len(vertices), 4, 4))
    for face in faces:
        v0, v1, v2 = vertices[face]
        normal = np.cross(v1 - v0, v2 - v0)
        normal_length = np.linalg.norm(normal)
        if normal_length != 0:
            normal /= normal_length
        else:
            normal = np.zeros_like(normal)
        d = -np.dot(normal, v0)
        plane = np.concatenate((normal, [d]))
        qem[face] += np.outer(plane, plane)
    return qem

def calculate_error(face, qem):
    qem_sum = qem[face].sum(axis=0)
    
    # Check if the coefficient matrix is singular
    if np.linalg.det(qem_sum[:3, :3]) == 0:
        return float('inf')  # Assign a high error value for singular faces
    
    vertex = np.linalg.solve(qem_sum[:3, :3], -qem_sum[:3, 3])
    error = np.dot(np.dot(vertex, qem_sum[:3, :3]), vertex) + 2 * np.dot(qem_sum[:3, 3], vertex) + qem_sum[3, 3]
    return error

def simplify_mesh(vertices, faces, target_faces):
    start = time.time()
    qem = compute_qem(vertices, faces)
    total_iterations = len(faces) - target_faces
    completed_iterations = 0
    previous_progress = -5  # Initialize with -5 to ensure the first progress is printed

    while len(faces) > target_faces:
        # Calculate the errors for all faces
        errors = []
        for face in faces:
            error = calculate_error(face, qem)
            errors.append(error)

        # Find the face with the minimal error
        min_error_index = np.argmin(errors)
        collapse_face = faces[min_error_index]

        # Collapse the face by merging its vertices
        new_vertex = np.mean(vertices[collapse_face], axis=0)
        vertices = np.concatenate((vertices, [new_vertex]), axis=0)

        # Update the neighboring faces
        neighbor_faces = np.where(np.any(faces == collapse_face[0], axis=1) |
                                  np.any(faces == collapse_face[1], axis=1) |
                                  np.any(faces == collapse_face[2], axis=1))
        faces[neighbor_faces] = np.where(faces[neighbor_faces] == collapse_face[0], len(vertices) - 1, faces[neighbor_faces])
        faces[neighbor_faces] = np.where(faces[neighbor_faces] == collapse_face[1], len(vertices) - 1, faces[neighbor_faces])
        faces[neighbor_faces] = np.where(faces[neighbor_faces] == collapse_face[2], len(vertices) - 1, faces[neighbor_faces])

        # Remove the collapsed face
        faces = np.delete(faces, min_error_index, axis=0)

        # Update the QEM matrices
        qem = compute_qem(vertices, faces)
        
        # Print progress
        completed_iterations += 1
        progress = (completed_iterations / total_iterations) * 100
        if progress >= previous_progress + 5:  # Print progress at every 5% interval
            print(f"Progress: {int(progress)}%")
            previous_progress += 5

    end = time.time()
    duration = np.around((end - start), 3)

    print(f"Number Of Face Are: {len(faces)}  Faces ")
    print(f"Duration To Generate The Mesh are {duration} Seconds ")

    return vertices, faces
