import numpy as np
from vispy import scene
from vispy.scene.visuals import Line
from vispy.geometry.generation import create_arrow
from vispy.scene.visuals import Mesh
from vispy.color import Color
import numpy as np
from vispy.visuals.transforms import MatrixTransform
from vispy.scene import Text
from params import quadrants, grid_size, line_spacing

def init_vis(init_pos):
    canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)
    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(up='z', fov=60)

    #lines gonna be on scale of 1 km
    num_lines = grid_size//line_spacing
    spacing = grid_size / num_lines
    if quadrants == 360:
        start = -grid_size / 2
    else:
        start = 0

    # -----------------------
    # XY plane (Z = 0)
    # -----------------------
    for i in range(num_lines):
        y = start + i * spacing
        if quadrants == 360:
            x = np.array([-grid_size/2, grid_size/2])
        else:
            x = np.array([0, grid_size])
        z = np.zeros(2)



        line = Line(pos=np.column_stack([x, [y, y], z]), color='white', width=1)
        line.set_gl_state(depth_test=False)
        view.add(line)

    for i in range(num_lines):
        x = start + i * spacing
        if quadrants == 360:
            y = np.array([-grid_size/2, grid_size/2])
        else:
            y = np.array([0, grid_size])
        z = np.zeros(2)


        line = Line(pos=np.column_stack([[x, x], y, z]), color='white', width=1)
        line.set_gl_state(depth_test=False)
        view.add(line)

    # -----------------------
    # YZ plane (X = 0)
    # -----------------------
    for i in range(num_lines):
        z = start + i * spacing
        if z < 0:
            continue
        if quadrants == 360:
            y = np.array([-grid_size/2, grid_size/2])
        else:
            y = np.array([0, grid_size])


        x = np.zeros(2)

        line = Line(pos=np.column_stack([x, y, [z, z]]), color='white', width=1)
        line.set_gl_state(depth_test=False)
        view.add(line)

    for i in range(num_lines):
        y = start + i * spacing
        if quadrants == 360:
            z = np.array([0, grid_size/2])
        else:
            z = np.array([0, grid_size])
        x = np.zeros(2)

        line = Line(pos=np.column_stack([x, [y, y], z]), color='white', width=1)
        line.set_gl_state(depth_test=False)
        view.add(line)

    # -----------------------
    # XZ plane (Y = 0)
    # -----------------------
    for i in range(num_lines):
        z = start + i * spacing
        if z < 0:
            continue
        if quadrants == 360:
            x = np.array([-grid_size/2, grid_size/2])
        else:
            x = np.array([0, grid_size])
        y = np.zeros(2)

        line = Line(pos=np.column_stack([x, y, [z, z]]), color='white', width=1)
        line.set_gl_state(depth_test=False)
        view.add(line)

    for i in range(num_lines):
        x = start + i * spacing
        if quadrants == 360:
            z = np.array([0, grid_size/2])
        else:
            z = np.array([0, grid_size])
        y = np.zeros(2)

        line = Line(pos=np.column_stack([[x, x], y, z]), color='white', width=1)
        line.set_gl_state(depth_test=False)
        view.add(line)

    axis_len = grid_size / 2 if quadrants == 360 else grid_size

    if quadrants == 360:
        start_line = [-axis_len, 0, 0]
    else:
        start_line = [0, 0, 0]

    # X axis (red)
    line = Line(
        pos=np.array([start_line, [axis_len, 0, 0]]),
        color='red',
        width=4,
    )
    line.set_gl_state(depth_test=False)
    view.add(line)

    if quadrants == 360:
        start_line = [0, -axis_len, 0]
    else:
        start_line = [0, 0, 0]
    # Y axis (blue)
    line = Line(
        pos=np.array([start_line, [0, axis_len, 0]]),
        color='blue',
        width=4
    )
    line.set_gl_state(depth_test=False)
    view.add(line)

    # Z axis (green)
    line = Line(
        pos=np.array([[0, 0, 0], [0, 0, axis_len]]),
        color='green',
        width=4
    )
    line.set_gl_state(depth_test=False)
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
    col = Color(color='yellow')
    rocket_mesh = Mesh(meshdata=arrow_meshdata, color=col, shading='smooth')
    rocket_mesh.parent = view.scene

    rocket_mesh.transform = MatrixTransform()


    # def set_normalized_position(x_frac, y_frac):
    #     w, h = canvas.size
    #     return [x_frac * w, y_frac * h]

    # x_label = Text('X: 0.0', color='red', font_size=10)
    # x_label.pos = set_normalized_position(0.07, 0.05)  # pixels from bottom-left
    
    # x_label.parent = canvas.scene

    # y_label = Text('Y: 0.0', color='blue', font_size=10)
    # y_label.pos = set_normalized_position(0.07, 0.1)
    # y_label.parent = canvas.scene

    # z_label = Text('Z: 0.0', color='green', font_size=10)
    # z_label.pos = set_normalized_position(0.07, 0.15)
    # z_label.parent = canvas.scene

    # angles_label= Text('Angles: 0.0', color='yellow', font_size=10)
    # angles_label.pos = set_normalized_position(0.1, 0.25)
    # angles_label.parent = canvas.scene

    # time_label= Text('Time: 0.0', color='white', font_size=10)
    # time_label.pos = set_normalized_position(0.1, 0.4)
    # time_label.parent = canvas.scene

    return canvas, view, rocket_mesh#, [x_label, y_label, z_label, angles_label, time_label]
