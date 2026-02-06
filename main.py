import time
import random

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

with open("assets/dat.json", "r") as file:
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
        time.sleep(0.5)

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

day_stage = pygame.transform.scale(pygame.image.load("assets/day/stage.png"), (1100, 700))
floor_better = pygame.transform.scale(pygame.image.load("assets/day/floor_better.png"), (1100, 700))
floor_default = pygame.transform.scale(pygame.image.load("assets/day/floor_default.png"), (1100, 700))

day_Bunny = pygame.transform.scale(pygame.image.load("assets/day/Bunny.png"), (1100, 700))
day_Fox = pygame.transform.scale(pygame.image.load("assets/day/Fox.png"), (1100, 700))
day_Dog = pygame.transform.scale(pygame.image.load("assets/day/Dog.png"), (1100, 700))

tables_2 = pygame.transform.scale(pygame.image.load("assets/day/tables_2.png"), (1100, 700))
tables_3 = pygame.transform.scale(pygame.image.load("assets/day/tables_3.png"), (1100, 700))
tables_4 = pygame.transform.scale(pygame.image.load("assets/day/tables_4.png"), (1100, 700))
tables_5 = pygame.transform.scale(pygame.image.load("assets/day/tables_5.png"), (1100, 700))
tables_6 = pygame.transform.scale(pygame.image.load("assets/day/tables_6.png"), (1100, 700))

shop_background = pygame.transform.scale(pygame.image.load("assets/upgrades_shop/background.png"), (1100, 700))
shop_icon = pygame.transform.scale(pygame.image.load("assets/upgrades_shop/icon.png"), (75, 75))
shop_icon_rect = pygame.rect.Rect((1000, 600, 75, 75))

Bunny_door = pygame.transform.scale(pygame.image.load("assets/mascots/bunny.png"), (1100, 700))
Fox_door = pygame.transform.scale(pygame.image.load("assets/mascots/fox.png"), (1100, 700))

standart_font = pygame.font.Font("assets/font.ttf", 60)

pygame.mixer.init()

computer_sound = pygame.mixer.Sound("assets/sound/computer.mp3")
menu_click_sound = pygame.mixer.Sound("assets/sound/menu_click.wav")
buy_sound = pygame.mixer.Sound("assets/sound/buy.wav")
clockAlarm_sound = pygame.mixer.Sound("assets/sound/clockAlarm.mp3")
door_sound = pygame.mixer.Sound("assets/sound/door.mp3")
window_sound = pygame.mixer.Sound("assets/sound/window.mp3")
lightSwitch_sound = pygame.mixer.Sound("assets/sound/lightSwitch.mp3")
jumpscare_sound = pygame.mixer.Sound("assets/sound/jumpscare.mp3")
jumpscare_sound.set_volume(0.7)
footstep_sound = pygame.mixer.Sound("assets/sound/footstep.mp3")
footstep_sound.set_volume(0.7)

office_ambience = "assets/sound/office_ambience.mp3"
pizzeria_music = "assets/sound/pizzeria_music.mp3"

key_press = ""
key_hold = ""

mouse_pos = (0, 0)
mouse_click = 0
mouse_hold = 0

class ShopButton:
    def __init__(self, pos, text):
        self.x = pos[0]
        self.y = pos[1]
        self.w = 500
        self.h = 150
        self.text = text
        self.rect = pygame.rect.Rect((self.x, self.y, self.w, self.h))
        self.font = pygame.font.Font("assets/font.ttf", 40)

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(self.x+self.w/2, self.y+self.h/2))
        self.text_rect.x = self.x+15

        self.sold = False

    def update(self):
        if self.sold:
            pygame.draw.rect(window, (100, 100, 100), self.rect, 8)
            return False

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, (70, 70, 200), self.rect)
            pygame.draw.rect(window, (200, 220, 230), self.rect, 8)
            window.blit(self.text_surface, self.text_rect)

            if mouse_click == 1:
                return True
        else:
            pygame.draw.rect(window, (70, 70, 160), self.rect)
            pygame.draw.rect(window, (200, 220, 230), self.rect, 8)
            window.blit(self.text_surface, self.text_rect)

        return False

