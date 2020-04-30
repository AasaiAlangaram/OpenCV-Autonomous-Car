#!/usr/bin/env python
"""Interactive control for the car"""

import pygame
import pygame.font
import serial
import configuration

UP = LEFT = DOWN = RIGHT  = False

def get_keys():
    """Returns a tuple of (UP, DOWN, LEFT, RIGHT, change, stop) representing which keys are UP or DOWN and
    whether or not the key states changed.
    """
    change = False
    stop = False
    key_to_global_name = {
        pygame.K_LEFT: 'LEFT',
        pygame.K_RIGHT: 'RIGHT',
        pygame.K_UP: 'UP',
        pygame.K_DOWN: 'DOWN',
        pygame.K_ESCAPE: 'QUIT',
        pygame.K_q: 'QUIT'
    }
    for event in pygame.event.get():
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_x] or key_input[pygame.K_q]:
            stop = True
        elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
            down = (event.type == pygame.KEYDOWN)
            change = (event.key in key_to_global_name)
            if event.key in key_to_global_name:
                globals()[key_to_global_name[event.key]] = down
    return (UP, DOWN, LEFT, RIGHT, change, stop)


def interactive_control():
    """Runs the interactive control"""
    ser = serial.Serial('COM3', 115200, timeout=.1)
    setup_interactive_control()
    clock = pygame.time.Clock()

    command = 'idle'

    while True:
        up_key, down, left, right, change, stop = get_keys()
        if stop:
            ser.write(chr(5).encode())
            print('q or esp pressed')
            break

        if change:
            command = 'idle'

            if up_key:
                ser.write(chr(1).encode())
                command = 'forward'

            elif down:
                ser.write(chr(2).encode())
                command = 'reverse'

            append = lambda x: command + '_' + x if command != 'idle' else x

            if left:
                ser.write(chr(3).encode())
                command = append('left')

            elif right:
                ser.write(chr(4).encode())
                command = append('right')

        print(command)
        print(stop)

        clock.tick(30)
    pygame.quit()

def setup_interactive_control():
    """Setup the Pygame Interactive Control Screen"""
    pygame.init()
    display_size = (300, 400)
    screen = pygame.display.set_mode(display_size)
    background = pygame.Surface(screen.get_size())
    color_white = (255, 255, 255)
    display_font = pygame.font.Font(None, 40)
    pygame.display.set_caption('RC Car Interactive Control')
    text = display_font.render('Use arrows to move', 1, color_white)
    text_position = text.get_rect(centerx=display_size[0] / 2)
    background.blit(text, text_position)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def main():
    """Main function"""
    interactive_control()

if __name__ == '__main__':
    main()
