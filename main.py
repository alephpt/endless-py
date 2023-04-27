import pygame
from OpenGL.GL import glTranslatef, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, glLoadIdentity
from grid import Grid
from engine import Engine
                
def main():
    SCREEN_SIZE = (1200, 800)

    grid = Grid()
    engine = Engine(SCREEN_SIZE)

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
                pygame.mouse.set_pos(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)
                engine.prev_mouse_pos = pygame.mouse.get_pos()
                

        engine.camera.set_projection(*SCREEN_SIZE)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        engine.camera.set()
        grid.render()
        engine.update()


if __name__ == "__main__":
    main()
    pygame.quit()