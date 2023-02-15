from sprite import *


class Tutorial:
    def __init__(self):
        self.slide = 0
        self.board = Actor('menu_text_board', pos=(WIDTH / 2, 840))

        self.joseph1 = Actor('joseph1', pos=(1500, 50), anchor=('center', 'top'))
        self.joseph2 = Actor('joseph2', pos=(1500, 50), anchor=('center', 'top'))
        self.joseph3 = Actor('joseph3', pos=(1500, 50), anchor=('center', 'top'))

        self.background_list = [Actor('tutorial1'), Actor('tutorial2'), Actor('tutorial3'),
                                Actor('tutorial4'), Actor('tutorial5'), Actor('tutorial6'),
                                Actor('tutorial7'), Actor('tutorial8')]

        self.text_list = []
        self.language = 'pl'
        self.text = open(f'texts/tutorial_{self.language}.txt', 'r', encoding="utf-8")
        for line in self.text:
            self.text_list.append(line)

    def draw(self, screen):
        self.board.draw()
        if 1 > self.slide >= 0:
            self.joseph1.draw()
        elif 4 >= self.slide >= 1:
            self.joseph2.draw()
        elif 7 >= self.slide > 4:
            self.joseph3.draw()
        if 7 >= self.slide >= 0:
            screen.draw.text(f'{self.text_list[self.slide]}', center=(WIDTH / 2, 850), color=BEIGE,
                             fontsize=26, fontname='bungee-regular', owidth=1, ocolor=BROWN, width=840)
            self.background_list[self.slide].draw()
