import trimesh
import numpy as np

def create_cylinder(radius, height, segments=64):
    """
    Create a single cylinder mesh using trimesh.
    :param radius: Radius of the cylinder.
    :param height: Height of the cylinder.
    :param segments: Number of segments around the cylinder.
    :return: Trimesh cylinder object.
    """
    return trimesh.creation.cylinder(radius=radius, height=height, sections=segments)

def arrange_cylinders_serial(rows, cols, spacing_x, spacing_y, radius, height):
    """
    Arrange cylinders in a serial grid pattern.
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param spacing_x: Spacing between cylinders in x-direction.
    :param spacing_y: Spacing between cylinders in y-direction.
    :param radius: Radius of the cylinders.
    :param height: Height of the cylinders.
    :return: Trimesh scene with serially arranged cylinders.
    """
    scene = trimesh.Scene()
    for i in range(rows):
        for j in range(cols):
            cylinder = create_cylinder(radius, height)
            cylinder.apply_translation([j * spacing_x, i * spacing_y, height / 2])
            scene.add_geometry(cylinder)
    return scene

def arrange_cylinders_staggered(rows, cols, spacing_x, spacing_y, radius, height):
    """
    Arrange cylinders in a staggered grid pattern.
    :param rows: Number of rows.
    :param cols: Number of columns.
    :param spacing_x: Spacing between cylinders in x-direction.
    :param spacing_y: Spacing between cylinders in y-direction.
    :param radius: Radius of the cylinders.
    :param height: Height of the cylinders.
    :return: Trimesh scene with staggered cylinders.
    """
    scene = trimesh.Scene()
    for i in range(rows):
        for j in range(cols):
            cylinder = create_cylinder(radius, height)
            offset_x = (spacing_x / 2) if i % 2 != 0 else 0  # Offset alternate rows
            cylinder.apply_translation([j * spacing_x + offset_x, i * spacing_y, height / 2])
            scene.add_geometry(cylinder)
    return scene

def export_to_stl(scene, filename):
    """
    Export a Trimesh scene to STL format.
    :param scene: Trimesh scene containing geometry.
    :param filename: Output STL file path.
    """
    combined_mesh = trimesh.util.concatenate(scene.dump())
    combined_mesh.export(filename)
    print(f"Exported to {filename}")

if __name__ == "__main__":
    # Parameters
    rows = 12
    cols = 12
    spacing_x = 0.06
    spacing_y = 0.06
    radius = 0.02
    height = 0.035

    # Generate serial arrangement
    serial_scene = arrange_cylinders_serial(rows, cols, spacing_x, spacing_y, radius, height)
    export_to_stl(serial_scene, "serial_cylinders.stl")

    # Generate staggered arrangement
    staggered_scene = arrange_cylinders_staggered(rows, cols, spacing_x, spacing_y, radius, height)
    export_to_stl(staggered_scene, "staggered_cylinders.stl")
