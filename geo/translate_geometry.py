import numpy as np
import trimesh

# Translate in x,y,z
translation = [0.06,0.08,-0.002]

# Serial 
mesh = trimesh.load('shrinkwrap/serial.obj')
mesh.vertices += translation
mesh.export('cylinder_serial.obj',include_normals=True)

# Staggered
mesh = trimesh.load('shrinkwrap/staggered.obj')
mesh.vertices += translation
mesh.export('cylinder_staggered.obj',include_normals=True)