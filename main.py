import time

import pygame

pygame.init()

window_w, window_h = 1100, 700
window = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Game")

window.fill((0,0,0))
loading_font = pygame.font.Font("assets/font.ttf", 30)
loading_text = loading_font.render("...", True, (255, 255, 255))
window.blit(loading_text, (0, window_h-40))
pygame.display.update()

Clock = pygame.time.Clock()

run = True

import json

with open("assets/settings.json", "r") as file:
    settings = json.load(file)

language = settings["language"]

if language == "eng":
    loading_text = loading_font.render("Loading...", True, (255, 255, 255))
else:
    loading_text = loading_font.render("Завантажування...", True, (255, 255, 255))

game_background_0 = pygame.transform.scale(pygame.image.load("assets/game/background_0.png"), (1100, 700))

window.blit(game_background_0, (0, 0))
window.blit(loading_text, (0, window_h-40))
pygame.display.update()

computer_off = pygame.transform.scale(pygame.image.load("assets/computer/off.png"), (400, 350))
computer_on = pygame.transform.scale(pygame.image.load("assets/computer/on.png"), (400, 350))

studio_logo = pygame.transform.scale(pygame.image.load("assets/studio_logo.png"), (300, 300))

shade = pygame.Surface((window_w, window_h), pygame.SRCALPHA)
for y in range(window_h):
    alpha = int((y / window_h) * 255)
    pygame.draw.line(shade, (0, 0, 0, alpha), (0, y), (window_w, y))

def draw_bg_screen():
    window.blit(game_background_0, (0, 0))
    pygame.draw.rect(window, (150, 150, 150), (0, 450, window_w, 200))
    window.blit(computer_off, (350, 250))
    window.blit(shade, (0, 50))

def draw_loading_screen(intro=False):
    draw_bg_screen()
    window.blit(loading_text, (0, window_h-40))
    if intro:
        window.blit(studio_logo, (400, 200))
    pygame.display.update()
    if intro:
        time.sleep(1)

draw_loading_screen(True)

game_background_n1open = pygame.transform.scale(pygame.image.load("assets/game/background_-1open.png"), (1100, 700))
game_background_n1closed = pygame.transform.scale(pygame.image.load("assets/game/background_-1closed.png"), (1100, 700))

door_rect = pygame.Rect(325, 25, 450, 575)

game_background_1open = pygame.transform.scale(pygame.image.load("assets/game/background_1open.png"), (1100, 700))
game_background_1closed = pygame.transform.scale(pygame.image.load("assets/game/background_1closed.png"), (1100, 700))

window_rect = pygame.Rect(375, 50, 350, 500)

light_switch = pygame.transform.scale(pygame.image.load("assets/game/light_switch.png"), (50, 75))
light_switch_rect = light_switch.get_rect()
light_switch_rect.x, light_switch_rect.y = 225, 250

pygame.mixer.init()

computer_sound = pygame.mixer.Sound("assets/sound/computer_noise.mp3")
pygame.mixer.music.load("assets/sound/office_ambience.mp3")

key_press = ""

mouse_pos = (0, 0)
mouse_click = 0
mouse_hold = 0

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

if language == "eng":
    Play_button = TextButton((30, 300, 200, 60), "Play")
    Language_button = TextButton((30, 380, 200, 60), "Ukr")
    Exit_button = TextButton((30, 460, 200, 60), "Exit")
elif language == "ukr":
    Play_button = TextButton((30, 300, 200, 60), "Грати")
    Language_button = TextButton((30, 380, 200, 60), "Англ.")
    Exit_button = TextButton((30, 460, 200, 60), "Вийти")

in_menu = True

def menu():
    global in_menu, run

    draw_bg_screen()

    pygame.draw.rect(window, (100, 100, 100), (0, 0, window_w/4, window_h))

    pygame.mixer.music.stop()

    if Play_button.update():
        in_menu = False
        pygame.mixer.music.play(-1)

    if Language_button.update():
        import sys
        import subprocess

        global language

        if language == "eng":
            language = "ukr"
        else:
            language = "eng"

        data = {
            "language": language
        }
        with open("assets/settings.json", "w") as file:
            file.write(json.dumps(data, indent=4))

        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()

    if Exit_button.update():
        run = False

def day():
    pass

def mascot_leave():
    window.fill((20, 20, 20))
    pygame.display.update()
    time.sleep(0.1)

looking = 0
computer_status = 0
door_status = 0
light_status = 1
window_status = 0

font = pygame.font.Font("assets/font.ttf", 30)
boot_time = "None"
night_percent = 0
previous_percent = 0

def office():
    global looking, computer_status, door_status, light_status, window_status, boot_time, night_percent, previous_percent

    window.fill((150, 200, 255))

    if looking == -1:
        if light_status:
            if door_status:
                window.blit(game_background_n1closed, (0, 0))
            else:
                window.blit(game_background_n1open, (0, 0))
            
            if door_rect.collidepoint(mouse_pos) and mouse_hold == 1:
                door_status = 1
            else:
                door_status = 0
        else:
            window.fill((0, 0, 0))

        window.blit(light_switch, light_switch_rect)
        if light_switch_rect.collidepoint(mouse_pos) and mouse_click == 1:
            light_status = not light_status

    if looking == 0:
        if key_press == "q":
            computer_status = not computer_status
            if computer_status:
                computer_sound.play(-1)
                boot_time = pygame.time.get_ticks()
            else:
                computer_sound.stop()
                previous_percent = night_percent

        window.blit(game_background_0, (0, 0))

        pygame.draw.rect(window, (150, 150, 150), (0, 450, window_w, 200))

        if computer_status:
            window.blit(computer_on, (350, 250))

            night_percent = int((pygame.time.get_ticks() - boot_time)/2400+previous_percent)

            if language == "eng":
                text = font.render(f"Working: {night_percent}%", True, (255, 255, 255))
            else:
                text = font.render(f"Робота: {night_percent}%", True, (255, 255, 255))
            text_rect = text.get_rect(center=(550, 425))

            window.blit(text, text_rect)

            if night_percent >= 100:
                time.sleep(0.5)
        else:
            window.blit(computer_off, (350, 250))

    if looking == 1:
        if window_status:
            window.blit(game_background_1closed, (0, 0))
        else:
            window.blit(game_background_1open, (0, 0))
        
        if window_rect.collidepoint(mouse_pos) and mouse_hold == 1:
            window_status = 1
        else:
            window_status = 0

    window.blit(shade, (0, 50))

    if not door_status and light_status and not window_status and not computer_status:
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
                mouse_hold = 1
            if event.button == 2:
                mouse_click = 2
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_hold = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = True
            else:
                key_press = pygame.key.name(event.key)

    if in_menu:
        menu()
    else:
        office()

    pygame.display.update()

    Clock.tick(60)
