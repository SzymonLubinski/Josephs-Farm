from time import time
from pygame import Color
from animals import *
from buildings import House, Stable, Shed, GreenHouse
from set_map import *
from plants import *
from feeders import VerticalCrib, HorizontalCrib, Pasturge, HenNest
from flowers import *
from announcement import CreateAd

set_map = SetMap()


class Menu:
    def __init__(self, keys=None):
        self.coins = 1500
        self.menu = Actor('inventory1', pos=(0, 0), anchor=(0, 0))
        self.menu.images = get_sprites(8, 'inventory')
        self.keys_active = {'menu_active': False, 'blocks_active': False, 'transparet_image': False,
                            'fences_menu': False, 'animal_menu': False, 'building_menu': False,
                            'feeders_menu': False, 'plants_menu': False, 'delete_menu': False,
                            'show_board': False}
        self.keys = keys
        self.small_rects = []  # small menu windows
        for h in range(2):
            h *= 93
            for x in range(9):
                first_x = 288
                width = 48
                height = 48
                x *= 15 + 48
                y = 143 + h
                menu_window = Rect((first_x + x, y), (width, height))
                self.small_rects.append(menu_window)
        self.big_rects = []     # big menu windows
        for x in range(4):
            first_x = 288
            width = 123
            height = 123
            x *= 15 + 126
            y = 159
            menu_window = Rect((first_x + x, y), (width, height))
            self.big_rects.append(menu_window)

        self.first_barrier = Rect((100, 550), (1150, 500))
        self.second_barrier = Rect((1300, 200), (650, 900))

        self.background_blocks = []  # 10x10 invisible blocks
        for x in range(COLS):
            x *= 10
            for y in range(ROWS):
                y *= 10
                block = Rect((x, y), (10, 10))
                self.background_blocks.append(block)

        self.alphaSurface = pygame.Surface((10, 10))  # RED and GREEN surface

        self.chosen_object = None
        self.transparent_object = None
        self.new_object = None

        self.draw_error = None
        self.timer = None
        self.timer2 = None

        # Announcement START
        self.items = {'ad_pumpkin': 0, 'ad_carrot': 0, 'ad_strawberry': 0,
                      'ad_tomato': 0, 'ad_corn': 0, 'ad_watermelon': 0,
                      'ad_black_rose': 0, 'ad_daisy': 0, 'ad_lily': 0,
                      'ad_tulip': 0, 'ad_red_rose': 0, 'ad_geraniums': 0,
                      'ad_big_egg': 0, 'ad_small_egg': 0, 'ad_milk': 0,
                      'ad_meat': 0, 'ad_thread': 0, 'ad_feather': 0}
        self.available_products = {}
        self.ads_board = Actor('ad_board1', pos=(670, 165))  # Board on the map
        self.ads_board.images = get_sprites(5, 'ad_board')
        self.ads_board.scale = 2.5
        self.board = Actor('ads', pos=(160, 20), anchor=('center', 'top'))  # Announcements menu
        self.board.scale = 2
        self.ads_list = []  # Announcements list
        self.new_ad_y = [330, 530, 730, 930]
        # Announcement END

        self.back_to_menugame = Actor('back_to_menu', pos=(WIDTH - 153, 150), anchor=(0, 0))

        self.animal_list = []
        self.buildings = []  # buildings and fences
        self.plants = []
        self.feeders = []

        self.language = 'pl'
        self.errors_list = []
        self.errors = open(f'texts/errors_{self.language}.txt', 'r', encoding="utf-8")
        for i in self.errors:
            self.errors_list.append(i)

        #   The number of barriers needed to write and load a save
        self.barriers = 2
        self.maps_items = []
        self.collide_rects = self.collision_initiation()  # Collide list

    def collision_initiation(self):
        collisions_list = []
        for block in self.background_blocks:
            if moveimage.get_at((block.x, block.y)) == Color(WATER):
                collisions_list.append(block)
        collisions_list.append(self.first_barrier)
        collisions_list.append(self.second_barrier)
        set_map.all_list = set_map.create_map()
        for i in set_map.all_list:
            collisions_list.append(i.structure.get_rect())
        return collisions_list


    def check_language(self):
        self.errors_list = []
        self.errors = open(f'texts/errors_{self.language}.txt', 'r', encoding="utf-8")
        for i in self.errors:
            self.errors_list.append(i)

    def load_save(self, file_to_load):
        self.animal_list = []  # clearing the page before saving
        self.buildings = []
        self.plants = []
        self.feeders = []
        self.ads_list = []
        self.maps_items = []
        self.ads_board.image = 'ad_board1'
        self.items = file_to_load[9]
        set_map.all_list = set_map.create_map()
        self.collide_rects = self.collision_initiation()
        self.coins = file_to_load[5]
        for index, data_list in enumerate(file_to_load[:4]):
            for i in data_list:
                create = eval(i['tp'])
                effigy = i['effigy']
                x = i['x']
                y = i['y']
                new = create(effigy, x, y)
                if index == 0:
                    self.buildings.append(new)
                elif index == 1:
                    self.animal_list.append(new)
                elif index == 2:
                    self.plants.append(new)
                elif index == 3:
                    self.feeders.append(new)

        if len(file_to_load[4]) > 0:
            for i in file_to_load[4]:
                createo = eval(i['tp'])
                x_o = i['x']
                y_o = i['y']
                new_o = createo(x_o, y_o)
                self.maps_items.append(new_o)
                self.collide_rects.remove(new_o.structure.get_rect())
                for item in set_map.all_list:
                    if item.x == x_o and item.y == y_o:
                        set_map.change_lists(item)

        for building in self.buildings:
            self.collide_rects.append(building.new_object.get_rect())
        for plant in self.plants:
            self.collide_rects.append(plant.new_object.get_rect())
        for feeder in self.feeders:
            self.collide_rects.append(feeder.new_object.get_rect())

        if file_to_load[8] == 1:
            set_map.first_barrier = []
            to_remove1 = self.collide_rects.index(self.first_barrier)
            self.collide_rects.pop(to_remove1)
        elif file_to_load[8] == 0:
            set_map.first_barrier = []
            to_remove1 = self.collide_rects.index(self.first_barrier)
            self.collide_rects.pop(to_remove1)
            set_map.second_barrier = []
            to_remove2 = self.collide_rects.index(self.second_barrier)
            self.collide_rects.pop(to_remove2)

    def draw(self, screen):
        self.timer2 = time.time()
        for i in self.buildings:
            i.draw(screen)
        set_map.draw()
        self.back_to_menugame.draw()

        if self.transparent_object is not None:
            self.transparent_object.draw()

        if self.keys_active['blocks_active']:  # RED and GREEN surface
            for block in self.collide_rects:
                self.alphaSurface = pygame.Surface((block.width, block.height))  # RED and GREEN surface
                self.alphaSurface.set_alpha(40)
                self.alphaSurface.fill(RED)
                screen.blit(self.alphaSurface, (block.x, block.y))

        if self.draw_error is not None:
            time_start = time.time()
            if self.timer + 3 > time_start:
                screen.draw.text(f'{self.draw_error}', center=(WIDTH / 2, HEIGHT - 100), color=RED, fontsize=36,
                                 fontname='bungee-regular')

        for i in self.plants:
            i.draw()

        for i in self.feeders:
            i.draw()

        screen.draw.text(f'{self.coins}', center=(WIDTH - 70, 131), color=ORANGE, fontsize=16,
                         fontname='bungee-regular', owidth=1, ocolor=PURPLE)
        for i in self.animal_list:
            i.draw()
        # Announcement START
        self.ads_board.draw()
        self.board.draw()
        if self.keys_active['show_board']:
            self.board.y = 20
            for ad in self.ads_list:  # drawing advertisements
                ad['ad'].draw()
                screen.draw.text(f'Prize: {ad["prize"]}',  # Show Prize
                                 (ad['ad'].x - ad['ad'].width / 2.1,
                                  ad['ad'].y - ad['ad'].height / 2.3), color=ORANGE,
                                 fontsize=28, fontname='bungee-regular', owidth=1, ocolor=PURPLE)
                ad['do_it'] = Actor('do_it', pos=(ad['ad'].x + ad['ad'].width / 3,
                                                  ad['ad'].y - ad['ad'].height / 2.8))  # Do it
                ad['do_it'].draw()
                for item in ad['items']:  # product drawing
                    item.draw()
                for index, amount in enumerate(ad['amount']):  # product amount drawing
                    x = ad['items'][index].x
                    y = ad['items'][index].y
                    screen.draw.text(f'{amount}', (x + 50, y - 13), color=ORANGE,
                                     fontsize=28, fontname='bungee-regular', owidth=1, ocolor=PURPLE)
        if not self.keys_active['show_board']:
            self.board.y = 850
        # Announcement END

        if self.keys_active['menu_active']:
            self.menu.draw()

    def on_mouse_down(self, pos):

        def rects(big_or_small, menu_active, position):
            for rect in big_or_small:
                if rect.collidepoint(position):
                    self.chosen_object = rect
                    self.keys_active[menu_active] = True

        def choose_object():
            self.chosen_object = None
            if self.menu.image == 'inventory1':
                rects(self.big_rects, 'fences_menu', pos)
            if self.menu.image == 'inventory2':
                rects(self.big_rects, 'building_menu', pos)
            if self.menu.image == 'inventory3':
                rects(self.big_rects, 'feeders_menu', pos)
            if self.menu.image == 'inventory4':
                rects(self.small_rects, 'animal_menu', pos)
            if self.menu.image == 'inventory5':
                rects(self.small_rects, 'plants_menu', pos)
            if self.menu.image == 'inventory8':
                rects(self.big_rects, 'delete_menu', pos)

            if self.chosen_object is not None:
                self.keys_active['menu_active'] = False
                self.keys_active['blocks_active'] = True
                self.keys_active['transparet_image'] = True
                choose_new_object()

        def choose_new_object():
            self.new_object = None
            self.transparent_object = None
            if self.keys_active['animal_menu']:
                if self.small_rects.index(self.chosen_object) == 0:
                    self.transparent_object = Actor('chicken_transparent')
                elif self.small_rects.index(self.chosen_object) == 1:
                    self.transparent_object = Actor('cow_transparent')
                elif self.small_rects.index(self.chosen_object) == 2:
                    self.transparent_object = Actor('goat_transparent')
                elif self.small_rects.index(self.chosen_object) == 3:
                    self.transparent_object = Actor('pig_transparent')
                elif self.small_rects.index(self.chosen_object) == 4:
                    self.transparent_object = Actor('bunny_transparent')
                elif self.small_rects.index(self.chosen_object) == 5:
                    self.transparent_object = Actor('sheep_transparent')
                elif self.small_rects.index(self.chosen_object) == 6:
                    self.transparent_object = Actor('turkey_transparent')
                elif self.small_rects.index(self.chosen_object) == 9:
                    self.transparent_object = Actor('chicken_baby_transparent')
                elif self.small_rects.index(self.chosen_object) == 10:
                    self.transparent_object = Actor('cow_baby_transparent')
                elif self.small_rects.index(self.chosen_object) == 11:
                    self.transparent_object = Actor('goat_baby_transparent')
                elif self.small_rects.index(self.chosen_object) == 12:
                    self.transparent_object = Actor('pig_baby_transparent')
                elif self.small_rects.index(self.chosen_object) == 13:
                    self.transparent_object = Actor('bunny_baby_transparent')
                elif self.small_rects.index(self.chosen_object) == 14:
                    self.transparent_object = Actor('sheep_baby_transparent')
            elif self.keys_active['fences_menu']:
                if self.big_rects.index(self.chosen_object) == 0:
                    self.transparent_object = Actor('bhwf_transparent')
                elif self.big_rects.index(self.chosen_object) == 1:
                    self.transparent_object = Actor('bvwf_transparent')
                elif self.big_rects.index(self.chosen_object) == 2:
                    self.transparent_object = Actor('bright_wooden_wicket_transparent')
                elif self.big_rects.index(self.chosen_object) == 3:
                    self.transparent_object = Actor('bright_wooden_pile_transparent')
            elif self.keys_active['building_menu']:
                if self.big_rects.index(self.chosen_object) == 0:
                    self.transparent_object = Actor('house_transparent')
                elif self.big_rects.index(self.chosen_object) == 1:
                    self.transparent_object = Actor('stable_transparent')
                elif self.big_rects.index(self.chosen_object) == 2:
                    self.transparent_object = Actor('shed_transparent')
                elif self.big_rects.index(self.chosen_object) == 3:
                    self.transparent_object = Actor('green_house_transparent')
            elif self.keys_active['plants_menu']:
                if self.small_rects.index(self.chosen_object) == 0:
                    self.transparent_object = Actor('plants_pumpkin_transparent')
                elif self.small_rects.index(self.chosen_object) == 1:
                    self.transparent_object = Actor('plants_carrot_transparent')
                elif self.small_rects.index(self.chosen_object) == 2:
                    self.transparent_object = Actor('plants_strawberry_transparent')
                elif self.small_rects.index(self.chosen_object) == 3:
                    self.transparent_object = Actor('plants_tomato_transparent')
                elif self.small_rects.index(self.chosen_object) == 4:
                    self.transparent_object = Actor('plants_corn_transparent')
                elif self.small_rects.index(self.chosen_object) == 5:
                    self.transparent_object = Actor('plants_watermelon_transparent')
                elif self.small_rects.index(self.chosen_object) == 9:
                    self.transparent_object = Actor('flower_black_rose_transparent')
                elif self.small_rects.index(self.chosen_object) == 10:
                    self.transparent_object = Actor('flower_daisy_transparent')
                elif self.small_rects.index(self.chosen_object) == 11:
                    self.transparent_object = Actor('flower_lily_transparent')
                elif self.small_rects.index(self.chosen_object) == 12:
                    self.transparent_object = Actor('flower_tulip_transparent')
                elif self.small_rects.index(self.chosen_object) == 13:
                    self.transparent_object = Actor('flower_red_rose_transparent')
                elif self.small_rects.index(self.chosen_object) == 14:
                    self.transparent_object = Actor('flower_geraniums_transparent')
            elif self.keys_active['feeders_menu']:
                if self.big_rects.index(self.chosen_object) == 0:
                    self.transparent_object = Actor('farm_vertical_crib_transparent')
                elif self.big_rects.index(self.chosen_object) == 1:
                    self.transparent_object = Actor('farm_horizontal_crib_transparent')
                elif self.big_rects.index(self.chosen_object) == 2:
                    self.transparent_object = Actor('farm_hen_nest_transparent')
                elif self.big_rects.index(self.chosen_object) == 3:
                    self.transparent_object = Actor('farm_pasturge_transparent')

        def add_fences():
            if self.big_rects.index(self.chosen_object) == 0:
                self.new_object = HorizontalBrightWoodenFence('bhwf', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 1:
                self.new_object = VerticalBrightWoodenFence('bvwf', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 2:
                self.new_object = BrightWoodenWicket('bright_wooden_wicket', pos[0], pos[1], )
            elif self.big_rects.index(self.chosen_object) == 3:
                self.new_object = BrightWoodenPile('bright_wooden_pile', pos[0], pos[1])
            can_add = self.can_add_object(self.new_object)
            if can_add:
                self.buildings.append(self.new_object)
                self.collide_rects.append(self.new_object.new_object.get_rect())
                self.coins -= self.new_object.purchase_cost

        def add_building():
            if self.big_rects.index(self.chosen_object) == 0:
                self.new_object = House('house', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 1:
                self.new_object = Stable('stable', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 2:
                self.new_object = Shed('shed', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 3:
                self.new_object = GreenHouse('green_house', pos[0], pos[1])

            can_add = self.can_add_object(self.new_object)
            if can_add and not self.required_buildings(self.new_object.__class__):
                self.buildings.append(self.new_object)
                self.collide_rects.append(self.new_object.new_object.get_rect())
                self.coins -= self.new_object.purchase_cost

        def add_feeders():
            if self.big_rects.index(self.chosen_object) == 0:
                self.new_object = VerticalCrib('farm_vertical_crib_empty', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 1:
                self.new_object = HorizontalCrib('farm_horizontal_crib_empty', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 2:
                self.new_object = HenNest('farm_hen_nest1', pos[0], pos[1])
            elif self.big_rects.index(self.chosen_object) == 3:
                self.new_object = Pasturge('farm_pasturge_empty', pos[0], pos[1])
            can_add = self.can_add_object(self.new_object)
            if can_add:
                self.feeders.append(self.new_object)
                self.collide_rects.append(self.new_object.new_object.get_rect())
                self.coins -= self.new_object.purchase_cost

        def add_animal():
            if self.small_rects.index(self.chosen_object) == 0:
                self.new_object = Chicken('chicken', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 1:
                self.new_object = Cow('cow', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 2:
                self.new_object = Goat('goat', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 3:
                self.new_object = Pig('pig', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 4:
                self.new_object = Bunny('bunny', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 5:
                self.new_object = Sheep('sheep', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 6:
                self.new_object = Turkey('turkey', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 9:
                self.new_object = ChickenBaby('chicken_baby', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 10:
                self.new_object = CowBaby('cow_baby', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 11:
                self.new_object = GoatBaby('goat_baby', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 12:
                self.new_object = PigBaby('pig_baby', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 13:
                self.new_object = BunnyBaby('bunny_baby', pos[0], pos[1])
            elif self.small_rects.index(self.chosen_object) == 14:
                self.new_object = SheepBaby('sheep_baby', pos[0], pos[1])

            can_add = self.can_add_object(self.new_object, Stable)
            if can_add:
                self.animal_list.append(self.new_object)
                self.coins -= self.new_object.purchase_cost

        def add_plants():
            can_add = False
            if self.small_rects.index(self.chosen_object) == 0:
                self.new_object = Pumpkin('plants_pumpkin', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, Shed)
            elif self.small_rects.index(self.chosen_object) == 1:
                self.new_object = Carrot('plants_carrot', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, Shed)
            elif self.small_rects.index(self.chosen_object) == 2:
                self.new_object = Strawberry('plants_strawberry', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, Shed)
            elif self.small_rects.index(self.chosen_object) == 3:
                self.new_object = Tomato('plants_tomato', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, Shed)
            elif self.small_rects.index(self.chosen_object) == 4:
                self.new_object = Corn('plants_corn', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, Shed)
            elif self.small_rects.index(self.chosen_object) == 5:
                self.new_object = Watermelon('plants_watermelon', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, Shed)
            elif self.small_rects.index(self.chosen_object) == 9:
                self.new_object = BlackRose('flower_black_rose', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, GreenHouse)
            elif self.small_rects.index(self.chosen_object) == 10:
                self.new_object = Daisy('flower_daisy', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, GreenHouse)
            elif self.small_rects.index(self.chosen_object) == 11:
                self.new_object = Lily('flower_lily', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, GreenHouse)
            elif self.small_rects.index(self.chosen_object) == 12:
                self.new_object = Tulip('flower_tulip', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, GreenHouse)
            elif self.small_rects.index(self.chosen_object) == 13:
                self.new_object = RedRose('flower_red_rose', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, GreenHouse)
            elif self.small_rects.index(self.chosen_object) == 14:
                self.new_object = Geraniums('flower_geraniums', pos[0], pos[1])
                can_add = self.can_add_object(self.new_object, GreenHouse)
            if can_add:
                self.plants.append(self.new_object)
                self.collide_rects.append(self.new_object.new_object.get_rect())
                self.coins -= self.new_object.purchase_cost

        def delete():
            if self.big_rects.index(self.chosen_object) == 0:  # SELLING
                for build in self.buildings:  # Removal from buildings list
                    if build.new_object.collidepoint(pos):
                        delete_object(build, self.buildings, build.purchase_cost * 2 / 3)
                for feeder in self.feeders:  # Removal from feeders list
                    if feeder.new_object.collidepoint(pos):
                        delete_object(feeder, self.feeders, feeder.purchase_cost * 2 / 3)
                for plant in self.plants:  # Removal from plants list
                    if plant.new_object.collidepoint(pos):
                        delete_object(plant, self.plants, plant.purchase_cost * 2 / 3)
                for animal in self.animal_list:  # Removal from animal list
                    if animal.new_object.collidepoint(pos):
                        delete_object(animal, self.animal_list, animal.purchase_cost * 2 / 3)

            elif self.big_rects.index(self.chosen_object) == 1:  # BUTCHER
                for animal in self.animal_list:
                    if animal.new_object.collidepoint(pos) and hasattr(animal, 'meat'):
                        self.items['ad_meat'] += animal.meat
                        delete_object(animal, self.animal_list, 0)

            elif self.big_rects.index(self.chosen_object) == 2:  # UNLOCKING FIELDS
                if self.coins <= 2000:
                    self.draw_error = self.errors_list[0]
                    self.timer = time.time()
                else:
                    if len(set_map.first_barrier) > 1:
                        self.coins -= 2000
                        set_map.first_barrier = []
                        to_remove = self.collide_rects.index(self.first_barrier)
                        self.collide_rects.pop(to_remove)
                        self.barriers -= 1
                    elif len(set_map.first_barrier) < 1 < len(set_map.second_barrier):
                        self.coins -= 2000
                        set_map.second_barrier = []
                        to_remove = self.collide_rects.index(self.second_barrier)
                        self.collide_rects.pop(to_remove)
                        self.barriers -= 1
                    else:
                        self.draw_error = self.errors_list[1]
                        self.timer = time.time()

            elif self.big_rects.index(self.chosen_object) == 3:  # REMOVING OBSTACLES
                for i in set_map.all_list:
                    if i.structure.collidepoint_pixel(pos) and i.structure.get_rect() in self.collide_rects:
                        if self.coins >= 50:
                            self.coins -= 50
                            self.collide_rects.remove(i.structure.get_rect())
                            self.maps_items.append(i)
                            set_map.change_lists(i)
                        else:
                            self.draw_error = self.errors_list[0]
                            self.timer = time.time()

        def delete_object(item, item_list, return_money):
            if item.new_object.collidepoint(pos):
                if item.new_object.get_rect() in self.collide_rects:
                    delete_rect = self.collide_rects.index(item.new_object.get_rect())
                    self.collide_rects.pop(delete_rect)
                self.coins += int(return_money)
                delete_item = item_list.index(item)
                item_list.pop(delete_item)

        # Announcement START

        def realize_ad(processing_ad):
            for index, item in enumerate(processing_ad['items']):
                self.items[item.image] -= processing_ad['amount'][index]
            self.coins += processing_ad['prize']
            ad_to_remove = self.ads_list.index(processing_ad)
            self.ads_list.pop(ad_to_remove)
            for i in range(4):
                self.ads_board.next_image()

            self.ad_update()

        def are_items_enough(need, in_magazine):
            if need > self.items[in_magazine]:
                return False
            else:
                return True

        def check_ad(checking_ad):
            items_enough = True
            for index, item in enumerate(checking_ad['items']):
                items_enough = are_items_enough(checking_ad['amount'][index], item.image)
                if not items_enough:
                    break

            if items_enough:
                realize_ad(checking_ad)
            else:
                self.draw_error = self.errors_list[2]
                self.timer = time.time()

        if self.keys_active['show_board']:
            for ad in self.ads_list:
                if ad['do_it'] != None:
                    if ad['do_it'].collidepoint_pixel(pos[0], pos[1]):
                        check_ad(ad)

        # Announcement END
        if not self.keys_active['blocks_active'] and self.keys_active['menu_active']:
            choose_object()
        elif self.keys_active['blocks_active'] and self.keys_active['animal_menu']:
            add_animal()
        elif self.keys_active['blocks_active'] and self.keys_active['fences_menu']:
            add_fences()
        elif self.keys_active['blocks_active'] and self.keys_active['building_menu']:
            add_building()
        elif self.keys_active['blocks_active'] and self.keys_active['feeders_menu']:
            add_feeders()
        elif self.keys_active['blocks_active'] and self.keys_active['plants_menu']:
            add_plants()
        elif self.keys_active['blocks_active'] and self.keys_active['delete_menu']:
            delete()
        elif not self.keys_active['blocks_active'] and not self.keys_active['menu_active']:

            if self.ads_board.collidepoint_pixel(pos[0], pos[1]) or self.board.collidepoint_pixel(pos[0], pos[1]):
                self.keys_active['show_board'] = True

            for i in self.buildings:  # warehouse service
                if i.new_object.collidepoint(pos):
                    if type(i) is Shed or Stable or GreenHouse:
                        i.show_magazine = True

            for i in self.plants:  # add crops to magazine
                if i.ripe and i.new_object.collidepoint(pos):
                    self.add_plants_to_magazine(i)
                    delete_object(i, self.plants, 0)

            for i in self.feeders:
                if i.new_object.collidepoint(pos):
                    if not isinstance(i, HenNest):  # Adding eggs to the warehouse
                        if not i.is_full:
                            i.is_full = True
                            i.time_end = time.time()
                    if isinstance(i, HenNest) and i.eggs > 0:
                        for j in self.buildings:
                            if isinstance(j, Stable):
                                sm_bg = random.randint(1, 3)
                                if sm_bg == 1:
                                    self.items['ad_big_egg'] += i.eggs
                                else:
                                    self.items['ad_small_egg'] += i.eggs
                                i.eggs = 0

            for animal in self.animal_list:  # add products to magazine
                if animal.new_object.collidepoint(pos):
                    matter = None
                    if animal.existence['milk']:
                        animal.existence['milk'] = False
                        matter = 'ad_milk'
                    if animal.existence['thread']:
                        animal.existence['thread'] = False
                        matter = 'ad_thread'
                    if animal.existence['feather']:
                        animal.existence['feather'] = False
                        matter = 'ad_feather'
                    if matter is not None:
                        for building in self.buildings:
                            if isinstance(building, Stable):
                                self.items[matter] += 1
                                break
                        animal.show_info = False

    def can_add_object(self, new_object, required=None):
        if new_object.new_object.get_rect().collidelistall(self.collide_rects):
            self.draw_error = self.errors_list[3]
            self.timer = time.time()
            return False
        if required is not None and not self.required_buildings(required):
            self.timer = time.time()
            if self.language == 'pl':
                if required.__name__ == 'Stable':
                    required = 'Stajnie'
                elif required.__name__ == 'Shed':
                    required = 'Szope'
                elif required.__name__ == 'GreenHouse':
                    required = 'Szklarnie'
                self.draw_error = f'{self.errors_list[4]} {required}'
            self.draw_error = f'{self.errors_list[4]} {required.__name__}'
            return False
        if self.coins < self.new_object.purchase_cost:
            self.draw_error = self.errors_list[0]
            self.timer = time.time()
            return False
        else:
            return True

    def add_plants_to_magazine(self, plantorflower):
        self.items[plantorflower.plants_ad] += plantorflower.crops

    def close_windows(self):
        self.keys_active['animal_menu'] = False
        self.keys_active['fences_menu'] = False
        self.keys_active['plants_menu'] = False
        self.keys_active['building_menu'] = False
        self.keys_active['feeders_menu'] = False
        for i in self.buildings:
            i.show_magazine = False

    def on_key_down(self, key):
        if key == self.keys.B:
            self.building_mode()
        if key == self.keys.RIGHT:
            self.change_menu_tab('right')
        if key == self.keys.LEFT:
            self.change_menu_tab('left')
        if key == self.keys.ESCAPE:
            self.close_windows()
            self.keys_active['menu_active'] = False
            self.keys_active['blocks_active'] = False
            self.keys_active['feeders_menu'] = False
            self.keys_active['delete_menu'] = False
            self.keys_active['transparet_image'] = False
            self.keys_active['show_board'] = False
            self.new_object = None
            self.transparent_object = None

    def on_key_up(self, key):
        pass

    def on_mouse_move(self, pos):
        if self.keys_active['transparet_image']:
            if self.transparent_object is not None:
                self.transparent_object.x = pos[0]
                self.transparent_object.y = pos[1]

    def building_mode(self):
        if self.keys_active['menu_active']:
            self.keys_active['menu_active'] = False
        elif not self.keys_active['menu_active']:
            self.keys_active['blocks_active'] = False
            self.keys_active['transparet_image'] = False
            self.transparent_object = None
            self.keys_active['menu_active'] = True
        if not self.keys_active['blocks_active']:
            self.close_windows()

    def change_menu_tab(self, direction):
        if self.keys_active['menu_active']:
            if direction == 'left':
                for i in range(7):
                    self.menu.next_image()
            if direction == 'right':
                self.menu.next_image()

    def required_buildings(self, required):
        answer = False
        for i in self.buildings:
            if isinstance(i, required):
                answer = True
                break
        return answer

    def upgrade_announcement_dictionary(self):
        upgraded_dict = {}
        if self.required_buildings(Shed):
            upgraded_dict.update({'ad_pumpkin': 40, 'ad_carrot': 6, 'ad_strawberry': 3,
                                  'ad_tomato': 6, 'ad_corn': 5, 'ad_watermelon': 30})
        if self.required_buildings(Stable):
            upgraded_dict.update({'ad_big_egg': 20, 'ad_small_egg': 5, 'ad_milk': 10,
                                  'ad_meat': 40, 'ad_thread': 8, 'ad_feather': 8})
        if self.required_buildings(GreenHouse):
            upgraded_dict.update({'ad_black_rose': 50, 'ad_daisy': 5, 'ad_lily': 20,
                                  'ad_tulip': 20, 'ad_red_rose': 60, 'ad_geraniums': 10})
        return upgraded_dict

    # Announcement START
    def ad_update(self):
        for index, ad in enumerate(self.ads_list):
            ad['ad'].y = self.new_ad_y[index]
            try:
                ad['items'][0].y = self.new_ad_y[index]
                ad['items'][1].x = ad['ad'].x + 40
                ad['items'][1].y = self.new_ad_y[index]
                ad['items'][2].y = self.new_ad_y[index] + 60
                ad['items'][3].x = ad['ad'].x + 40
                ad['items'][3].y = self.new_ad_y[index] + 60
            except:
                pass

    def update(self):
        if len(self.ads_list) < 4:
            time = random.randint(1, 300)
            if time == 1:
                upgraded_dict = self.upgrade_announcement_dictionary()
                if len(upgraded_dict) > 1:
                    new_ad = CreateAd(self.board.x, self.new_ad_y[0], upgraded_dict).add_ad()
                    self.ads_list.append(new_ad)
                    self.ads_board.next_image()
                self.ad_update()

        # Announcement END

        for feeder in self.feeders:
            feeder.update()

            if not isinstance(feeder, HenNest) and feeder.time_end is not None:
                if feeder.time_end + SPEED_GAME * 1.5 < self.timer2:  # time of filled feeders and water tanks
                    feeder.is_full = False
                    feeder.time_end = None

        for building in self.buildings:  # warehouse service
            if isinstance(building, Stable) or isinstance(building, Shed) or isinstance(building, GreenHouse):
                for key in building.magazine_content.keys():
                    building.magazine_content[key] = self.items[f'ad_{key}']

        for plant in self.plants:
            plant.update()

        for animal in self.animal_list:
            animal.update()
            # Checking that animals have water and feed
            if any(isinstance(x, HorizontalCrib) and x.new_object.image == x.full_image for x in self.feeders) or \
                    any(isinstance(x, VerticalCrib) and x.new_object.image == x.full_image for x in self.feeders):
                animal.existence['water'] = True
            else:
                animal.existence['water'] = False

            if any(isinstance(x, Pasturge) and x.new_object.image == x.full_image for x in self.feeders):
                animal.existence['food'] = True
            else:
                animal.existence['food'] = False

            if hasattr(animal, 'baby_animal'):  # Animal reproduction
                for duplicate in self.animal_list:
                    if animal.__class__.__name__ == duplicate.__class__.__name__ and animal != duplicate and animal.existential_requirements:
                        reproduction = random.randint(1, animal.reproduction_speed)
                        if reproduction == 1:
                            kind = animal.baby_animal
                            birth = kind(animal.baby, animal.x + 5, animal.y + 5)
                            self.animal_list.append(birth)

            # Animals growing
            if hasattr(animal, 'grow_up'):
                if animal.grow_up > SPEED_GAME * 0.2 and animal.existential_requirements:
                    adult = animal.adult_animal(animal.adult, animal.new_object.x, animal.new_object.y)
                    delete_item = self.animal_list.index(animal)
                    self.animal_list.append(adult)
                    self.animal_list.pop(delete_item)

            if isinstance(animal, Chicken):  # Adding eggs to the henhouse
                if animal.add_eggs >= 1:
                    amount = animal.add_eggs
                    animal.add_eggs = 0
                    for feeder in self.feeders:
                        if type(feeder) is HenNest and not feeder.is_full:
                            feeder.eggs += amount
                            break

            for x in range(4):  # animal collision handling
                for plant in self.plants:
                    if animal.borders[x].colliderect(plant.new_object.get_rect()):
                        self.plants.remove(plant)
                if animal.borders[x].collidelistall(self.collide_rects):
                    if x in [0, 1, 2, 3]:
                        animal.new_object.status = 'idle'
                    if x == 0:
                        animal.new_object.x += 1
                        animal.new_object.images, animal.flip_x = check_status(animal.effigy, 'idle')
                    if x == 1:
                        animal.new_object.x -= 1
                        animal.new_object.images, animal.flip_x = check_status(animal.effigy, 'idle')
                    if x == 2:
                        animal.new_object.y += 1
                        animal.new_object.images, animal.flip_x = check_status(animal.effigy, 'idle')
                    if x == 3:
                        animal.new_object.y -= 1
                        animal.new_object.images, animal.flip_x = check_status(animal.effigy, 'idle')
