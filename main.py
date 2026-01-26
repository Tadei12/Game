import pygame

pygame.init()

window_w, window_h = 1100, 700
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Game")

Clock = pygame.time.Clock()

run = True

computer_off = pygame.transform.scale(pygame.image.load("assets/computer/off.png"), (400, 350))
computer_on = pygame.transform.scale(pygame.image.load("assets/computer/on.png"), (400, 350))

game_background_n1 = pygame.transform.scale(pygame.image.load("assets/game/background_-1.png"), (1100, 700))
game_background_0 = pygame.transform.scale(pygame.image.load("assets/game/background_0.png"), (1100, 700))

key_press = ""

mouse_pos = (0, 0)
mouse_click = 0

class TextButton:
    def __init__(self, rect_value, text):
        self.x = rect_value[0]
        self.y = rect_value[1]
        self.w = rect_value[2]
        self.h = rect_value[3]
        self.text = text
        self.rect = pygame.rect.Rect((self.x, self.y, self.w, self.h))
        self.font = pygame.font.Font("assets/font.ttf", 50)

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.x+self.w/2, self.y+self.h/2))
        self.text_rect.x = self.x+15
    
    def update(self):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, (50, 50, 50), self.rect)
            if mouse_click == 1:
                return True
        
        window.blit(self.text_surface, self.text_rect)

        return False

Play_button = TextButton((30, 300, 200, 60), "Play")
Placeholder_button = TextButton((30, 380, 200, 60), "...")
Exit_button = TextButton((30, 460, 200, 60), "Exit")

in_menu = True

def menu():
    global in_menu, run
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (100, 100, 100), (0, 0, window_w/4, window_h))

    if Play_button.update():
        in_menu = False

    if Placeholder_button.update():
        pass

    if Exit_button.update():
        run = False

looking = 0
computer_status = 0

def game():
    global looking, computer_status

    window.fill((150, 200, 255))

    if looking == -1:
        window.blit(game_background_n1, (0, 0))

    if looking == 0:
        if key_press == "q":
            computer_status = not computer_status

        window.blit(game_background_0, (0, 0))

        pygame.draw.rect(window, (200, 100, 0), (0, 450, window_w, 200))

        if computer_status:
            window.blit(computer_on, (350, 250))
        else:
            window.blit(computer_off, (350, 250))
    
    if key_press == "a":
        if looking > -1:
            looking -= 1
    if key_press == "d":
        if looking < 1:
            looking += 1

while run:
    key_press = ""

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = 1
            if event.button == 2:
                mouse_click = 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = True
            else:
                key_press = pygame.key.name(event.key)

    if in_menu:
        menu()
    else:
        game()

    pygame.display.update()

    Clock.tick(60)
