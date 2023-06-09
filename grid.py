from OpenGL.GL import glBegin, glEnd, glColor3f, glVertex3fv, GL_LINES

square = (
    (1, 0, 0),
    (1, 0, 0),
    (-1, 0, 0),
    (-1, -0, 0)
    )

edges = (
    (0,1),
    (0,3),
    (2,1),
    (2,3),
    )


class Grid:
    def __init__(self):
        self.grid = []
        self.edges = []
        self.grid_sq = 10
        self.create_grid()
    
    def create_grid(self):
        for j in range(self.grid_sq + 1):
            for i in range(self.grid_sq + 1):
                x = i - self.grid_sq // 2
                z = j - self.grid_sq // 2
                self.grid.append((x, 0, z))

        verticals = []
        for j in range(self.grid_sq + 1):
            for i in range(self.grid_sq):
                verticals.append((j * (self.grid_sq + 1) + i, j * (self.grid_sq + 1) + i + 1))
        
        horizontals = []
        for j in range(self.grid_sq):
            for i in range(self.grid_sq + 1):
                horizontals.append((j * (self.grid_sq + 1) + i, (j + 1) * (self.grid_sq + 1) + i))
        
        # zip up verticals and horitzontals interlaced
        self.edges = [val for pair in zip(verticals, horizontals) for val in pair]
                
    def move_grid(self, offset):
        for i in range(len(self.grid)):
            self.grid[i] = (self.grid[i][0] + offset[0], self.grid[i][1] + offset[1], self.grid[i][2] + offset[2])

    def draw(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.grid[vertex])
                vert = edge[0]
                glColor3f(0.75 - (vert + 1) / (self.grid_sq ** 2) * 0.5, \
                        0.25 + (vert + 1) / (self.grid_sq ** 2) * 0.25, \
                        0.25 + (vert + 1) / (self.grid_sq ** 2 * 0.5))
        glEnd()