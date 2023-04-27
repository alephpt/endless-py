import pygame
from OpenGL.GL import glTranslatef, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glLoadIdentity
from world import World
from grid import Grid
from engine import Engine

   
def main():
    map_size = 10
    engine = Engine(map_size)
    screen_size = engine.screen_size
    screen_width, screen_height = screen_size
    glTranslatef(0.0,0.0, -40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                # update the pitch and yaw of the camera based on the mouse movement
                engine.update_camera_direction(x, y)
                # reset the mouse location and update the previous mouse position
                pygame.mouse.set_pos(screen_width / 2, screen_height / 2)
                engine.prev_mouse_pos = pygame.mouse.get_pos()
                

        engine.camera.set_projection(*screen_size)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        engine.camera.set()
        engine.update()
        

if __name__ == "__main__":
    main()
    pygame.quit()