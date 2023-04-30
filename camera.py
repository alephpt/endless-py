import numpy as np
from OpenGL.GL import glMatrixMode, glLoadIdentity, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective, gluLookAt
import math


class Camera:
    def __init__(self, pos=(0, 0, 0)):
        self.pos = np.array(pos)
        self.forward = np.array([0, 0, 1])
        self.up = np.array([0, 1, 0])
        self.right = np.array([1, 0, 0])

    # rotates the camera around the right vector
    def pitch(self, angle):
        radians = math.radians(angle)
        
        new_forward = self.forward * math.cos(radians) - self.up * math.sin(radians)
        new_up = self.up * math.cos(radians) - self.forward * math.sin(radians)
        new_right = np.cross(new_forward, new_up)
        
        self.forward = new_forward
        self.up = new_up
        self.right = new_right / np.linalg.norm(new_right)

    # rotates the camera around the up vector
    def yaw(self, angle):
        radians = math.radians(angle)
        
        new_forward = self.forward * math.cos(radians) - self.right * math.sin(radians)
        new_right = np.cross(self.forward, self.up)
        new_up = np.cross(new_right, new_forward)
        
        self.forward = new_forward
        self.right = new_right / np.linalg.norm(new_right)
        self.up = new_up / np.linalg.norm(new_up)

    # rotates the camera around the forward vector
    def roll(self, angle):
        radians = math.radians(angle)
        
        new_up = self.up * math.cos(radians) - self.right * math.sin(radians)
        new_right = self.right * math.cos(radians) + self.up * math.sin(radians)
        
        self.up = new_up
        self.right = new_right
    
    # move the camera direction based on the cursor movement
    def look(self, yaw, pitch):
        self.yaw(yaw)
        self.pitch(pitch)

    # moves the camera forward or backward based on 
    # the camera's current forward vector
    def move(self, t, map_size=100):
        offset = map_size // 2
        self.pos = self.pos + self.forward * t
        
        # check if the new position has gone out of bounds
        if self.pos[0] < -offset:
            self.pos[0] = offset
        elif self.pos[0] > offset:
            self.pos[0] = -offset
        if self.pos[1] < -offset:
            self.pos[1] = offset
        elif self.pos[1] > offset:
            self.pos[1] = -offset
        if self.pos[2] < -offset:
            self.pos[2] = offset
        elif self.pos[2] > offset:
            self.pos[2] = -offset
    
    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def set(self):
        gluLookAt(*self.pos, *(self.pos + self.forward), *self.up)