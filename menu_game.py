import os.path

from constains import *
from saving import Save
from tutorial import Tutorial
saving = Save()
tutorial = Tutorial()


class MenuGame:
    def __init__(self):
        self.background = Actor('menu_background')

        self.start = Actor('menu_start', pos=(WIDTH/2 - 400, HEIGHT/2 - 100))
        self.tutorial = Actor('menu_tutorial', pos=(WIDTH/2, HEIGHT/2 - 100))
        self.load = Actor('menu_load', pos=(WIDTH/2 + 400, HEIGHT/2 - 100))
        self.exit = Actor('menu_exit', pos=(WIDTH/2 - 400, HEIGHT/2 + 300))
        self.language = Actor('menu_language', pos=(WIDTH/2, HEIGHT / 2 + 300))
        self.save = Actor('menu_save', pos=(WIDTH/2 + 400, HEIGHT/2 + 300))
        self.back = Actor('menu_back', pos=(220, HEIGHT - 200))
        self.next = Actor('menu_next', pos=(WIDTH - 220, HEIGHT - 200))

        self.game_name = Actor('menu_josephs_farm', pos=(WIDTH/2, 150))
        self.save_load_info = Actor('menu_saved', pos=(250, HEIGHT/2))
        self.save_load_info.scale = 2

        self.developed = Actor('menu_developed', pos=(WIDTH - 200, HEIGHT - 120))
        self.selected_language = 'pl'
        self.arrow = Actor('menu_arrow', pos=(self.language.x - 75, self.language.y - 45))
        self.items = [self.start, self.tutorial, self.load, self.exit, self.language, self.save, self.arrow]

        self.field_active = {'menu_on': True, 'tutorial': False, 'save': False, 'load': False, 'saved': False,
                             'loaded': False}
        self.score = 0
        self.save_index = None
        self.load_index = None

        self.a = 0

    def draw(self, screen):
        self.background.draw()
        if self.field_active['tutorial']:
            self.back.draw()
            self.next.draw()
            tutorial.draw(screen)
            return

        if self.field_active['save'] or self.field_active['load']:
            if self.field_active['saved']:
                self.save_load_info.image = 'menu_saved'
                self.save_load_info.draw()
            elif self.field_active['loaded']:
                self.save_load_info.image = 'menu_loaded'
                self.save_load_info.draw()
            self.game_name.scale = 0.7
            self.game_name.draw()
            self.back.draw()
            saving.draw(screen)
            return

        if self.check_true():
            self.game_name.scale = 1
            self.game_name.draw()
            self.developed.draw()
            for item in self.items:
                item.draw()
            return

    def check_true(self):
        for x, y in self.field_active.items():
            if x == 'menu_on' and y:
                continue
            if x != 'menu_on' and not y:
                continue
            else:
                return False
        return True

    def on_mouse_down(self, pos):
        if self.start.collidepoint_pixel(pos[0], pos[1]) and self.check_true():
            self.field_active['menu_on'] = False

        elif self.save.collidepoint_pixel(pos[0], pos[1]) and self.check_true():
            saving.set_score(self.score)
            self.field_active['save'] = True

        elif self.load.collidepoint_pixel(pos[0], pos[1]) and self.check_true():
            self.field_active['load'] = True

        elif self.tutorial.collidepoint_pixel(pos[0], pos[1]) and self.check_true():
            self.field_active['tutorial'] = True

        elif self.exit.collidepoint_pixel(pos[0], pos[1]) and self.check_true():
            sys.exit()

        elif self.language.collidepoint_pixel(pos[0], pos[1]) and self.check_true():
            if self.selected_language == 'eng':
                self.selected_language = 'pl'
                tutorial.language = 'pl'
                self.arrow.y = self.language.y - 45
            elif self.selected_language == 'pl':
                self.selected_language = 'eng'
                tutorial.language = 'eng'
                self.arrow.y = self.language.y + 45

            tutorial.text_list = []
            tutorial.text = open(f'texts/tutorial_{tutorial.language}.txt', 'r', encoding="utf-8")
            for line in tutorial.text:
                tutorial.text_list.append(line)

        elif self.back.collidepoint_pixel(pos[0], pos[1]) and any((self.field_active['save'], self.field_active['load'])):
            self.field_active['save'] = False
            self.field_active['load'] = False
            self.field_active['saved'] = False
            self.field_active['loaded'] = False
            self.field_active['tutorial'] = False

        if self.field_active['tutorial']:
            if self.next.collidepoint_pixel(pos[0], pos[1]):
                if tutorial.slide >= 7:
                    self.field_active['tutorial'] = False
                    tutorial.slide = 0
                else:
                    tutorial.slide += 1
            if self.back.collidepoint_pixel(pos[0], pos[1]):
                if tutorial.slide <= 0:
                    self.field_active['tutorial'] = False
                    tutorial.slide = 0
                else:
                    tutorial.slide -= 1

    def on_key_down(self, key):
        if saving.editing:
            if key.name != 'RETURN':
                saving.append_to_name(key)
            if key.name == 'RETURN':
                self.save_index = saving.exit()
                saving.editing = False
                self.field_active['loaded'] = False
                self.field_active['saved'] = True

        elif self.field_active['save']:
            if key.name == 'UP':
                saving.now_index -= 1
            if key.name == 'DOWN':
                saving.now_index += 1
            if key.name == 'RETURN':
                saving.editing = True

        elif self.field_active['load']:
            if key.name == 'UP':
                saving.now_index -= 1
            if key.name == 'DOWN':
                saving.now_index += 1
            if key.name == 'RETURN':
                if os.path.isfile(f'saves/save{saving.now_index}'):
                    self.load_index = saving.now_index
                    self.field_active['loaded'] = True
                    self.field_active['saved'] = False
                else:
                    print('there is no save')

    def on_key_up(self, key):
        pass

    def update(self):
        if saving.now_index > 9:
            saving.now_index = 0
        if saving.now_index < 0:
            saving.now_index = 9
