import numpy as np
from OpenGL.GL import glMatrixMode, glLoadIdentity, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective, gluLookAt
import math


class Camera:
    def __init__(self, pos=(0, 0, 0)):
        self.pos = np.array(pos)
        self.pitch = 0
        self.yaw = 0
        self.forward = np.array([0, 0, 1])
        self.up = np.array([0, 1, 0])
        self.right = np.array([1, 0, 0])

    # makes sure that all the vectors are orthogonal
    def update_vectors(self):
        # Calculate the new forward vector based on the current yaw and pitch
        forward = np.array([
            math.sin(self.yaw) * math.cos(self.pitch),
            math.sin(self.pitch),
            math.cos(self.yaw) * math.cos(self.pitch)
        ])
        self.forward = forward / np.linalg.norm(forward)

        # Calculate the new right and up vectors
        self.right = np.cross(self.forward, np.array([0, 1, 0]))
        self.right /= np.linalg.norm(self.right)
        self.up = np.cross(self.right, self.forward)

    def look(self, p, y):
        # Convert the angles to radians
        self.yaw = math.radians(y)
        self.pitch = math.radians(p)

    # moves the camera forward or backward based on 
    # the camera's current forward vector
    def move(self, t):
        #print("moving forward at speed: ", t)
        self.pos = self.pos + self.forward * t
    
    # rolls the camera by the given angle in degrees
    # with respect to the camera's current orientation
    # positive angles roll the camera clockwise
    # updating the camera's up and right vectors
    def roll(self, angle):
        # Convert the angle from degrees to radians
        angle = math.radians(angle)
        # Create a rotation matrix for the roll
        roll_rot = np.array([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ])
        # Apply the rotation to the up and right vectors
        self.up = np.dot(roll_rot, self.up)
        self.right = np.dot(roll_rot, self.right)
        self.update_vectors()
         
    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def set(self):
        gluLookAt(*self.pos, *(self.pos + self.forward), *self.up)