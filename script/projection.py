import numpy as np
import math
from coppeliasim_zmqremoteapi_client import RemoteAPIClient


def projection_calculation(sensor_handle, object_handle):
    # Get the position of the object relative to the camera
    object_pose = sim.getObjectPosition(object_handle, sensor_handle)

    # Convert the pose to a numpy array
    object_pose = np.array(object_pose)
    
    # Camera sensor resolution
    res_sensor_x = 640
    res_sensor_y = 640

    # Calculate focal length using the perspective angle value
    f = (res_sensor_x / (2 * math.tan(40)))  # f = Rx / (2 * tan(perspective angle / 2))

    # Project 3D coordinates to 2D
    x_img = f * (-object_pose[0] / object_pose[2])
    y_img = f * (-object_pose[1] / object_pose[2])

    # Convert to pixel coordinates
    x_pixel = res_sensor_x / 2 + x_img
    y_pixel = res_sensor_y / 2 - y_img

    return x_pixel, y_pixel

client = RemoteAPIClient()
sim = client.require('sim')
sim.startSimulation()


while (t := sim.getSimulationTime()) < 100000:

    vision = sim.getObjectHandle('/Vision_sensor')
    p3dx = sim.getObjectHandle('/PioneerP3DX')

    print(projection_calculation(vision, p3dx))

sim.stopSimulation()