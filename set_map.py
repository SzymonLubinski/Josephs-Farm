from pgzhelper import *


class SetMap:
    def __init__(self):

        self.all_list = self.create_map()
        self.first_barrier = [Wall(380, 600), Gate(440, 600), Wall(500, 600)]
        self.second_barrier = [WallVertical(1350, 880), WallVertical(1350, 820)]
        self.copy1 = self.all_list.copy()
        self.copy2 = self.first_barrier.copy()
        self.copy3 = self.second_barrier.copy()

    def create_map(self):
        map_list = [Lamp(560, 130), Bench(510, 165), TreeLeafyBig(210, 60), TreeLeafyBig(300, 60), TreeConifer(253, 65),
                    TreeLeafyBig(350, 60),
                    TreeLeafyBig(420, 70), TreeLeafySmall(178, 77), TreeLeafySmall(290, 102),
                    TreeConifer(253, 72), TreeConifer(310, 90), TreeConifer(390, 95), TreeConifer(370, 950),
                    TreeConifer(390, 990), TreeConifer(350, 995), TreeLeafyBig(420, 950),
                    TreeLeafySmall(428, 1000), TreeLeafyBig(470, 985), TreeLeafyBig(1720, 467),
                    TreeConifer(1800, 500), TreeConifer(1830, 520), TreeConifer(1780, 540),
                    TreeConifer(1815, 550), TreeConifer(1765, 560), TreeConifer(1820, 585),
                    TreeConifer(1770, 615), TreeConifer(1802, 626), TreeConifer(1845, 616),
                    TreeConifer(130, 240), TreeConifer(90, 250), TreeConifer(170, 260),
                    TreeConifer(128, 270), TreeConifer(93, 280), TreeConifer(166, 280),
                    TreeConifer(90, 310), TreeConifer(115, 330), TreeConifer(150, 320),
                    TreeLeafyBig(1550, 800), TreeLeafySmall(1575, 795), TreeLeafyBig(1615, 812),
                    TreeLeafySmall(1535, 855), TreeLeafyBig(1600, 860), TreeLeafySmall(1630, 860),
                    TreeLeafyBig(1550, 900), TreeLeafySmall(1585, 905), TreeLeafyBig(1615, 930),
                    TreeLeafySmall(1585, 950), TreeLeafyBig(1635, 970), TreeLeafySmall(1680, 990),
                    TreeLeafyBig(1645, 800), TreeLeafySmall(1682, 785), TreeLeafyBig(1720, 820),
                    TreeLeafySmall(1663, 858), TreeLeafyBig(1705, 860), TreeLeafySmall(1770, 860),
                    TreeLeafyBig(1675, 900), TreeLeafySmall(1715, 905), TreeLeafyBig(1744, 920),
                    TreeLeafySmall(1671, 960), TreeLeafyBig(1722, 975), TreeLeafySmall(1752, 1000),
                    TreeConifer(970, 640), TreeConifer(1010, 631), TreeConifer(1050, 634),
                    TreeLeafyBig(1080, 653), TreeLeafySmall(960, 692), TreeLeafyBig(1005, 670),
                    TreeLeafySmall(1040, 705), TreeLeafyBig(946, 730), TreeLeafySmall(1000, 722),
                    TreeLeafySmall(1065, 740), TreeLeafyBig(1085, 705), TreeLeafySmall(1100, 740),
                    StoneOne(300, 500), StoneOne(160, 510), StoneOne(210, 525), StoneOne(291, 530),
                    StoneTwo(278, 470), StoneOne(210, 502), StoneOne(325, 530), StoneTwo(200, 475),
                    StoneOne(170, 532), StoneOne(230, 535), StoneTwo(250, 510), StoneOne(515, 995),
                    StoneOne(528, 1017), StoneTwo(555, 995), StoneOne(100, 120), StoneOne(138, 150),
                    StoneOne(500, 950), StoneTwo(540, 940), StoneOne(520, 970), StoneOne(570, 965),
                    StoneOne(600, 1000), StoneTwo(605, 960), StoneOne(590, 930), StoneOne(599, 900),
                    StoneOne(130, 122), StoneTwo(175, 127), StoneOne(84, 175), StoneOne(175, 175),
                    StoneOne(90, 145), StoneTwo(130, 180), StoneOne(155, 200), StoneOne(95, 195)]
        return map_list

    def export_items(self):
        pass

    def change_lists(self, deleting):
        self.all_list.remove(deleting)

    def draw(self):
        for i in self.all_list:
            i.draw()
        for i in self.first_barrier:
            i.draw()
        for i in self.second_barrier:
            i.draw()


class AddObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.structure = Actor('tree_leafy_big', pos=(self.x, self.y))
        self.effigy = 'tree_leafy_big'
        self.structure.scale = 2

    def draw(self):
        self.structure.draw()


class TreeLeafyBig(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('tree_leafy_big', pos=(x, y))
        self.effigy = 'tree_leafy_big'
        self.structure.scale = 2


class TreeLeafySmall(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('tree_leafy_small', pos=(x, y))
        self.effigy = 'tree_leafy_small'
        self.structure.scale = 2


class TreeConifer(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('tree_conifer', pos=(x, y))
        self.effigy = 'tree_conifer'
        self.structure.scale = 2


class StoneOne(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('stone_two', pos=(x, y))
        self.effigy = 'stone_two'
        self.structure.scale = 2


class StoneTwo(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('stone_two', pos=(x, y))
        self.effigy = 'stone_two'
        self.structure.scale = 3


class MushroomBrown(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('mushroom_brown', pos=(x, y))
        self.effigy = 'mushroom_brown'
        self.structure.scale = 2


class MushroomPurple(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('mushroom_purple', pos=(x, y))
        self.effigy = 'mushroom_purple'
        self.structure.scale = 2


class Lamp(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('black_lamp', pos=(x, y))
        self.effigy = 'black_lamp'
        self.structure.scale = 2


class Bench(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('bench', pos=(x, y))
        self.effigy = 'bench'
        self.structure.scale = 2


class Wall(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('stone_wall', pos=(x, y))
        self.effigy = 'stone_wall'
        self.structure.scale = 2


class WallVertical(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('stone_vertical_wall', pos=(x, y))
        self.effigy = 'stone_vertical_wall'
        self.structure.scale = 2


class Gate(AddObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.structure = Actor('stone_gate', pos=(x, y))
        self.effigy = 'stone_gate'
        self.structure.scale = 2
