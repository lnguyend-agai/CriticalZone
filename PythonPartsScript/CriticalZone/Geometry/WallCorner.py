from .Wall import Wall

class WallCorner():
    def __init__(self, wall_corner: Wall, wall_straight: Wall):
        self.wall_corner = wall_corner
        self.wall_straight = wall_straight
        self.angle = self.__calc_angle(wall_corner, wall_straight)


    def __calc_angle(self, wall_corner: Wall, wall_straight: Wall):
        return 0

