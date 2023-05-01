import numpy as np
from OpenGL.GL import glMatrixMode, glLoadIdentity, glRotatef, glTranslatef, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective, gluLookAt
from pyquaternion import Quaternion


class Camera:
    def __init__(self, pos=np.array([0, 0, 0])):
        self.pos = pos
        self.rotation_quaternion = Quaternion()

    def get_rotation_quaternion(self, pitch, yaw, roll):
        x_axis = Quaternion(1, 0, 0, pitch)
        y_axis = Quaternion(0, 1, 0, yaw)
        z_axis = Quaternion(0, 0, 1, roll)
        return x_axis * y_axis * z_axis

    def rotate_vector_by_quaternion(self, vector, quaternion):
        vector_quaternion = Quaternion(0, *vector)
        return quaternion * vector_quaternion * quaternion.conjugate

    def look(self, yaw, pitch, roll):
        self.rotation_quaternion = self.get_rotation_quaternion(pitch, yaw, roll)

    def move(self, t, map_size=100):
        offset = map_size // 2
        forward = self.rotate_vector_by_quaternion(np.array([0, 0, 1]), self.rotation_quaternion)
        new_pos = self.pos + forward * t
        new_pos = np.clip(new_pos, -offset, offset)
        self.pos = new_pos
        if self.pos[0] <= -offset or self.pos[0] >= offset or self.pos[1] <= -offset or self.pos[1] >= offset:
            forward_xy = forward.copy()
            forward_xy[2] = 0
            forward_xy = forward_xy / np.linalg.norm(forward_xy)
            self.rotation_quaternion = Quaternion(np.array([0, 0, 1]), forward_xy)

    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        
    def set(self):
        glLoadIdentity()
        forward = self.rotate_vector_by_quaternion(np.array([0, 0, -1]), self.rotation_quaternion)
        up = self.rotate_vector_by_quaternion(np.array([0, 1, 0]), self.rotation_quaternion)
        target = self.pos + forward
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                target[0], target[1], target[2],
                up[0], up[1], up[2])
