import numpy as np
from OpenGL.GL import glMatrixMode, glLoadIdentity, glRotatef, glTranslatef, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective, gluLookAt
from quaternion import Quaternion


class Camera:
    def __init__(self, pos=np.array([0, 0, 0])):
        self.pos = pos
        self.rotation_quaternion = Quaternion()
        self.x_axis = Quaternion(np.array([1, 0, 0]), 0)
        self.y_axis = Quaternion(np.array([0, 1, 0]), 0)
        self.z_axis = Quaternion(np.array([0, 0, 1]), 0)

    def get_rotation_quaternion(self, pitch, yaw, roll):
        #print("Rotation Angles: ", pitch, yaw, roll)
        self.y_axis = Quaternion(np.array([0, 1, 0]), yaw)
        self.x_axis = Quaternion(np.array([1, 0, 0]), pitch)
        self.z_axis = Quaternion(np.array([0, 0, 1]), roll)
        #print("Rotation Quaternion: ", "\n", x_axis, "\n", y_axis, "\n", z_axis)
        return self.x_axis * self.y_axis * self.z_axis

    def rotate_vector_by_quaternion(self, vector, quaternion):
        vector_quaternion = Quaternion.from_rotation_vector(vector)
        return quaternion * vector_quaternion * quaternion.conjugate()

    def look(self, yaw, pitch, roll):
        pitch = np.radians(pitch)
        yaw = np.radians(yaw)
        roll = np.radians(roll)
        self.rotation_quaternion = self.get_rotation_quaternion(pitch, yaw, roll)

    def move(self, t, map_size=100):
        offset = map_size // 2
        forward = self.rotation_quaternion.to_np_array()
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
        gluLookAt(self.pos[0], self.pos[1], self.pos[2],
                    self.pos[0] + self.rotation_quaternion.x,
                    self.pos[1] + self.rotation_quaternion.y,
                    self.pos[2] + self.rotation_quaternion.z,
                    self.y_axis.x, self.y_axis.y, self.y_axis.z)
