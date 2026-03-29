import numpy as np
from vispy import scene
from vispy.scene.visuals import Line
from vispy.geometry.generation import create_arrow
from vispy.scene.visuals import Mesh
from vispy.color import Color
import numpy as np
from vispy.visuals.transforms import MatrixTransform

def init_vis(init_pos):
    canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(up='z', fov=60)

    #lines gonna be on scale of 1 km
    grid_size = 100 # this is noth sides so across whole plain -50 ro 50
    num_lines = grid_size//5
    spacing = grid_size / num_lines
    start = -grid_size / 2

    # -----------------------
    # XY plane (Z = 0)
    # -----------------------
    for i in range(num_lines):
        y = start + i * spacing
        x = np.array([-grid_size/2, grid_size/2])
        z = np.zeros(2)

        line = Line(pos=np.column_stack([x, [y, y], z]), color='blue', width=1)
        view.add(line)

    for i in range(num_lines):
        x = start + i * spacing
        y = np.array([-grid_size/2, grid_size/2])
        z = np.zeros(2)

        line = Line(pos=np.column_stack([[x, x], y, z]), color='blue', width=1)
        view.add(line)

    # -----------------------
    # YZ plane (X = 0)
    # -----------------------
    for i in range(num_lines):
        z = start + i * spacing
        if z < 0:
            continue
        y = np.array([-grid_size/2, grid_size/2])
        x = np.zeros(2)

        line = Line(pos=np.column_stack([x, y, [z, z]]), color='red', width=1)
        view.add(line)

    for i in range(num_lines):
        y = start + i * spacing
        z = np.array([0, grid_size/2])
        x = np.zeros(2)

        line = Line(pos=np.column_stack([x, [y, y], z]), color='red', width=1)
        view.add(line)

    # -----------------------
    # XZ plane (Y = 0)
    # -----------------------
    for i in range(num_lines):
        z = start + i * spacing
        if z < 0:
            continue
        x = np.array([-grid_size/2, grid_size/2])
        y = np.zeros(2)

        line = Line(pos=np.column_stack([x, y, [z, z]]), color='green', width=1)
        view.add(line)

    for i in range(num_lines):
        x = start + i * spacing
        z = np.array([0, grid_size/2])
        y = np.zeros(2)

        line = Line(pos=np.column_stack([[x, x], y, z]), color='green', width=1)
        view.add(line)

    # Create a MeshData arrow
    arrow_meshdata = create_arrow(
        rows=40, cols=50,      # low resolution
        radius=.1,          # cylinder radius
        length=1,          # cylinder length
        cone_radius=.15,     # tip radius
        cone_length=.3      # tip length
    )

    # Create mesh visual from MeshData
    col = Color(color='red')
    rocket_mesh = Mesh(meshdata=arrow_meshdata, color=col, shading='smooth')
    rocket_mesh.parent = view.scene

    transform = MatrixTransform()
    rocket_mesh.transform = transform


    return canvas, view, rocket_mesh