class MenuButton:
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
        self.text_rect.x = self.x+10
    
    def update(self):
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(window, (50, 50, 50), self.rect)
            if mouse_click == 1:
                menu_click_sound.play()
                return True
        
        window.blit(self.text_surface, self.text_rect)

        return False

if language == "eng":
    Play_button = MenuButton((30, 300, 200, 60), "Play")
    Language_button = MenuButton((30, 380, 200, 60), "Ukr")
    Exit_button = MenuButton((30, 460, 200, 60), "Exit")

    NewGame_button = MenuButton((30, 300, 200, 60), "New")
    ContinueGame_button = MenuButton((30, 380, 200, 60), "Cont.")
    Back_button = MenuButton((30, 460, 200, 60), "Back")

    Table_button = ShopButton((25, 100), "Buy a table - 150$")
    Floor_button = ShopButton((550, 100), "Floor upgrade - 400$")

    Bunny_button = ShopButton((25, 350), "Bunny - 400$")
    Fox_button = ShopButton((550, 350), "Fox - 325$")
    Dog_button = ShopButton((25, 525), "Dog - 325$")

    FinishDay_button = MenuButton((10, 630, 200, 60), "Finish")

elif language == "ukr":
    Play_button = MenuButton((30, 300, 200, 60), "Грати")
    Language_button = MenuButton((30, 380, 200, 60), "Англ.")
    Exit_button = MenuButton((30, 460, 200, 60), "Вийти")

    NewGame_button = MenuButton((30, 300, 200, 60), "Нова")
    ContinueGame_button = MenuButton((30, 380, 200, 60), "Далі")
    Back_button = MenuButton((30, 460, 200, 60), "Назад")

    Table_button = ShopButton((25, 100), "Купити стіл - 150$")
    Floor_button = ShopButton((550, 100), "Нова підлога - 400$")

    Bunny_button = ShopButton((25, 350), "Заєць - 400$")
    Fox_button = ShopButton((550, 350), "Лисиця - 325$")
    Dog_button = ShopButton((25, 525), "Собака - 325$")

    FinishDay_button = MenuButton((10, 630, 200, 60), "Далі")

music_list = [(office_ambience, 1), (pizzeria_music, 0.3), (pizzeria_music, 0.1), (pizzeria_music, 0.3)]
def music_switch(new_game_state):
    pygame.mixer.music.stop()
    computer_sound.stop()
    pygame.mixer.music.load(music_list[new_game_state][0])
    pygame.mixer.music.set_volume(music_list[new_game_state][1])
    pygame.mixer.music.play(-1)

BuyBunny = settings["BuyBunny"]
BuyFox = settings["BuyFox"]
BuyDog = settings["BuyDog"]

in_menu = True

game_state = 0

menu_state = 0

current_day = 1

def menu():
    global language, money, current_floor, current_tables, current_day
    global in_menu, run, game_state, menu_state

    if menu_state == 0:
        draw_bg_screen()

        pygame.draw.rect(window, (100, 100, 100), (0, 0, window_w/4, window_h))

        pygame.mixer.music.stop()

        if Play_button.update():
            menu_state = 1

        if Language_button.update():
            import sys
            import subprocess

            if language == "eng":
                language = "ukr"
            else:
                language = "eng"

            data = {
                "language": language,
                "money": money,
                "current_floor": current_floor,
                "current_tables": current_tables,
                "current_day": current_day,
                "BuyBunny": BuyBunny,
                "BuyFox": BuyFox,
                "BuyDog": BuyDog
            }
            with open("assets/dat.json", "w") as file:
                file.write(json.dumps(data, indent=4))

            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit()

        if Exit_button.update():
            run = False

    elif menu_state == 1:
        window.blit(floor_default, (0, 0))
        window.blit(day_stage, (0, 0))
        window.blit(shade, (0, 50))

        pygame.draw.rect(window, (100, 100, 100), (0, 0, window_w/4, window_h))

        pygame.mixer.music.stop()

        if NewGame_button.update():
            in_menu = False
            game_state = 1
            music_switch(game_state)

            data = {
                "language": language,
                "money": 200,
                "current_floor": 0,
                "current_tables": 2,
                "current_day": 1,
                "BuyBunny": 0,
                "BuyFox": 0,
                "BuyDog": 0
            }
            with open("assets/dat.json", "w") as file:
                file.write(json.dumps(data, indent=4))

            LoadFunc()
        
        if ContinueGame_button.update():
            in_menu = False
            game_state = 1
            music_switch(game_state)
            LoadFunc()

            recou()

        if Back_button.update():
            menu_state = 0

