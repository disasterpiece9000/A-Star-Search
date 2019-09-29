class Node:
    def __init__(self, posX, posY, parent):
        self.posX = posX
        self.posY = posY
        self.parent = parent

        self.is_obstacle = False
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return other.posX == self.posX and other.posY == self.posY