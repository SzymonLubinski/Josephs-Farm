from sprite import *


class Feeders:
    def __init__(self, feeder_type, x=None, y=None):
        self.x = x
        self.y = y
        self.effigy = feeder_type
        self.new_object = Actor(self.effigy, pos=(self.x, self.y))
        self.new_object.scale = 2

        self.info = Actor('farm_eggs_ready', pos=(x, y - self.new_object.height))

    def update(self):
        if self.is_full:
            self.new_object.image = self.full_image
        else:
            self.new_object.image = self.empty_image

    def draw(self):
        self.new_object.draw()
        if self.new_object.image == 'farm_hen_nest4':
            self.info.draw()


class VerticalCrib(Feeders):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 100
        self.is_full = False
        self.time_end = None
        self.full_image = 'farm_vertical_crib_full'
        self.empty_image = 'farm_vertical_crib_empty'

    def update(self):
        Feeders.update(self)


class HorizontalCrib(Feeders):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 100
        self.is_full = False
        self.time_end = None
        self.full_image = 'farm_horizontal_crib_full'
        self.empty_image = 'farm_horizontal_crib_empty'

    def update(self):
        Feeders.update(self)


class HenNest(Feeders):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 200
        self.is_full = False
        self.eggs = 0
        self.full_image = 'farm_hen_nest1'
        self.empty_image = 'farm_hen_nest4'

    def update(self):
        Feeders.update(self)

        if self.eggs == 0:
            self.new_object.image = 'farm_hen_nest1'
            self.is_full = False
        if self.eggs == 1:
            self.new_object.image = 'farm_hen_nest2'
            self.is_full = False
        if self.eggs == 2:
            self.new_object.image = 'farm_hen_nest3'
            self.is_full = False
        if self.eggs == 3:
            self.new_object.image = 'farm_hen_nest4'
            self.is_full = True


class Pasturge(Feeders):
    def __init__(self, building_type, x=None, y=None):
        super().__init__(building_type, x, y)
        self.purchase_cost = 100
        self.is_full = False
        self.time_end = None
        self.full_image = 'farm_pasturge_full'
        self.empty_image = 'farm_pasturge_empty'

    def update(self):
        Feeders.update(self)


