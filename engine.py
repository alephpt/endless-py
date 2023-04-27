import pygame
from OpenGL.GLU import gluPerspective
from pygame.locals import DOUBLEBUF, OPENGL
from camera import Camera

class Engine:
    def __init__(self, screen_size):
        pygame.init()
        pygame.display.set_mode(screen_size, DOUBLEBUF|OPENGL)
        pygame.mouse.set_visible(False)
        gluPerspective(45, (screen_size[0]/screen_size[1]), 0.1, 1000.0)
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.camera = Camera()
        self.prev_mouse_pos = (0, 0)
        self.acceleration = 0
        self.yaw = 0
        self.pitch = 0
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
        
        yaw = dx / 5
        pitch = dy / 10

        # update the camera rotation based on the mouse movement
        self.camera.look(yaw, pitch)
        return

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

        # update the roll of the camera
        if key[pygame.K_a]:
            self.camera.roll(5)
            return
        if key[pygame.K_d]:
            self.camera.roll(-5)
            return
    
    # update the camera location
    def update(self):
        if key := pygame.key.get_pressed():
            # move the camera based on key presses
            self.navigate(key)

        # update the camera location based on fwd, right, up
        self.camera.move(self.acceleration)
        #self.camera.pos = self.camera.pos - self.camera.forward * self.acceleration
        self.camera.set()
        
        pygame.display.flip()
        self.clock.tick(30)
