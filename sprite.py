import random
from constains import *


def get_sprites(index, name):
    sprites = []
    for i in range(1, index + 1):
        if name + str(i) not in sprites:
            sprites.append(name + str(i))

    return sprites


def random_move(cannot):
    animal_status = None
    animal_choice = random.randint(0, 10)
    if animal_choice == cannot:
        random_move(cannot)
    if animal_choice == 1:
        animal_status = 'walk_right'
    elif animal_choice == 2:
        animal_status = 'walk_left'
    elif animal_choice == 3:
        animal_status = 'walk_up'
    elif animal_choice == 4:
        animal_status = 'walk_down'
    else:
        animal_status = 'idle'

    return animal_status


def check_status(animal_type, status):
    flipped = None
    images = None
    if status == 'idle':
        images = get_sprites(1, f'{animal_type}_idle')
    if status == 'walk_down':
        images = get_sprites(4, f'{animal_type}_walk_down')
    if status == 'walk_up':
        images = get_sprites(4, f'{animal_type}_walk_up')
    if status == 'walk_left':
        images = get_sprites(4, f'{animal_type}_walk')
        flipped = True
    if status == 'walk_right':
        images = get_sprites(4, f'{animal_type}_walk')
        flipped = False
    return images, flipped


def where_can_move(status, x, y):
    x = x
    y = y
    cannot = None
    if moveimage.get_at((int(x + 3), int(y))) != Color(GREEN_GRASS):
        cannot = 1
        x -= 5
        status = 'idle'
    elif moveimage.get_at((int(x - 3), int(y))) != Color(GREEN_GRASS):
        cannot = 2
        x += 5
        status = 'idle'
    elif moveimage.get_at((int(x), int(y - 3))) != Color(GREEN_GRASS):
        cannot = 3
        y += 5
        status = 'idle'
    elif moveimage.get_at((int(x), int(y + 3))) != Color(GREEN_GRASS):
        cannot = 4
        y -= 5
        status = 'idle'

    return cannot, x, y, status

