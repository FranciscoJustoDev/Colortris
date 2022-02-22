import pygame as pg
import random as rdm
import sys
from os import path

from settings import *
from sprites import *
from computations import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.all_sprites = pg.sprite.Group()
        self.monster_sprites = pg.sprite.Group()
        self.menu_sprites = pg.sprite.Group()
        self.credit_sprites = pg.sprite.Group()
        self.load_data()

    def load_data(self):
        self.load_graphics()
        self.load_audio()

    def load_graphics(self):
        self.fonts_dir = path.join(path.dirname(__file__), 'assets/fonts')
        self.font_18 = pg.font.Font(path.join(self.fonts_dir, 'PixelatedPusab.ttf'), 18)
        self.font_24 = pg.font.Font(path.join(self.fonts_dir, 'PixelatedPusab.ttf'), 24)
        self.font_36 = pg.font.Font(path.join(self.fonts_dir, 'PixelatedPusab.ttf'), 36)
        self.font_text_18 = pg.font.Font(path.join(self.fonts_dir, 'Pixellari.ttf'), 18)
        self.font_text_24 = pg.font.Font(path.join(self.fonts_dir, 'Pixellari.ttf'), 24)
        self.font_text_36 = pg.font.Font(path.join(self.fonts_dir, 'Pixellari.ttf'), 36)

        self.level_dir = path.join(path.dirname(__file__), 'assets/sprites/level')
        
        self.slime_anim = []
        for n in range(0, 12):
            filename = 'monsters/slime/slime-{}.png'.format(n)
            img = pg.image.load(path.join(self.level_dir, filename))
            img.set_colorkey(BLACK)
            img_scaled = pg.transform.scale(img, (78, 78))
            self.slime_anim.append(img_scaled)
        
        self.ghost_anim = []
        for n in range(0, 12):
            filename = 'monsters/ghost/ghost-{}.png'.format(n)
            img = pg.image.load(path.join(self.level_dir, filename))
            img.set_colorkey(BLACK)
            img_scaled = pg.transform.scale(img, (78, 78))
            self.ghost_anim.append(img_scaled)
        
        self.bogo_anim = []
        for n in range(0, 12):
            filename = 'monsters/bogo/bogo-{}.png'.format(n)
            img = pg.image.load(path.join(self.level_dir, filename))
            img.set_colorkey(BLACK)
            img_scaled = pg.transform.scale(img, (78, 78))
            self.bogo_anim.append(img_scaled)
        
        self.vala_anim = []
        for n in range(0, 12):
            filename = 'monsters/vala/vala-{}.png'.format(n)
            img = pg.image.load(path.join(self.level_dir, filename))
            img.set_colorkey(BLACK)
            img_scaled = pg.transform.scale(img, (78, 78))
            self.vala_anim.append(img_scaled)

        self.level_anim = []
        for n in range(0, 12):
            filename = 'bg/level_bg-{}.png'.format(n)
            img = pg.image.load(path.join(self.level_dir, filename))
            img.set_colorkey(BLACK)
            img_scaled = pg.transform.scale(img, (64 * 8, 88 * 8))
            self.level_anim.append(img_scaled)

        self.start_dir = path.join(path.dirname(__file__), 'assets/sprites/startmenu')

        img = pg.image.load(path.join(self.start_dir, 'cursor/heart-0.png'))
        self.cursor_img = pg.transform.scale(img, (48, 48))

        self.mana_pool_anim = []
        for n in range(0, 31):
            filename = 'manapool/mana_pool-rot-{}.png'.format(n)
            img = pg.image.load(path.join(self.start_dir, filename))
            img.set_colorkey(BLACK)
            img_scaled = pg.transform.scale(img, (64 * 3, 88 * 3))
            self.mana_pool_anim.append(img_scaled)

    def load_audio(self):
        self.music_dir = path.join(path.dirname(__file__), "assets/audio/music")
        self.sfx_dir = path.join(path.dirname(__file__), "assets/audio/sfx")

        self.menu_music = path.join(self.music_dir, 'menu_track.wav')
        self.game_music = path.join(self.music_dir, 'level_track.wav')

        self.button_pressed_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'button-click.wav'))
        self.button_select1_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'button-select-1.wav'))
        self.button_select2_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'button-select-2.wav'))
        self.highscore_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'button-select-2.wav'))
        self.score_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'score.wav'))
        self.land_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'land.wav'))
        self.love_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'love.wav'))
        self.lose_sound = pg.mixer.Sound(path.join(self.sfx_dir, 'lose.wav'))

    def level_setup(self):
        self.all_sprites.empty()
        self.monster_sprites.empty()
        self.grid_data = grid_data_load()
        self.grid_map = grid_map_pop()
        self.spawn_column = GRID_WIDTH / 2 + (GRID_ORIGIN[0] - GRID_ORIGIN[0] / 2)
        self.no_monsters = True
        self.speed = 1
        self.level_last_update = pg.time.get_ticks()
        self.level_frame = 0
        pg.mixer.music.unload()
        pg.mixer.music.load(self.game_music)
        pg.mixer.music.play(-1)

    def level_run(self):
        # Game loop
        self.game_running = True
        while self.game_running:
            self.dt = self.clock.tick(FPS) / 1000
            self.level_events()
            self.level_update()
            self.level_draw()

    def quit(self):
        pg.quit()
        sys.exit()
    
    def level_update(self):
        self.all_sprites.update()
        self.spawn_monster()
        self.dwn_mov()
        self.update_grid_map()
        self.monster_logic()

    def draw_grid(self):
        # Visual aid for development
        for x in range(GRID_ORIGIN[0], GRID_WIDTH, CELL_SIZE):
            pg.draw.line(self.screen, WHITE, (x, GRID_ORIGIN[1]), (x, GRID_HEIGHT))
        pg.draw.line(self.screen, WHITE, (GRID_ORIGIN[0], GRID_HEIGHT), (GRID_WIDTH, GRID_HEIGHT))

        for y in range(GRID_ORIGIN[1], GRID_HEIGHT, CELL_SIZE):
            pg.draw.line(self.screen, WHITE, (GRID_ORIGIN[0], y), (GRID_WIDTH, y))
        pg.draw.line(self.screen, WHITE, (GRID_WIDTH, GRID_ORIGIN[1]), (GRID_WIDTH, GRID_HEIGHT))
    
    def level_draw(self):
        self.screen.fill(BLACK)
        self.draw_level()
        self.screen.blit(self.level_anim[self.level_frame], (0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    
    def draw_level(self):
        now = pg.time.get_ticks()
        if now - self.level_last_update > 800:
            self.level_last_update = now
            if self.level_frame > 10:
                self.level_frame = 0
            else:
                self.level_frame += 1

    def level_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    for monster in self.monster_sprites:
                        if monster.active:
                            for e in self.grid_data:
                                if e[0] == monster.sector:
                                    if monster.sector[0] > 0:
                                        if self.grid_map[monster.sector[1]][monster.sector[0] - 1] == 0:
                                            monster.rect.x -= CELL_SIZE
                                            self.spawn_column -= CELL_SIZE
                if event.key == pg.K_RIGHT:
                    for monster in self.monster_sprites:
                        if monster.active:
                            for e in self.grid_data:
                                if e[0] == monster.sector:
                                    if monster.sector[0] < N_COLS - 1:
                                        if self.grid_map[monster.sector[1]][monster.sector[0] + 1] == 0:
                                            monster.rect.x += CELL_SIZE
                                            self.spawn_column += CELL_SIZE
                if event.key == pg.K_DOWN:
                    for monster in self.monster_sprites:
                        if monster.active:
                            self.speed = 2

            if event.type == pg.KEYUP:
                if event.key == pg.K_DOWN:
                    for monster in self.monster_sprites:
                        if monster.active:
                            self.speed = 1
    
    def spawn_monster(self):
        monster_type = rdm.randint(1, 4)
        if monster_type == 1:
            anim = self.slime_anim
        elif monster_type == 2:
            anim = self.ghost_anim
        elif monster_type == 3:
            anim = self.bogo_anim
        else:
            anim = self.vala_anim
        
        if self.no_monsters:
            self.no_monsters = False
            self.monster = Monster(self.grid_data, self.spawn_column, monster_type, anim)
            self.monster_sprites.add(self.monster)
            self.all_sprites.add(self.monster)

        for monster in self.monster_sprites:
            if not(monster.active) and not(monster.locked) and not(monster.tracked):
                monster.locked = True
                self.monster = Monster(self.grid_data, self.spawn_column, monster_type, anim)
                self.monster_sprites.add(self.monster)
                self.all_sprites.add(self.monster)
    
    def dwn_mov(self):
        for monster in self.monster_sprites:
            if monster.active and not(monster.locked) and not(monster.tracked):
                if monster.sector[1] < N_ROWS - 1:
                    if self.grid_map[monster.sector[1] + 1][monster.sector[0]] != 0:
                        for e in self.grid_data:
                            if e[0] == monster.sector:
                                monster.rect.centery = e[4]
                                monster.active = False
                                pg.mixer.Sound.play(self.land_sound)
                if monster.active:
                    if monster.sector[1] < N_ROWS - 1:
                        monster.rect.y += SPEED * self.speed
                    else:
                        for e in self.grid_data:
                            if monster.sector == e[0]:
                                monster.rect.centery = e[4]
                                monster.active = False
                        pg.mixer.Sound.play(self.land_sound)

    def update_grid_map(self):
        for monster in self.monster_sprites:
            if not(monster.active) and monster.locked and not(monster.tracked):
                if monster.sector[1] == 0:
                    self.game_running = False
                else:
                    x = monster.sector[0]
                    y = monster.sector[1]
                    self.grid_map[y][x] = monster.type
                    monster.tracked = True
                    self.animation_manager()
    
    def monster_logic(self):
        hor = False
        ver = False
        hor_kill_queue = []
        ver_kill_queue = []
        # Check for basic match!!
        for monster in self.monster_sprites:
            if not(monster.active) and monster.locked and monster.tracked:
                if monster.sector[0] > 0 and monster.sector[0] < N_COLS - 1:
                    if self.grid_map[monster.sector[1]][monster.sector[0] + 1] == monster.type:
                        if self.grid_map[monster.sector[1]][monster.sector[0] - 1] == monster.type:
                            hor = True
                            hor_kill_queue = [(monster.sector[0] - 1, monster.sector[1]), (monster.sector[0], monster.sector[1]), (monster.sector[0] + 1, monster.sector[1])]
                if monster.sector[1] < N_ROWS - 1 and monster.sector[1] > 0:
                    if self.grid_map[monster.sector[1] + 1][monster.sector[0]] == monster.type:
                        if self.grid_map[monster.sector[1] - 1][monster.sector[0]] == monster.type:
                            ver = True
                            ver_kill_queue = [(monster.sector[0], monster.sector[1] - 1), (monster.sector[0], monster.sector[1]), (monster.sector[0], monster.sector[1] + 1)]
        
        # Check for additional matches!!
        if hor:
            for monster in self.monster_sprites:
                if monster.sector == hor_kill_queue[0]:
                    if monster.sector[0] > 0:
                        if self.grid_map[monster.sector[1]][monster.sector[0] - 1] == monster.type:
                            hor_kill_queue.append((monster.sector[0] - 1, monster.sector[1]))
                elif monster.sector == hor_kill_queue[2]:
                    if monster.sector[0] < N_COLS - 1:
                        if self.grid_map[monster.sector[1]][monster.sector[0] + 1] == monster.type:
                            hor_kill_queue.append((monster.sector[0] + 1, monster.sector[1]))
        if ver:
            for monster in self.monster_sprites:
                if monster.sector == ver_kill_queue[0]:
                    if monster.sector[1] > 0:
                        if self.grid_map[monster.sector[1] - 1][monster.sector[0]] == monster.type:
                            ver_kill_queue.append((monster.sector[0], monster.sector[1] - 1))
                elif monster.sector == ver_kill_queue[2]:
                    if monster.sector[1] < N_ROWS - 1:
                        if self.grid_map[monster.sector[1] + 1][monster.sector[0]] == monster.type:
                            ver_kill_queue.append((monster.sector[0], monster.sector[1] + 1))
        
        # Execute order 66... >:3
        for monster in self.monster_sprites:
                for k in hor_kill_queue:
                    if monster.sector == k:
                        monster.kill()
                        pg.mixer.Sound.stop(self.love_sound)
                        pg.mixer.Sound.play(self.score_sound)
                        self.grid_map[monster.sector[1]][monster.sector[0]] = 0

        for monster in self.monster_sprites:
                for k in ver_kill_queue:
                    if monster.sector == k:
                        monster.kill()
                        pg.mixer.Sound.stop(self.love_sound)
                        pg.mixer.Sound.play(self.score_sound)
                        self.grid_map[monster.sector[1]][monster.sector[0]] = 0

        # update floating sprites
        for monster in self.monster_sprites:
            if not(monster.active) and monster.locked and monster.tracked:
                if monster.sector[1] < N_ROWS - 1:
                    if self.grid_map[monster.sector[1] + 1][monster.sector[0]] == 0:
                        monster.tracked = False
                        monster.rect.y += CELL_SIZE
                        self.grid_map[monster.sector[1]][monster.sector[0]] = 0

    def animation_manager(self):
        for monster in self.monster_sprites:
            x = monster.sector[0]
            y = monster.sector[1]
            if monster.active:
                monster.init_frame = 0
            elif monster.tracked:
                if y == N_ROWS - 1:
                    # is grounded
                    if x == 0:
                        #left
                        if self.grid_map[y - 1][x] == 0 and self.grid_map[y][x + 1] == 0:
                            #alone
                            monster.init_frame = 3
                        else:
                            if self.grid_map[y - 1][x] == monster.type or self.grid_map[y][x + 1] == monster.type:
                                #in love
                                monster.init_frame = 9
                                if monster.love_sfx == True:
                                    pg.mixer.Sound.play(self.love_sound)
                                    monster.love_sfx = False
                            elif self.grid_map[y - 1][x] != monster.type and self.grid_map[y - 1][x] != 0:
                                #upset - squished
                                monster.init_frame = 6
                            else:
                                monster.init_frame = 0
                    elif x == N_COLS - 1:
                        #right
                        if self.grid_map[y - 1][x] == 0 and self.grid_map[y][x - 1] == 0:
                            #alone
                            monster.init_frame = 3
                        else:
                            if self.grid_map[y - 1][x] == monster.type or self.grid_map[y][x - 1] == monster.type:
                                #in love
                                monster.init_frame = 9
                                if monster.love_sfx == True:
                                    pg.mixer.Sound.play(self.love_sound)
                                    monster.love_sfx = False
                            elif self.grid_map[y - 1][x] != monster.type and self.grid_map[y - 1][x] != 0:
                                #upset - squished
                                monster.init_frame = 6
                            else:
                                monster.init_frame = 0
                    else:
                        #middle
                        if self.grid_map[y - 1][x] == 0 and self.grid_map[y][x - 1] == 0 and self.grid_map[y][x + 1] == 0:
                            #alone
                            monster.init_frame = 3
                        else:
                            if self.grid_map[y - 1][x] == monster.type or self.grid_map[y][x - 1] == monster.type or self.grid_map[y][x + 1] == monster.type:
                                #in love
                                monster.init_frame = 9
                                if monster.love_sfx == True:
                                    pg.mixer.Sound.play(self.love_sound)
                                    monster.love_sfx = False
                            elif self.grid_map[y - 1][x] != monster.type and self.grid_map[y - 1][x] != 0:
                                #upset - squished
                                monster.init_frame = 6
                            else:
                                monster.init_frame = 0
                else:
                    # Not grounded / Alone always false
                    if x == 0:
                        #left
                        if self.grid_map[y - 1][x] == monster.type or self.grid_map[y + 1][x] == monster.type or self.grid_map[y][x + 1] == monster.type:
                            #in love
                            monster.init_frame = 9
                            if monster.love_sfx == True:
                                pg.mixer.Sound.play(self.love_sound)
                                monster.love_sfx = False
                        elif self.grid_map[y - 1][x] != monster.type and self.grid_map[y - 1][x] != 0:
                            #upset
                            monster.init_frame = 6
                    elif x == N_COLS - 1:
                        #right
                        if self.grid_map[y - 1][x] == monster.type or self.grid_map[y + 1][x] == monster.type or self.grid_map[y][x - 1] == monster.type:
                            #in love
                            monster.init_frame = 9
                            if monster.love_sfx == True:
                                pg.mixer.Sound.play(self.love_sound)
                                monster.love_sfx = False
                        elif self.grid_map[y - 1][x] != monster.type and self.grid_map[y - 1][x] != 0:
                            #upset
                            monster.init_frame = 6
                    else:
                        #middle
                        if self.grid_map[y - 1][x] == monster.type or self.grid_map[y + 1][x] == monster.type or self.grid_map[y][x + 1] == monster.type or self.grid_map[y][x - 1] == monster.type:
                            #in love
                            monster.init_frame = 9
                            if monster.love_sfx == True:
                                pg.mixer.Sound.play(self.love_sound)
                                monster.love_sfx = False
                        elif self.grid_map[y - 1][x] != monster.type and self.grid_map[y - 1][x] != 0:
                            #squished
                            monster.init_frame = 6

    def start_menu_setup(self):
        self.start_menu_last_update = pg.time.get_ticks()
        self.all_sprites.empty()
        self.menu_sprites.empty()
        self.start_text = Text(self.font_36, "Start", GREEN, (WIDTH/2, HEIGHT/2))
        self.credits_text = Text(self.font_36, "Credits", CYAN, (WIDTH/2, HEIGHT/2 + 100))
        self.exit_text = Text(self.font_36, "Exit", MAGENTA, (WIDTH/2, HEIGHT/2 + 200))
        self.menu_sprites.add(self.start_text)
        self.menu_sprites.add(self.credits_text)
        self.menu_sprites.add(self.exit_text)

        self.credits_info = {
            'h1' : [self.font_36, "Art and Code:", MAGENTA, (WIDTH/2, 100)],
            'h1_name' : [self.font_text_24, "Francisco Justo", WHITE, (WIDTH/2, 140)],
            'h1_email' : [self.font_text_24, "franciscojusto.dev@gmail.com", WHITE, (WIDTH/2, 170)],
            'h1_itch' : [self.font_text_24, "https://franciscojustodev.itch.io/", WHITE, (WIDTH/2, 200)],
            'h2' : [self.font_36, "Sound Design:", YELLOW, (WIDTH/2, 260)],
            'h2_name' : [self.font_text_24, "Nelson Milheiro", WHITE, (WIDTH/2, 300)],
            'h2_email' : [self.font_text_24, "nelsonfcmilheiro@gmail.com", WHITE, (WIDTH/2, 330)],
            'h2_itch' : [self.font_text_24, "https://mikapuccino.itch.io/", WHITE, (WIDTH/2, 360)],
            'h3' : [self.font_text_24, "Pixellari font:", WHITE, (WIDTH/2, 500)],
            'h3_name' : [self.font_text_24, "Zacchary Dempsey-Plante", WHITE, (WIDTH/2, 524)],
            'h4' : [self.font_24, "Pixelated Pusab font:", WHITE, (WIDTH/2, 550)],
            'h4_name': [self.font_24, "JumperBox Games", WHITE, (WIDTH/2, 574)]
        }

        for key, value in self.credits_info.items():
            t = Text(value[0], value[1], value[2], value[3])
            self.credit_sprites.add(t)

        self.mana_pool_frame = 0
        self.button_current = 0
        self.screen_active = 0
        pg.mixer.Sound.stop(self.lose_sound)
        pg.mixer.music.load(self.menu_music)
        pg.mixer.music.play(-1)

    def start_menu_run(self):
        self.start_menu_running = True
        while self.start_menu_running:
            if self.screen_active == 0:
                self.start_menu_events()
                self.start_menu_update()
                self.start_menu_draw()
            elif self.screen_active == 1:
                self.start_menu_credits()
    
    def start_menu_events(self):
        select_n = rdm.randint(1, 2)
        if select_n == 1:
            button_sound = self.button_select1_sound
        else:
            button_sound = self.button_select2_sound

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            
            if event.type == pg.KEYDOWN:
                # Perform button action
                if event.key == pg.K_RETURN:
                    if self.button_current == 0:
                        self.start_menu_running = False
                    elif self.button_current == 1:
                        pg.mixer.Sound.play(self.button_pressed_sound)
                        self.screen_active = 1
                    else:
                        self.quit()
                
                # change button
                if event.key == pg.K_UP:
                    if self.button_current == 0:
                        self.button_current = 2
                        pg.mixer.Sound.play(button_sound)
                    elif self.button_current == 1:
                        self.button_current = 0
                        pg.mixer.Sound.play(button_sound)
                    else:
                        self.button_current = 1
                        pg.mixer.Sound.play(button_sound)
                
                if event.key == pg.K_DOWN:
                    if self.button_current == 0:
                        self.button_current = 1
                        pg.mixer.Sound.play(button_sound)
                    elif self.button_current == 1:
                        self.button_current = 2
                        pg.mixer.Sound.play(button_sound)
                    else:
                        self.button_current = 0
                        pg.mixer.Sound.play(button_sound)

    def start_menu_update(self):
        pass

    def start_menu_draw(self):
        self.screen.fill(BLACK)
        if self.button_current == 0:
            self.screen.blit(self.cursor_img, (158, HEIGHT/2 - 20))
        elif self.button_current == 1:
            self.screen.blit(self.cursor_img, (142, HEIGHT/2 + 100))
        else:
            self.screen.blit(self.cursor_img, (168, HEIGHT/2 + 200))

        now = pg.time.get_ticks()
        if now - self.start_menu_last_update > 350:
            self.start_menu_last_update = now
            if self.mana_pool_frame > 29:
                self.mana_pool_frame = 0
            else:
                self.mana_pool_frame += 1
        self.screen.blit(self.mana_pool_anim[self.mana_pool_frame], (162, 32))
        self.menu_sprites.draw(self.screen)
        pg.display.flip()

    def start_menu_credits(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            
            if event.type == pg.KEYDOWN:
                # Perform button action
                if event.key == pg.K_RETURN:
                    self.screen_active = 0

        self.screen.fill(BLACK)
        self.credit_sprites.draw(self.screen)
        pg.display.flip()

    def go_menu_setup(self):
        pg.mixer.music.unload()
        pg.mixer.Sound.play(self.lose_sound)

    def go_menu_run(self):
        self.go_menu_running = True
        while self.go_menu_running:
            self.go_menu_events()
            self.go_menu_update()
            self.go_menu_draw()
    
    def go_menu_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.go_menu_running = False

    def go_menu_update(self):
        pass

    def go_menu_draw(self):
        self.screen.fill(RED)
        pg.display.flip()

g = Game()
while True:
    g.start_menu_setup()
    g.start_menu_run()
    g.level_setup()
    g.level_run()
    g.go_menu_setup()
    g.go_menu_run()