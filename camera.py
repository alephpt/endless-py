import numpy as np
from OpenGL.GL import glMatrixMode, glLoadIdentity, glRotatef, glTranslatef, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective, gluLookAt
from quaternion import Quaternion
import math


class Camera:
    def __init__(self, pos=(0, 0, 0)):
        self.pos = np.array(pos)
        self.rotation_quaternion = Quaternion([1.0, 0.0, 0.0], 0.0)

    def get_rotation_quaternion(self, pitch, yaw, roll):
        x_axis = Quaternion.from_axis_angle((1, 0, 0), pitch)
        y_axis = Quaternion.from_axis_angle((0, 1, 0), yaw)
        z_axis = Quaternion.from_axis_angle((0, 0, 1), roll)
        return x_axis * y_axis * z_axis

    def rotate_vector_by_quaternion(self, vector, quaternion):
        vector_quaternion = Quaternion.from_rotation_vector(vector)
        return (quaternion * vector_quaternion * quaternion.conjugate())
    
    # move the camera direction based on the cursor movement
    def look(self, yaw, pitch, roll):
        self.rotation_quaternion = self.get_rotation_quaternion(pitch, yaw, roll)

    # moves the camera forward or backward based on 
    # the camera's current forward vector
    def move(self, t, map_size=100):
        offset = map_size // 2
        # set camera position based on the quaternion
        # get forward direction from quaternion
        forward = self.rotate_vector_by_quaternion([0, 0, 1], self.rotation_quaternion).to_np_array()
        forward = forward / np.linalg.norm(forward)
        
        # move the camera in the forward direction
        new_pos = self.pos + forward * t
        
        # clamp the camera position to the valid range
        new_pos = np.clip(new_pos, -offset, offset)
        self.pos = new_pos
        
        # check if the camera has gone out of bounds on the x-y plane
        # if so, project the camera's forward vector onto the x-y plane
        # and use it as the new forward direction
        if self.pos[0] <= -offset or self.pos[0] >= offset or self.pos[1] <= -offset or self.pos[1] >= offset:
            forward_xy = forward.copy()
            forward_xy[2] = 0
            forward_xy = forward_xy / np.linalg.norm(forward_xy)
            self.rotation_quaternion = Quaternion.from_rotation_vectors([0, 0, 1], forward_xy)
    
    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        
    def set(self):
        forward = self.rotate_vector_by_quaternion([0, 0, 1], self.rotation_quaternion).normalized_np_array()[:3]
        up = self.rotate_vector_by_quaternion([0, 1, 0], self.rotation_quaternion).normalized_np_array()[:3]
        gluLookAt(*self.pos, *(self.pos + forward), *up)