def build_day_surface():
    surface = pygame.Surface((1100, 700))
    if current_floor:
        surface.blit(floor_better, (0, 0))
    else:
        surface.blit(floor_default, (0, 0))
    surface.blit(day_stage, (0, 0))
    surface.blit(tables_list[current_tables-2], (0, 0))

    if BuyBunny:
        surface.blit(day_Bunny, (0, 0))
    if BuyFox:
        surface.blit(day_Fox, (0, 0))
    if BuyDog:
        surface.blit(day_Dog, (0, 0))

    return surface

money = 200

current_floor = 0
current_tables = 2
tables_list = [tables_2, tables_3, tables_4, tables_5, tables_6]

def day():
    global game_state

    window.blit(day_surface, (0, 0))

    window.blit(shop_icon, shop_icon_rect)
    if shop_icon_rect.collidepoint(mouse_pos):
        if mouse_click == 1:
            menu_click_sound.play()
            game_state = 2
            pygame.mixer.music.set_volume(0.1)
    
    if FinishDay_button.update():
        data = {
            "language": language,
            "money": money,
            "current_floor": current_floor,
            "current_tables": current_tables,
            "current_day": current_day,
            "BuyBunny": BuyBunny,
            "BuyFox": BuyFox,
            "BuyDog": BuyDog
        }
        with open("assets/dat.json", "w") as file:
            file.write(json.dumps(data, indent=4))

        game_state = 0
        if language == "eng":
            transition("10:00 PM")
        else:
            transition("22:00")
        music_switch(game_state)

        Load_MascotValues()

    if language == "eng":
        draw_text(f"Day: {current_day}", standart_font, (950, 50))
    else:
        draw_text(f"День: {current_day}", standart_font, (950, 50))
    
    if key_press == "ESCAPE":
        global in_menu
        in_menu = True
        pygame.mixer.music.stop()
        menu_click_sound.play()

def draw_text(text, text_font, text_center, text_colour=(0, 0, 0)):
    text_surface = text_font.render(text, True, text_colour)
    text_rect = text_surface.get_rect(center=(text_center[0], text_center[1]))

    window.blit(text_surface, text_rect)

def upgrades_shop():
    global current_floor, current_tables, money, BuyBunny, BuyFox, BuyDog

    window.blit(shop_background, (0, 0))

    draw_text(f"{money}$", standart_font, (1000, 50))
    if language == "eng":
        draw_text("Interior", standart_font, (550, 50))
        draw_text("Repair mascots", standart_font, (550, 300))
    else:
        draw_text("Інтер'єр", standart_font, (550, 50))
        draw_text("Ремонт маскотів", standart_font, (550, 300))

    if key_press == "ESCAPE":
        global game_state
        game_state = 1
        pygame.mixer.music.set_volume(0.3)
        menu_click_sound.play()

        global day_surface
        day_surface = build_day_surface()
    
    if Table_button.update():
        if money >= 150:
            money -= 150

            current_tables += 1
            buy_sound.play()

    if current_tables == 4 and not current_floor:
        Table_button.sold = True
    elif current_tables == 6:
        Table_button.sold = True
    else:
        Table_button.sold = False

    if Floor_button.update():
        if money >= 400:
            Floor_button.sold = True
            money -= 400

            current_floor = 1
            buy_sound.play()
    

    if Bunny_button.update():
        if money >= 400:
            Bunny_button.sold = True
            money -= 400

            BuyBunny = True
            buy_sound.play()
    
    if Fox_button.update():
        if money >= 325:
            Fox_button.sold = True
            money -= 325

            BuyFox = True
            buy_sound.play()

    if Dog_button.update():
        if money >= 325:
            Dog_button.sold = True
            money -= 325

            BuyDog = True
            buy_sound.play()

