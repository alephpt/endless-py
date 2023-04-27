from grid import Grid

class World:
    def __init__(self, map_size):
        self.map_size = map_size
        self.objects = []
        
    def add_object(self, obj):
        self.objects.append(obj)
        
    def construct_map(self):
        # create main grid
        center_grid = Grid()
        self.add_object(center_grid)
        
        # create grids for all 26 neighbors
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x == 0 and y == 0 and z == 0:
                        continue
                    grid = Grid()
                    grid.move_grid((x * self.map_size, y * self.map_size, z * self.map_size))
                    self.add_object(grid)
                    
    def render(self):
        for obj in self.objects:
            obj.draw()