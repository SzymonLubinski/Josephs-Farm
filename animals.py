from pygame import Rect

from sprite import *
from constains import *
from staticbuilding import *


class Animal:
    def __init__(self, animal_type, x=None, y=None):
        self.effigy = animal_type
        self.baby = animal_type + '_baby'
        self.x = x
        self.y = y
        self.new_object = Actor(self.effigy + '_idle1', pos=(self.x, self.y))
        self.new_object.scale = 2.5
        self.new_object.status = 'idle'
        self.cannot = None
        self.borders = []
        self.timer = 0

        self.info = Actor('farm_milk_ready', pos=(x, y))
        self.info.x = self.new_object.x
        self.info.y = self.new_object.y - self.new_object.height
        self.show_info = False

        self.existence = {'water': True, 'food': True, 'milk': False, 'thread': False, 'feather': False}
        self.existential_requirements = True

    def draw(self):
        self.new_object.draw()
        if self.show_info:
            self.info.draw()

    def apply_status(self):
        if self.new_object.status == 'idle':
            self.new_object.images, self.new_object.flip_x = check_status(self.effigy, self.new_object.status)
        elif self.new_object.status == 'walk_down':
            self.if_not_idle()
            self.new_object.move_right(animals_speed)
        elif self.new_object.status == 'walk_up':
            self.if_not_idle()
            self.new_object.move_left(animals_speed)
        elif self.new_object.status == 'walk_left':
            self.if_not_idle()
            self.new_object.move_back(animals_speed)
        elif self.new_object.status == 'walk_right':
            self.if_not_idle()
            self.new_object.move_forward(animals_speed)

    def if_not_idle(self):
        self.new_object.animate()
        #   Information position update
        self.info.x = self.new_object.x
        self.info.y = self.new_object.y - self.new_object.height

    def update_borders(self):
        d1 = 2

        border_left = Rect((self.new_object.x - self.new_object.width / 2 - 2 * d1, self.new_object.y - self.new_object.height / 2), (d1, self.new_object.height))
        border_right = Rect((self.new_object.x + self.new_object.width / 2, self.new_object.y - self.new_object.height / 2), (d1, self.new_object.height))
        border_up = Rect((self.new_object.x - self.new_object.width / 2, self.new_object.y - self.new_object.height / 2 - d1), (self.new_object.width, d1))
        border_down = Rect((self.new_object.x - self.new_object.width / 2, self.new_object.y + self.new_object.height / 2), (self.new_object.width, d1))

        self.borders = [border_left, border_right, border_up, border_down]

    def update(self):
        self.update_borders()
        #   Random move
        if self.timer == 1:
            #    Where new_object Can move
            self.cannot, self.new_object.x, self.new_object.y, self.new_object.status = where_can_move(self.new_object.status, self.new_object.x, self.new_object.y)
            self.new_object.status = random_move(self.cannot)
            self.new_object.images, self.new_object.flip_x = check_status(self.effigy, self.new_object.status)
            self.cannot = None
        self.timer = random.randint(1, animals_choosing)
        self.apply_status()

        if not self.existence['food']:
            self.info.image = 'farm_nofood'
            self.existential_requirements = False
        elif not self.existence['water']:
            self.info.image = 'farm_nowater'
            self.existential_requirements = False
        elif self.existential_requirements and self.existence['milk']:
            self.info.image = 'farm_milk_ready'
            self.show_info = True
        elif self.existential_requirements and self.existence['thread']:
            self.info.image = 'farm_thread_ready'
            self.show_info = True
        elif self.existential_requirements and self.existence['feather']:
            self.info.image = 'farm_feather_ready'
            self.show_info = True
        elif self.existential_requirements and not self.existence['milk'] and not self.existence['thread'] and not self.existence['feather']:
            self.show_info = False
        else:
            self.existential_requirements = True

        if not self.existential_requirements:
            self.show_info = True

        #   Does the animal have food and water?
        if hasattr(self, 'grow_up'):
            if self.existential_requirements:
                self.grow_up += 0.005
            else:
                if self.grow_up > 0:
                    self.grow_up -= 0.005