def transition(text, text2="NO TEXT"):
    pygame.mixer.music.stop()
    computer_sound.stop()

    text_surface = standart_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(550, 350))

    clockAlarm_sound.play()

    for x in range(3):
        window.fill((0, 0, 0))
        if x == 1:
            window.blit(text_surface, text_rect)
        if text2 != "NO TEXT" and x==2:
            text_surface = standart_font.render(text2, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(550, 350))
            window.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(2)

def Load_MascotValues():
    global Bunny_level, Fox_level, Dog_level

    if current_day == 1:
        Bunny_level = 2
        Fox_level = 0
        Dog_level = 0

    elif current_day == 2:
        Bunny_level = 3
        Fox_level = 2
        Dog_level = 0

    elif current_day == 3:
        Bunny_level = 4
        Fox_level = 3
        Dog_level = 3

    elif current_day == 4:
        Bunny_level = 4
        Fox_level = 4
        Dog_level = 4
    
    elif current_day == 5:
        Bunny_level = 5
        Fox_level = 5
        Dog_level = 6
    
    elif current_day == 6:
        Bunny_level = 7
        Fox_level = 6
        Dog_level = 7
    
    elif current_day == 7:
        Bunny_level = 8
        Fox_level = 8
        Dog_level = 8

jumpscare = 0

Bunny_pos = 0
Bunny_level = 0
Fox_pos = 0
Fox_level = 0
Dog_pos = 0
Dog_level = 0

def BunnyMascot():
    global Bunny_pos, jumpscare
    
    local_level = 0
    if Bunny_level > 0:
        local_level = Bunny_level + computer_status*2

    if local_level >= random.randint(1, 10):
        Bunny_pos += 1
        if Fox_pos == 2 or Dog_pos == 2:
            Bunny_pos = 1
        if Bunny_pos == 3:
            if not door_status:
                jumpscare = 1
            Bunny_pos = 2
    
    if door_status:
        Bunny_pos = 0
        mascot_leave()

def FoxMascot():
    global Fox_pos, jumpscare
    
    local_level = 0
    if Fox_level > 0:
        local_level = Fox_level + computer_status*2

    if local_level >= random.randint(1, 10):
        Fox_pos += 1
        if Bunny_pos == 2 or Dog_pos == 2:
            Fox_pos = 1
        if Fox_pos == 3:
            if light_status:
                jumpscare = 1
            Fox_pos = 2
    
    if not light_status:
        Fox_pos = 0
        mascot_leave()

def DogMascot():
    global Dog_pos, jumpscare
    
    local_level = 0
    if Dog_level > 0:
        local_level = Dog_level + computer_status*2

    if local_level >= random.randint(1, 10):
        Dog_pos += 1
        if Bunny_pos == 2 or Fox_pos == 2:
            Dog_pos = 1
        if Dog_pos == 2:
            footstep_sound.play(loops=1)
        if Dog_pos == 3:
            if not window_status:
                jumpscare = 1
            Dog_pos = 2

    if window_status:
        Dog_pos = 0
        mascot_leave()

mascot_timer = pygame.time.get_ticks()

def UpdateMascots():
    global mascot_timer
    if pygame.time.get_ticks() - mascot_timer > random.randint(6, 9)*1000:
        mascot_timer = pygame.time.get_ticks()
        BunnyMascot()
        FoxMascot()
        DogMascot()

def mascot_leave():
    window.fill((0, 0, 0))
    pygame.display.update()
    time.sleep(0.1)

def update_and_save():
    global money

    CountMascots()

    money += current_floor*25 + current_tables*50 + mascot_count*25

    data = {
        "language": language,
        "money": money,
        "current_floor": current_floor,
        "current_tables": current_tables,
        "current_day": current_day,
        "BuyBunny": BuyBunny,
        "BuyFox": BuyFox,
        "BuyDog": BuyDog
    }
    with open("assets/dat.json", "w") as file:
        file.write(json.dumps(data, indent=4))

