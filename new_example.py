import pygame
from pygame.math import Vector3
from quaternion import Quaternion

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Quaternion Visual")


def get_rotation_quaternion(pitch, yaw, roll):
    x_axis = Quaternion.from_axis_angle((1, 0, 0), pitch)
    y_axis = Quaternion.from_axis_angle((0, 1, 0), yaw)
    z_axis = Quaternion.from_axis_angle((0, 0, 1), roll)
    return x_axis * y_axis * z_axis


def rotate_vector_by_quaternion(vector, quaternion):
    vector_quaternion = Quaternion.from_rotation_vector(vector)
    return (quaternion * vector_quaternion * quaternion.conjugate())


def main_loop():
    # Define initial rotation angles
    pitch, yaw, roll = 0, 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return

        # Update rotation angles based on user input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pitch -= 0.01
        if keys[pygame.K_DOWN]:
            pitch += 0.01
        if keys[pygame.K_LEFT]:
            yaw += 0.01
        if keys[pygame.K_RIGHT]:
            yaw -= 0.01
        if keys[pygame.K_z]:
            roll += 0.01
        if keys[pygame.K_x]:
            roll -= 0.01

        # Get rotation quaternion from angles
        rotation_quaternion = get_rotation_quaternion(pitch, yaw, roll)

        # Define vectors to be rotated
        vectors = [
            Vector3(0, 0, 100),
            Vector3(0, 50, 0),
            Vector3(50, 0, 0),
        ]

        # Rotate vectors by quaternion
        rotated_vectors = [rotate_vector_by_quaternion(vector, rotation_quaternion) for vector in vectors]

        # Clear screen
        screen.fill((255, 255, 255))

        # Draw rotated vectors
        for vector in rotated_vectors:
            x, y = vector.x + width/2, vector.y + height/2
            pygame.draw.rect(screen, (0, 0, 0), (x, y, width // 2, height // 2), 1)
            
        # Update screen
        pygame.display.flip()

main_loop()
