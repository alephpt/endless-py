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

    def pitch(self, angle):
        radians = math.radians(angle)
        
        new_forward = self.forward * math.cos(radians) - self.up * math.sin(radians)
        new_up = self.up * math.cos(radians) - self.forward * math.sin(radians)
        new_right = np.cross(new_forward, new_up)
        
        self.forward = new_forward
        self.up = new_up
        self.right = new_right / np.linalg.norm(new_right)

    def yaw(self, angle):
        radians = math.radians(angle)
        
        new_forward = self.forward * math.cos(radians) - self.right * math.sin(radians)
        new_right = np.cross(self.forward, self.up)
        new_up = np.cross(new_right, new_forward)
        
        self.forward = new_forward
        self.right = new_right / np.linalg.norm(new_right)
        self.up = new_up / np.linalg.norm(new_up)

    def look(self, yaw, pitch):
        self.yaw(yaw)
        self.pitch(pitch)

    # moves the camera forward or backward based on 
    # the camera's current forward vector
    def move(self, t, map_size=100):
        offset = map_size // 2
        new_pos = self.pos + self.forward * t
        
        # check if the new position has gone out of bounds
        # if the x position is less than -offset set to offset
        if new_pos[0] < -offset:
            new_pos[0] = offset
        # or if the x position is greater than offset set to -offset
        elif new_pos[0] > offset:
            new_pos[0] = -offset
        # if the y position is less than -offset set to offset
        if new_pos[1] < -offset:
            new_pos[1] = offset
        # or if the y position is greater than offset set to -offset
        elif new_pos[1] > offset:
            new_pos[1] = -offset
        # if the z position is less than -offset set to offset
        if new_pos[2] < -offset:
            new_pos[2] = offset
        # or if the z position is greater than offset set to -offset
        elif new_pos[2] > offset:
            new_pos[2] = -offset
        
        self.pos = new_pos
    
    # rolls the camera by the given angle in degrees
    # with respect to the camera's current orientation
    # positive angles roll the camera clockwise
    # updating the camera's up and right vectors
    def roll(self, angle):
        radians = math.radians(angle)
        
        new_up = self.up * math.cos(radians) - self.right * math.sin(radians)
        new_right = self.right * math.cos(radians) + self.up * math.sin(radians)
        
        self.up = new_up
        self.right = new_right
    
    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

    def set(self):
        gluLookAt(*self.pos, *(self.pos + self.forward), *self.up)