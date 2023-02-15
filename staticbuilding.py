from pgzhelper import *


class Fences:
    def __init__(self, species, x, y):
        self.x = x
        self.y = y
        self.effigy = species
        self.new_object = Actor(self.effigy, pos=(self.x, self.y))
        self.new_object.scale = 3

    def draw(self, screen):
        self.new_object.draw()

    def update(self):
        pass


class VerticalBrightWoodenFence(Fences):
    def __init__(self, x, y, species):
        super().__init__(x, y, species)
        self.purchase_cost = 50


class HorizontalBrightWoodenFence(Fences):
    def __init__(self, x, y, species):
        super().__init__(x, y, species)
        self.purchase_cost = 50


class BrightWoodenWicket(Fences):
    def __init__(self, x, y, species):
        super().__init__(x, y, species)
        self.purchase_cost = 100


class BrightWoodenPile(Fences):
    def __init__(self, x, y, species):
        super().__init__(x, y, species)
        self.purchase_cost = 25
