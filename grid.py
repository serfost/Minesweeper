from random import randint
import pygame


class Grid :
    BOOM = False
    first_move = True
    def __init__(self, width, height, n_squares_x, n_squares_y, n_bombs) :
        self.width = width
        self.height = height
        self.n_squares_x = n_squares_x
        self.n_squares_y = n_squares_y
        self.squares_width = width // n_squares_x
        self.squares_height = height // n_squares_y
        self.n_bombs = n_bombs
        self.squares = self.generate_squares()

    def generate_squares(self) :            
        squares = []
        for x in range(self.n_squares_x) :
            for y in range(self.n_squares_y) :
                squares.append(
                    Square(
                        x, y,
                        self.squares_width,
                        self.squares_height
                        )
                    )        
        return squares

    def init_squares(self, first_squares) :
        bomb_coords = []
        while len(bomb_coords) <= self.n_bombs :
            bomb_x = randint(0,self.n_squares_x-1)
            bomb_y = randint(0,self.n_squares_y-1)
            if (bomb_x,bomb_y) not in bomb_coords :
                if (bomb_x,bomb_y) not in [square.pos for square in first_squares] :
                    bomb_coords.append((bomb_x,bomb_y))

        for bomb_pos in bomb_coords :
            self.get_square_from_pos(bomb_pos).bomb = True
                
        for square in self.squares :
            if not square.bomb :
                square.value = 0
                for surrounding_square in square.get_surrounding_squares(self) :
                    if surrounding_square.bomb :
                        square.value += 1

    def get_square_from_pos(self, pos) :
        for square in self.squares :
            if square.pos == pos :
                return square

    def victory(self) :
        if all(square.discovered or square.bomb for square in self.squares) :
            return True
        else :
            return False

    def handle_click(self, button, mx, my) :
        x = mx // self.squares_width
        y = my // self.squares_height
        clicked_square = self.get_square_from_pos((x,y))
        if button == 1 :
            clicked_square.discover(self)
        elif button == 3 :
            clicked_square.flag_square()

    def draw(self, display) :
        for square in self.squares :
            square.draw(display)

class Square :
    discovered = False
    flag = False
    bomb = False
    value = 0
    def __init__(self, x, y, width, height) :
        self.x = x
        self.y = y
        self.abs_x = x * width
        self.abs_y = y * height
        self.pos = (x,y)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(
            self.abs_x,
            self.abs_y,
            self.width - 1,
            self.height - 1
        )

    def flag_square(self) :
        if not self.discovered :
            self.flag = False if self.flag else True

    def get_surrounding_squares(self, grid) :
        surrounding_squares = []
        for x in range(self.x-1, self.x+2) :
            for y in range(self.y-1, self.y+2) :
                if ( (x,y) != self.pos
                     and x >= 0
                     and y >= 0
                     and x < grid.n_squares_x
                     and y < grid.n_squares_y ) :
                    surrounding_squares.append(
                        grid.get_square_from_pos((x,y))
                    )
        return surrounding_squares

    def discover(self, grid) :
        if self.discovered and self.value == sum(square.flag == True for square in self.get_surrounding_squares(grid)) :
            for square in self.get_surrounding_squares(grid) :
                    if not square.discovered and not square.flag :
                        square.discover(grid)
        if not self.flag :
            self.discovered = True
            if grid.first_move :
                grid.init_squares(self.get_surrounding_squares(grid) + [self])
                grid.first_move = False
            if self.value == 0 :
                for square in self.get_surrounding_squares(grid) :
                    if not square.discovered :
                        square.discover(grid)
            if self.bomb :
                for square in grid.squares :
                    if square.bomb :
                        square.discovered = True
                grid.BOOM = True

    def draw(self, display) :
        if self.discovered :
            if self.bomb :
                pygame.draw.rect(display,(200,0,0),self.rect)
                img = pygame.image.load("img/bomb.png").convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                centering_rect = img.get_rect()
                centering_rect.center = self.rect.center
                display.blit(img, centering_rect.topleft)
            else :
                pygame.draw.rect(display,(20,20,20),self.rect)
                font = pygame.font.Font(None, 37)
                text = font.render(str(self.value), True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.center = self.rect.center
                display.blit(text, text_rect.topleft)
        elif self.flag :
            pygame.draw.rect(display,(100,100,100),self.rect)
            img = pygame.image.load("img/flag.png").convert_alpha()
            img = pygame.transform.scale(img, (self.width, self.height))
            centering_rect = img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(img, centering_rect.topleft)
        else :
            pygame.draw.rect(display,(100,100,100),self.rect)
