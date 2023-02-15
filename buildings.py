from pygame import Rect
from constains import *


class Building:
    def __init__(self, building_type, x=None, y=None):
        self.x = x
        self.y = y
        self.effigy = building_type
        self.new_object = Actor(self.effigy, pos=(self.x, self.y))
        self.new_object.scale = 2

        self.magazine = Actor('magazine_house', pos=(1100, 200))
        self.show_magazine = False
        self.magazine_fields = []
        for y in range(2):
            y *= 144
            for x in range(3):
                x *= 100
                field = Rect((self.magazine.x - 138 + x, self.magazine.y - 135 + y), (80, 136))
                self.magazine_fields.append(field)

    def draw(self, screen):
        self.new_object.draw()
        if self.show_magazine:
            self.magazine.draw()
            if not isinstance(self, House):
                for i, j in enumerate(self.magazine_content.items()):  # RECTS
                    field = self.magazine_fields[i]
                    screen.draw.text(f'{j[1]}', center=(field.x + 41, field.y + 110),
                                     color=ORANGE, fontsize=22, fontname='bungee-regular')

    def magazine(self, amount, product_type):
        self.magazine_content[f'{product_type}'] += amount


class House(Building):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 50
        self.magazine_image = 'magazine_house'
        self.magazine_content = {'noname1': 0, 'noname2': 0, 'noname3': 0, 'noname4': 0, 'noname5': 0, 'noname6': 0}


class Stable(Building):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 4000
        self.magazine.image = 'magazine_stable'
        self.magazine_content = {'small_egg': 0, 'big_egg': 0, 'milk': 0, 'meat': 0, 'thread': 0, 'feather': 0}


class Shed(Building):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 750
        self.magazine.image = 'magazine_shed'
        self.magazine_content = {'pumpkin': 0, 'carrot': 0, 'strawberry': 0, 'tomato': 0, 'corn': 0, 'watermelon': 0}


class GreenHouse(Building):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 2000
        self.magazine.image = 'magazine_green_house'
        self.magazine_content = {'black_rose': 0, 'daisy': 0, 'lily': 0, 'tulip': 0, 'red_rose': 0, 'geraniums': 0}
