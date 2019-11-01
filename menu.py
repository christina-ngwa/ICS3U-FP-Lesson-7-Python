#!/usr/bin/env python3

# Created by: Christina Ngwa
# Created on: October 2019
# This file is the "Space Aliens" game
#    for CircuitPython

import ugame
import stage

import constants


def menu_scene():
    # This function is the splash game loop

    # New pallet for black filled text
    NEW_PALETTE = (b'\xff\xff\x00\x22\xcey\x22\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                   b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # set the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_X, constants.SCREEN_Y)

    # a list of sprites that wil be updated every frame
    sprites = []

    # add text objects
    text = []
    text1 = stage.Text(width = 29, height = 12, font = None, palette = NEW_PALETTE, buffer = None)
    text1.move(20, 10)
    text1.text("MT Game Studios")
    text.append(text1)

    text2 = stage.Text(width = 29, height = 12, font = None, palette = NEW_PALETTE, buffer = None)
    text2.move(40, 110)
    text2.text("PRESS START")
    text.append(text2)


    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = text + sprites + [background]
    # render the background and initial location sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)

        # Start button is pressed
        if keys & ugame.K_START != 0:
            game_scene()

        # update game logic

        # redraw sprite list
        # game.render_sprites()
        game.tick() # wait until refresh rate finishes

def game_scene():
    # This function is a scene

    # buttons that you want to keep state information on
    a_button = constants.button_state["button_up"]
    b_button = constants.button_state["button_up"]
    start_button = constants.button_state["button_up"]
    select_button = constants.button_state["button_up"]

    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_X,
                            constants.SCREEN_Y)

    # a list of sprites that will be updated every frame
    sprites = []

    ship = stage.Sprite(image_bank_1, 5, int(constants.SCREEN_X / 2
                        - constants.SPRITE_SIZE / 2), int(constants.SCREEN_Y -
                        constants.SPRITE_SIZE))
    sprites.append(ship)  # insert at the top of sprite list

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = sprites + [background]
    # render the background and inital location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)

        # update game logic
        # A button to fire
        if keys & ugame.K_X != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]

        # move ship right
        if keys & ugame.K_RIGHT != 0:
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
            else:
                ship.move(ship.x + 1, ship.y)

        # move ship left
        if keys & ugame.K_LEFT != 0:
            if ship.x < 0:
                ship.move(0, ship.y)
            else:
                ship.move(ship.x - 1, ship.y)
        # play sound if A is pressed
        if a_button == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        # redraw sprite list
        game.render_sprites(sprites)
        game.tick()  # wait until refresh rate finishes



if __name__ == "__main__":
    menu_scene()