looking = 0
computer_status = 0
door_status = 0
light_status = 1
window_status = 0

font = pygame.font.Font("assets/font.ttf", 30)
boot_time = "None"
night_percent = 0
previous_percent = night_percent

def office():
    global looking, computer_status, door_status, light_status, window_status, boot_time, night_percent, previous_percent

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
            
            if door_rect.collidepoint(mouse_pos) and mouse_click == 1:
                door_sound.play()
        else:
            window.fill((0, 0, 0))

        window.blit(light_switch, light_switch_rect)
        if light_switch_rect.collidepoint(mouse_pos) and mouse_click == 1:
            light_status = not light_status
            lightSwitch_sound.play()

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

            night_percent = int((pygame.time.get_ticks() - boot_time)/800+previous_percent)

            if language == "eng":
                text = font.render(f"Working: {night_percent}%", True, (255, 255, 255))
            else:
                text = font.render(f"Робота: {night_percent}%", True, (255, 255, 255))
            text_rect = text.get_rect(center=(550, 425))

            window.blit(text, text_rect)

            if night_percent >= 100:
                global game_state, current_day

                computer_status = 0
                boot_time = "None"
                night_percent = 0
                previous_percent = night_percent
                current_day += 1

                update_and_save()

                game_state = 1
                if language == "eng":
                    transition("12:00 AM", f"Day {current_day}")
                else:
                    transition("00:00", f"День {current_day}")
                music_switch(game_state)

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
        
        if window_rect.collidepoint(mouse_pos) and mouse_click == 1:
            window_sound.play()

    global jumpscare
    if jumpscare:
        computer_sound.stop()
        jumpscare_sound.play()
        jumpscare = 0

        looking = 0
        computer_status = 0
        door_status = 0
        light_status = 1
        window_status = 0

        global Bunny_pos, Fox_pos, Dog_pos

        Bunny_pos = 0
        Fox_pos = 0
        Dog_pos = 0

        boot_time = "None"
        night_percent = 0
        previous_percent = night_percent

        window.fill((0, 0, 0))
        pygame.display.update()
        time.sleep(4)

        if language == "eng":
            transition("10:00 PM")
        else:
            transition("22:00")
        music_switch(game_state)

    UpdateMascots()

    if looking == -1 and not door_status:
        if Bunny_pos == 2:
            window.blit(Bunny_door, (0, 0))
        if Fox_pos == 2:
            window.blit(Fox_door, (0, 0))

    window.blit(shade, (0, 50))

    if not door_status and light_status and not window_status and not computer_status:
        if key_press == "a":
            if looking > -1:
                looking -= 1
        if key_press == "d":
            if looking < 1:
                looking += 1

def LoadFunc():
    global settings, money, current_floor, current_tables, current_day, BuyBunny, BuyFox, BuyDog
    with open("assets/dat.json", "r") as file:
        settings = json.load(file)
    money = settings["money"]
    current_floor = settings["current_floor"]
    current_tables = settings["current_tables"]
    current_day = settings["current_day"]
    BuyBunny = settings["BuyBunny"]
    BuyFox = settings["BuyFox"]
    BuyDog = settings["BuyDog"]

mascot_count = 0

def CountMascots():
    global mascot_count
    if BuyBunny: mascot_count += 1
    if BuyFox: mascot_count += 1
    if BuyDog: mascot_count += 1

day_surface = build_day_surface()

def recou():
    if current_floor: Floor_button.sold = True
    else: Floor_button.sold = False

    if BuyBunny: Bunny_button.sold = True
    else: Bunny_button.sold = False

    if BuyFox: Fox_button.sold = True
    else: Fox_button.sold = False

    if BuyDog: Dog_button.sold = True
    else: Dog_button.sold = False

    global day_surface
    day_surface = build_day_surface()

LoadFunc()

recou()

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
                key_press = "ESCAPE"
            else:
                key_press = pygame.key.name(event.key)

    if in_menu:
        menu()
    elif game_state == 0:
        office()
    elif game_state == 1:    
        day()
    elif game_state == 2:
        upgrades_shop()

    pygame.display.update()

    Clock.tick(60)
