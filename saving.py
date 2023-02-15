from datetime import datetime
from constains import *


class Save:
    def __init__(self):
        self.saves_tab = Actor('menu_save_tab', pos=(WIDTH/2, HEIGHT/2 + 100), anchor=('center', 'center'))
        self.now_index = 0
        self.save_index = 0
        self.name = ''
        self.score = 0
        self.date_now = datetime.now().strftime('%Y-%m-%d/%H:%M:%S')
        self.editing = False
        self.positions = []
        with open('saves/saves_table.txt', 'r') as file:
            for index, line in enumerate(file):
                split_line = line.split()
                self.positions.append((index, split_line[0], split_line[1], split_line[2]))

    def set_score(self, score):
        self.score = score

    def exit(self):
        if len(self.name) < 1:
            self.name = 'NoName'
        self.positions.pop(self.now_index)
        self.positions.append((self.now_index, self.name, self.score, self.date_now))
        self.positions.sort(key=lambda x: x[0])
        self.positions = [(index, position[1], position[2], position[3]) for index, position in enumerate(self.positions)]
        self.name = ''
        lines = []
        for index, name, score, date_now in self.positions:
            lines.append(f'{name} {score} {date_now}\n')
        with open('saves/saves_table.txt', 'w') as file:
            file.writelines(lines)
        return self.now_index

    def append_to_name(self, key):
        if key.name == 'BACKSPACE':
            self.name = self.name[:-1]
        if len(self.name) <= 7:
            if key.name[:2] == 'K_':
                self.name += key.name[-1]
            elif len(key.name) == 1:
                self.name += key.name
            elif key.name == 'SPACE':
                self.name += ' '

    def draw(self, screen):
        self.date_now = datetime.now().strftime('%Y-%m-%d/%H:%M:%S')
        self.saves_tab.draw()
        for i, line in enumerate(self.positions):
            index, name, score, date_now = line
            if index == self.now_index and self.editing:
                screen.draw.text(f'{self.name}_', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 0.60, self.saves_tab.y * 0.65 + 50 * i))
                screen.draw.text(f'{self.score}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 0.8, self.saves_tab.y * 0.65 + 50 * i))
                screen.draw.text(f'{self.date_now}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 1, self.saves_tab.y * 0.65 + 50 * i))
            elif index == self.now_index and not self.editing:
                screen.draw.text(f'{name}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 0.60, self.saves_tab.y * 0.65 + 50 * i))
                screen.draw.text(f'{score}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 0.8, self.saves_tab.y * 0.65 + 50 * i))
                screen.draw.text(f'{date_now}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 1, self.saves_tab.y * 0.65 + 50 * i))
            else:
                screen.draw.text(f'{name}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 0.60, self.saves_tab.y * 0.65 + 50 * i),
                                 owidth=1, ocolor=(100, 100, 100))
                screen.draw.text(f'{score}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 0.8, self.saves_tab.y * 0.65 + 50 * i),
                                 owidth=1, ocolor=(100, 100, 100))
                screen.draw.text(f'{date_now}', color=BEIGE, fontsize=tab_fs, fontname='bungee-regular',
                                 topleft=(self.saves_tab.x * 1, self.saves_tab.y * 0.65 + 50 * i),
                                 owidth=1, ocolor=(100, 100, 100))
