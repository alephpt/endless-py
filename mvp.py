import pygame
import numpy as np
from quaternion import Quaternion
from OpenGL.GL import *
from OpenGL.GLU import *

# Define constants for the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define the vertices of the cube
vertices = np.array([
    [-1, -1, -1],
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1],
    [1, 1, 1]
])

# Define the edges of the cube
edges = np.array([
    [0, 1],
    [0, 2],
    [0, 4],
    [1, 3],
    [1, 5],
    [2, 3],
    [2, 6],
    [3, 7],
    [4, 5],
    [4, 6],
    [5, 7],
    [6, 7]
])

# Define the faces of the cube
faces = np.array([
    [0, 1, 3, 2],
    [0, 1, 5, 4],
    [0, 2, 6, 4],
    [1, 3, 7, 5],
    [2, 3, 7, 6],
    [4, 5, 7, 6]
])

# Define the colors of the faces
colors = np.array([
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 255, 0],
    [255, 0, 255],
    [0, 255, 255]
])

normals = np.array([
    [0, 0, -1],
    [0, 0, 1],
    [0, -1, 0],
    [0, 1, 0],
    [-1, 0, 0],
    [1, 0, 0]
])

# Define the initial position and orientation of the cube
position = np.array([0, 0, 0])
orientation = Quaternion.from_euler_angles(0, 0, 0)

# Initialize Pygame
pygame.init()

# Set the window size
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)

# Set up the OpenGL context
glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 50)
glMatrixMode(GL_MODELVIEW)

# Set up the OpenGL lighting
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, [0, 1, 1, 0])
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

# Set up the OpenGL material
glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1, 1, 1, 1])
glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

# Set up the OpenGL depth buffer    
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

# Set up the OpenGL backface culling
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

# set perspective, fov, near, far
fov = 45
near_clip = 0.1
far_clip = 50
aspect_ratio = WINDOW_WIDTH / WINDOW_HEIGHT

def perspective(fov, aspect_ratio, near_clip, far_clip):
    f = 1 / np.tan(fov / 2)
    return np.array([
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far_clip + near_clip) / (near_clip - far_clip), (2 * far_clip * near_clip) / (near_clip - far_clip)],
        [0, 0, -1, 0]
    ])

# set pitch, yaw and roll
pitch = 0
yaw = 0
roll = 0

# define shader
shader = glCreateProgram()

# set up model quaternion, scale matrix, translation matrix and mvp matrix location for gluniformmatrix4fv
model_quat = Quaternion.from_euler_angles(pitch, yaw, roll)
scale_matrix = np.eye(4)
translation_matrix = np.eye(4)


# Define the main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up the model view matrix
    glLoadIdentity()
    glTranslatef(*position)
    glMultMatrixf(orientation.to_rotation_matrix())

    # Draw the cube
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glColor3f(*colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Update the display
    pygame.display.flip()

    # Rotate the cube using the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        orientation *= Quaternion.from_axis_angle(np.array([0, 1, 0]), np.pi / 180)
    if keys[pygame.K_RIGHT]:
        orientation *= Quaternion.from_axis_angle(np.array([0, 1, 0]), -np.pi / 180)
    if keys[pygame.K_UP]:
        orientation *= Quaternion.from_axis_angle(np.array([1, 0, 0]), np.pi / 180)
    if keys[pygame.K_DOWN]:
        orientation *= Quaternion.from_axis_angle(np.array([1, 0, 0]), -np.pi / 180)
    
    # Move the cube using the WASD keys
    if keys[pygame.K_w]:
        position += np.array([0, 0, 0.1])
    if keys[pygame.K_s]:
        position += np.array([0, 0, -0.1])
    if keys[pygame.K_a]:
        position += np.array([-0.1, 0, 0])
    if keys[pygame.K_d]:
        position += np.array([0.1, 0, 0])
        
    
    # Clear screen and set background color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 0.5, 0.5, 1)

    # Set up model matrix
    model_matrix = model_quat.to_rotation_matrix()
    model_matrix = np.dot(model_matrix, scale_matrix)

    # Set up view matrix
    view_matrix = Quaternion.from_euler_angles(-pitch, -yaw, -roll).to_rotation_matrix()
    view_matrix = np.dot(view_matrix, translation_matrix)

    # Set up projection matrix
    projection_matrix = perspective(fov, aspect_ratio, near_clip, far_clip)

    # Set up MVP matrix and pass it to the shader program
    mvp_matrix = projection_matrix @ view_matrix @ scale_matrix @ translation_matrix

    # Set up the vertex buffer
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, vertices)

    # Set up the normal buffer
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 0, normals)

    # Draw the model
    glDrawArrays(GL_TRIANGLES, 0, len(vertices))

    # Swap buffers
    pygame.display.flip()
    pygame.time.wait(10)