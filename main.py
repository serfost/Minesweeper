from grid import Grid
import pygame
import pygame_menu
from pygame_menu import themes

pygame.init()

MENU_WINDOW_SIZE = (600,600)
screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

square_width = 10
square_height = 10
n_bombs = 10

def draw(display) :
    display.fill('black')
    grid.draw(display)
    pygame.display.update()

def set_difficulty(difficulty, value) :
    global square_width, square_height, n_bombs
    match value :
        case 1 :
            square_width, square_height, n_bombs = (10,10,10)
        case 2 :
            square_width, square_height, n_bombs = (15,15,35)
        case 3 :
            square_width, square_height, n_bombs = (20,20,50)


def game() :
    global grid
    global screen
    WINDOW_SIZE = (square_width*30,square_height*30)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    grid = Grid(
        WINDOW_SIZE[0],
        WINDOW_SIZE[1],
        square_width,
        square_height,
        n_bombs
    )
    running = True
    while running :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                mx, my = pygame.mouse.get_pos()
                grid.handle_click(event.button, mx, my)
                if grid.BOOM :
                    running = False
                    print("YOU LOST !")
                if grid.victory() :
                    running = False
                    print("YOU WON !")
        draw(screen)
    screen = pygame.display.set_mode(MENU_WINDOW_SIZE)
        
if __name__ == '__main__' :
    mainmenu = pygame_menu.Menu('Welcome',
                                MENU_WINDOW_SIZE[0],
                                MENU_WINDOW_SIZE[1], 
                                theme=themes.THEME_SOLARIZED)
    
    mainmenu.add.button('Play', game)

    mainmenu.add.selector('Select difficulty :', [('easy', 1), ('medium', 2), ('hard',3)], onchange=set_difficulty)
    
    mainmenu.mainloop(screen)
