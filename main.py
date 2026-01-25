import pygame

pygame.init()

window_w, window_h = 800, 600
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Гра")

Clock = pygame.time.Clock()

font = pygame.font.Font(None, 60)

mouse_pos = (0, 0)
mouse_click = "0"

class MenuButton:
    def __init__(self, y, text):
        self.y = y
        self.text = text
        self.rect = pygame.rect.Rect((200, self.y, 400, 120))
        self.font = pygame.font.Font(None, 140)

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(400, self.y+60))    
    
    def update(self):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, (180, 180, 180), self.rect)
            window.blit(self.text_surface, self.text_rect)
            if mouse_click == "1":
                return True
        else:
            pygame.draw.rect(window, (140, 140, 140), self.rect)
            window.blit(self.text_surface, self.text_rect)

        return False

Play_button = MenuButton(100, "Play")

in_menu = True

def menu():
    window.fill((255, 255, 255))

    if Play_button.update():
        global in_menu
        in_menu = False


def game():
    pass

run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = "0"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = "1"
            if event.button == 2:
                mouse_click = "2"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = True

    if in_menu:
        menu()
    else:
        game()

    pygame.display.update()

    Clock.tick(60)