class Chicken(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 200
        self.baby_animal = ChickenBaby
        self.new_object.images = get_sprites(1, 'chicken_idle')
        self.add_eggs = 0
        self.meat = 1
        self.reproduction_speed = 4200 * SPEED_GAME

    def update(self):
        Animal.update(self)
        if self.existential_requirements:
            add_egg = random.randint(1, 10 * SPEED_GAME)
            if add_egg == 1:
                self.add_eggs += 1


class ChickenBaby(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 100
        self.new_object.images = get_sprites(1, 'chicken_baby_idle')
        self.grow_up = 0
        self.adult = 'chicken'
        self.adult_animal = Chicken


class Cow(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 1000
        self.baby_animal = CowBaby
        self.new_object.images = get_sprites(1, 'cow_idle')
        self.meat = 5
        self.reproduction_speed = 6000 * SPEED_GAME

    def update(self):
        Animal.update(self)
        if self.existential_requirements:
            milk = random.randint(1, 15 * SPEED_GAME)
            if milk == 1:
                self.existence['milk'] = True


class CowBaby(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 500
        self.new_object.images = get_sprites(1, 'cow_baby_idle')
        self.grow_up = 0
        self.adult = 'cow'
        self.adult_animal = Cow


class Goat(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 800
        self.baby_animal = GoatBaby
        self.new_object.images = get_sprites(1, 'goat_idle')
        self.info.image = 'farm_milk_ready'
        self.meat = 2
        self.reproduction_speed = 5000 * SPEED_GAME

    def update(self):
        Animal.update(self)
        if self.existential_requirements:
            milk = random.randint(1, 22 * SPEED_GAME)
            if milk == 1:
                self.existence['milk'] = True


class GoatBaby(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 400
        self.new_object.images = get_sprites(1, 'goat_baby_idle')
        self.grow_up = 0
        self.adult = 'goat'
        self.adult_animal = Goat


class Pig(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 700
        self.baby_animal = PigBaby
        self.new_object.images = get_sprites(1, 'pig_idle')
        self.meat = 5
        self.reproduction_speed = 4000 * SPEED_GAME


class PigBaby(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 350
        self.new_object.images = get_sprites(1, 'pig_baby_idle')
        self.grow_up = 0
        self.adult = 'pig'
        self.adult_animal = Pig


class Bunny(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 150
        self.baby_animal = BunnyBaby
        self.new_object.images = get_sprites(1, 'bunny_idle')
        self.meat = 1
        self.reproduction_speed = 2600 * SPEED_GAME


class BunnyBaby(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 75
        self.new_object.images = get_sprites(1, 'bunny_baby_idle')
        self.grow_up = 0
        self.adult = 'bunny'
        self.adult_animal = Bunny


class Sheep(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 800
        self.baby_animal = SheepBaby
        self.new_object.images = get_sprites(1, 'sheep_idle')
        self.meat = 2
        self.reproduction_speed = 4500 * SPEED_GAME

    def update(self):
        Animal.update(self)
        if self.existential_requirements:
            thread = random.randint(1, 15 * SPEED_GAME)
            if thread == 1:
                self.existence['thread'] = True

class SheepBaby(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 400
        self.new_object.images = get_sprites(1, 'sheep_baby_idle')
        self.grow_up = 0
        self.adult = 'sheep'
        self.adult_animal = Sheep


class Turkey(Animal):
    def __init__(self, animal_type, x=None, y=None):
        super().__init__(animal_type, x, y)
        self.purchase_cost = 600
        self.new_object.images = get_sprites(1, 'turkey_idle')
        self.meat = 3

    def update(self):
        Animal.update(self)
        if self.existential_requirements:
            feather = random.randint(1, 13 * SPEED_GAME)
            if feather == 1:
                self.existence['feather'] = True

