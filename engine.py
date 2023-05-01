import pygame
from OpenGL.GLU import gluPerspective
from OpenGL.GL import *
from pygame.locals import DOUBLEBUF, OPENGL
from camera import Camera
from world import World

class Engine:
    def __init__(self, map_size):
        pygame.init()
        # get the full size of the screen and set the display
        self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        pygame.display.set_mode(self.screen_size, DOUBLEBUF|OPENGL)
        pygame.mouse.set_visible(False)
        gluPerspective(45, (self.screen_size[0]/self.screen_size[1]), 0.1, 1000.0)

        # set depth, culling and clipping
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)
        glEnable(GL_CLIP_DISTANCE0)

        # # set the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.screen_size[0]/self.screen_size[1], 0.1, 100)
        glMatrixMode(GL_MODELVIEW)

        self.screen_width = self.screen_size[0]
        self.screen_height = self.screen_size[1]
        self.world = World(map_size)
        self.world.construct_map()
        self.camera = Camera()
        self.map_size = map_size
        self.prev_mouse_pos = (0, 0)
        self.acceleration = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.max_acceleration = 3
        self.clock = pygame.time.Clock()

    # govern the speed of the camera
    def govern_speed(self, a):
        if a > self.max_acceleration:
            a = self.max_acceleration
            return
        elif a < -self.max_acceleration:
            a = -self.max_acceleration
            return
        self.acceleration = a

    # determine the camera's pitch and yaw based on the mouse movement
    def update_camera_direction(self, x, y):
        # determine the change in mouse position
        dx = x - self.prev_mouse_pos[0]
        dy = y - self.prev_mouse_pos[1]

        self.yaw += dx / 3
        self.pitch += dy / 6

        if self.pitch > 90:
            self.pitch = 90
        elif self.pitch < -90:
            self.pitch = -90

        if self.yaw > 360:
            self.yaw = 0
        elif self.yaw < -360:
            self.yaw = 0



    # move the camera based on key presses
    def navigate(self, key):
        # update the acceleration of the camera
        if key[pygame.K_w]:
            self.govern_speed(self.acceleration + 0.01)
            #print("moving forward at speed: ", self.acceleration)
            return
        if key[pygame.K_s]:
            #print("moving forward at speed: ", self.acceleration)
            self.govern_speed(self.acceleration - 0.01)
            return

        # TODO: fix the roll so that it doesn't go past 360 degrees or -360 degrees
        # update the roll of the camera
        if key[pygame.K_a]:
            self.roll += 1
            return
        if key[pygame.K_d]:
            self.roll -= 1
            return

    # update the camera location
    def update(self):
        # move the camera based on key presses
        if key := pygame.key.get_pressed():
            self.navigate(key)

        print("yaw: ", self.yaw, " pitch: ", self.pitch, " roll: ", self.roll)
        # update the pitch, yaw and roll of the camera
        self.camera.look(self.yaw, self.pitch, self.roll)

        # update the camera location based on fwd, right, up
        self.camera.move(self.acceleration, self.map_size)

        # update the cameras direction in opengl
        self.camera.set()

        # render the world
        self.world.render()

        # update the display and tick the clock
        pygame.display.flip()
        self.clock.tick(15)
