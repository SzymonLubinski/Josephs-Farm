from sprite import *


class Plants:
    def __init__(self, plant_type, x=None, y=None):
        self.x = x
        self.y = y
        self.effigy = plant_type
        self.new_object = Actor(self.effigy + '5', pos=(self.x, self.y))
        self.new_object.scale = 2

    def draw(self):
        self.new_object.draw()

    def update(self):
        if self.new_object.image == self.effigy + '5':
            self.time_now = None
            self.time_start = None
            self.ripe = True
        else:
            self.time_now = time.time()
            if self.time_start + self.speed_growing < self.time_now:  # SET TIME PERIOD
                self.new_object.next_image()
                self.time_start = time.time()


class Pumpkin(Plants):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(5, 'plants_pumpkin')
        self.purchase_cost = 10
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(1, 2)
        self.speed_growing = random.randint(0.6 * SPEED_GAME, 0.9 * SPEED_GAME)
        self.plants_ad = 'ad_pumpkin'


class Carrot(Plants):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(5, 'plants_carrot')
        self.purchase_cost = 10
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(2, 6)
        self.speed_growing = random.randint(0.2 * SPEED_GAME, 0.5 * SPEED_GAME)
        self.plants_ad = 'ad_carrot'


class Strawberry(Plants):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(5, 'plants_strawberry')
        self.purchase_cost = 10
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(4, 6)
        self.speed_growing = random.randint(0.15 * SPEED_GAME, 0.3 * SPEED_GAME)
        self.plants_ad = 'ad_strawberry'


class Tomato(Plants):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(5, 'plants_tomato')
        self.purchase_cost = 10
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(3, 4)
        self.speed_growing = random.randint(0.3 * SPEED_GAME, 0.5 * SPEED_GAME)
        self.plants_ad = 'ad_tomato'


class Corn(Plants):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(5, 'plants_corn')
        self.purchase_cost = 10
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(10, 15)
        self.speed_growing = random.randint(0.6 * SPEED_GAME, 0.8 * SPEED_GAME)
        self.plants_ad = 'ad_corn'


class Watermelon(Plants):
    def __init__(self, plant_type, x=None, y=None):
        super().__init__(plant_type, x, y)
        self.new_object.images = get_sprites(5, 'plants_watermelon')
        self.purchase_cost = 10
        self.time_start = time.time()
        self.time_now = None
        self.ripe = False
        self.crops = random.randint(1, 3)
        self.speed_growing = random.randint(0.4 * SPEED_GAME, 0.6 * SPEED_GAME)
        self.plants_ad = 'ad_watermelon'
