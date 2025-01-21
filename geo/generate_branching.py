import trimesh
import numpy as np


def load_and_rescale_stl(file_path, bbox_min, bbox_max):
    """
    Load an STL file and rescale it to fit within a user-defined bounding box.
    :param file_path: Path to the STL file.
    :param bbox_min: Tuple (xmin, ymin, zmin) defining the minimum coordinates of the bounding box.
    :param bbox_max: Tuple (xmax, ymax, zmax) defining the maximum coordinates of the bounding box.
    :return: Rescaled trimesh object.
    """
    # Load the STL file
    mesh = trimesh.load(file_path)

    # Compute the current bounding box of the mesh
    mesh_bounds_min = mesh.bounds[0]
    mesh_bounds_max = mesh.bounds[1]

    # Scale factors for each dimension
    scale_factors = [
        (bbox_max[i] - bbox_min[i]) / (mesh_bounds_max[i] - mesh_bounds_min[i])
        for i in range(3)
    ]
    scale_factor = min(scale_factors)  # Uniform scaling to maintain proportions

    # Apply scaling
    mesh.apply_scale(scale_factor)

    # Recompute bounds after scaling
    new_bounds_min = mesh.bounds[0]
    new_bounds_max = mesh.bounds[1]

    # Compute translation to align with the desired bounding box
    translation = [
        (bbox_min[i] + bbox_max[i]) / 2 - (new_bounds_min[i] + new_bounds_max[i]) / 2
        for i in range(3)
    ]
    mesh.apply_translation(translation)

    return mesh


def arrange_mesh_serial(mesh, rows, cols, spacing_x, spacing_y):
    """
    Arrange the mesh in a serial grid pattern.
    :param mesh: Trimesh object to be arranged.
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param spacing_x: Spacing between meshes in the x-direction.
    :param spacing_y: Spacing between meshes in the y-direction.
    :return: Trimesh scene with serially arranged meshes.
    """
    scene = trimesh.Scene()
    for i in range(rows):
        for j in range(cols):
            print(f"Generating row {i} | column {j} ...")
            instance = mesh.copy()
            instance.apply_translation([j * spacing_x, i * spacing_y, 0])
            scene.add_geometry(instance)
    return scene


def arrange_mesh_staggered(mesh, rows, cols, spacing_x, spacing_y):
    """
    Arrange the mesh in a staggered grid pattern.
    :param mesh: Trimesh object to be arranged.
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param spacing_x: Spacing between meshes in the x-direction.
    :param spacing_y: Spacing between meshes in the y-direction.
    :return: Trimesh scene with staggered meshes.
    """
    scene = trimesh.Scene()
    for i in range(rows):
        for j in range(cols):
            print(f"Generating row {i} | column {j} ...")
            instance = mesh.copy()
            offset_y = (spacing_y / 2) if j % 2 != 0 else 0  # Offset alternate rows
            instance.apply_translation([j * spacing_x, i * spacing_y + offset_y, 0])
            scene.add_geometry(instance)
    return scene


def export_to_stl(scene, filename):
    """
    Export a Trimesh scene to STL format.
    :param scene: Trimesh scene containing geometry.
    :param filename: Output STL file path.
    """
    combined_mesh = trimesh.util.concatenate(scene.dump())
    combined_mesh.export(filename,include_normals=True)
    print(f"Exported to {filename}")


if __name__ == "__main__":
    # User-defined parameters
    input_stl = "obj/Madrepora_Formosa_wrap400.obj"  	# Path to input STL file
    bbox_min = (0.0, 0.0, -0.002)       # Bounding box minimum (xmin, ymin, zmin)
    bbox_max = (0.04, 0.04, 0.035)      # Bounding box maximum (xmax, ymax, zmax)
    rows = 12                      # Number of rows in the grid
    cols = 12                      # Number of columns in the grid
    spacing_x = 0.06               # Spacing in x-direction
    spacing_y = 0.06               # Spacing in y-direction

    # Load and rescale the mesh
    rescaled_mesh = load_and_rescale_stl(input_stl, bbox_min, bbox_max)

    # Generate serial arrangement
    serial_scene = arrange_mesh_serial(rescaled_mesh, rows, cols, spacing_x, spacing_y)
    export_to_stl(serial_scene, "branching_serial.obj")

    # Generate staggered arrangement
    staggered_scene = arrange_mesh_staggered(rescaled_mesh, rows, cols, spacing_x, spacing_y)
    export_to_stl(staggered_scene, "branching_staggered.obj")