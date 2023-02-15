import pgzrun
import pygame
from pgzero.screen import Screen
from pgzero.builtins import keyboard, music

from constains import *
from set_time import SetTime
from menu import Menu
from menu_game import MenuGame
from new_save import NewSave, LoadSave

keys: keyboard
screen: Screen
menu = Menu(keys)
set_time = SetTime()
menu_game = MenuGame()


def draw():
    if menu_game.field_active['menu_on']:
        menu_game.draw(screen)
        return
    else:
        background.draw()
        set_time.draw()
        menu.draw(screen)


def on_mouse_down(pos):

    if menu_game.field_active['menu_on']:
        menu_game.on_mouse_down(pos)
        return
    try:
        menu.on_mouse_down(pos)
        if menu.back_to_menugame.collidepoint_pixel(pos[0], pos[1]):
            menu_game.field_active['menu_on'] = True
    except:
        print(f'{pos} is out of bounds')


def on_key_down(key):
    menu.on_key_down(key)
    if menu_game.field_active['menu_on']:
        menu_game.on_key_down(key)
    if keyboard.f:
        if is_fullscreen():
            surface_size = screen.surface.get_size()
            screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        else:
            surface_size = screen.surface.get_size()
            screen.surface = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), pygame.FULLSCREEN)
        change_fullscreen()


def on_key_up(key):
    menu.on_key_up(key)
    if menu_game.field_active['menu_on']:
        menu_game.on_key_up(key)


def on_mouse_move(pos):
    menu.on_mouse_move(pos)


def update():
    if menu.language != menu_game.selected_language:
        menu.language = menu_game.selected_language
        menu.check_language()

    if menu_game.save_index is not None:
        data = [menu.buildings, menu.animal_list, menu.plants, menu.feeders, menu.maps_items, menu.coins, set_time.time_oclock,
                set_time.date_day, menu.barriers, menu.items]
        NewSave(menu_game.save_index, data).save_it()
        menu_game.save_index = None

    if menu_game.load_index is not None:
        load_data = LoadSave(menu_game.load_index).load_it()
        menu.load_save(load_data)
        set_time.load_save(load_data[5], load_data[6])
        menu_game.load_index = None

    if menu_game.field_active['menu_on']:
        menu_game.score = menu.coins
        menu_game.update()
    else:
        set_time.update()
        menu.update()


music.play('country-swing-with-harmonica-1357')
music.set_volume(0.1)
pgzrun.go()