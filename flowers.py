from sprite import *


class Flowers:
    def __init__(self, flower_type, x=None, y=None):
        self.x = x
        self.y = y
        self.effigy = flower_type
        self.new_object = Actor(self.effigy + '4', pos=(self.x, self.y))
        self.new_object.scale = 2

    def draw(self):
        self.new_object.draw()

    def update(self):
        if self.new_object.image == self.effigy + '4':
            self.time_now = None
            self.time_start = None
            self.ripe = True
        else:
            self.time_now = time.time()
            if self.time_start + self.speed_growing < self.time_now:  # SET TIME PERIOD
                self.new_object.next_image()
                self.time_start = time.time()


class BlackRose(Flowers):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(4, 'flower_black_rose')
        self.purchase_cost = 25
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(1, 2)
        self.speed_growing = random.randint(0.6 * SPEED_GAME, 0.7 * SPEED_GAME)
        self.plants_ad = 'ad_black_rose'

    def update(self):
        Flowers.update(self)


class Daisy(Flowers):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(4, 'flower_daisy')
        self.purchase_cost = 25
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(10, 15)
        self.speed_growing = random.randint(0.2 * SPEED_GAME, 0.3 * SPEED_GAME)
        self.plants_ad = 'ad_daisy'

    def update(self):
        Flowers.update(self)


class Lily(Flowers):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(4, 'flower_lily')
        self.purchase_cost = 25
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(4, 9)
        self.speed_growing = random.randint(0.3 * SPEED_GAME, 0.4 * SPEED_GAME)
        self.plants_ad = 'ad_lily'

    def update(self):
        Flowers.update(self)


class RedRose(Flowers):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(4, 'flower_red_rose')
        self.purchase_cost = 25
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(1, 2)
        self.speed_growing = random.randint(0.7 * SPEED_GAME, 0.8 * SPEED_GAME)
        self.plants_ad = 'ad_red_rose'

    def update(self):
        Flowers.update(self)


class Tulip(Flowers):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(4, 'flower_tulip')
        self.purchase_cost = 25
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(4, 6)
        self.speed_growing = random.randint(0.3 * SPEED_GAME, 0.4 * SPEED_GAME)
        self.plants_ad = 'ad_tulip'

    def update(self):
        Flowers.update(self)


class Geraniums(Flowers):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(4, 'flower_geraniums')
        self.purchase_cost = 25
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(1, 9)
        self.speed_growing = random.randint(0.2 * SPEED_GAME, 0.4 * SPEED_GAME)
        self.plants_ad = 'ad_geraniums'

    def update(self):
        Flowers.update(self)
