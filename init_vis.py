import numpy as np
from vispy import scene
from vispy.scene.visuals import Line

def init_vis():
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

        line = Line(pos=np.column_stack([x, [y, y], z]), color='gray', width=1)
        view.add(line)

    for i in range(num_lines):
        x = start + i * spacing
        y = np.array([-grid_size/2, grid_size/2])
        z = np.zeros(2)

        line = Line(pos=np.column_stack([[x, x], y, z]), color='gray', width=1)
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

        line = Line(pos=np.column_stack([x, y, [z, z]]), color='gray', width=1)
        view.add(line)

    for i in range(num_lines):
        y = start + i * spacing
        z = np.array([0, grid_size/2])
        x = np.zeros(2)

        line = Line(pos=np.column_stack([x, [y, y], z]), color='gray', width=1)
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

        line = Line(pos=np.column_stack([x, y, [z, z]]), color='gray', width=1)
        view.add(line)

    for i in range(num_lines):
        x = start + i * spacing
        z = np.array([0, grid_size/2])
        y = np.zeros(2)

        line = Line(pos=np.column_stack([[x, x], y, z]), color='gray', width=1)
        view.add(line)

    # Ball (marker)
    ball = scene.Markers()
    ball.set_data(pos=np.array([[0, 0, 0]]), size=10)
    view.add(ball)
    return canvas, view, ball