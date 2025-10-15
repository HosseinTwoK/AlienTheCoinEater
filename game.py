from settings import *


class Game():
    def __init__(self):
        pygame.init()
        
        self.game_surface = pygame.display.set_mode(SC_SIZE)
        pygame.display.set_caption(TITLE_MENU)
        # icon 
        icon = pygame.image.load(path.join("assets","icon","alien.ico"))
        pygame.display.set_icon(icon)
        
        self.clock = pygame.time.Clock()
        

        self.running = True
        self.rendering = False
        
        self.show_intro = False
        self.pause = False
        self.game_over = False
        
        # game control variables
        self.player_score = 0
        self.player_lives = PLAYER_LIVES
        self.player_velocity = PLAYER_STARTING_VELOCITY
        self.coin_velocity = COIN_STARTING_VELOCITY
        
        
        # animation control variables
        self.ani_frame_index_bg = 0     # which frame we are on
        self.ani_frame_time_bg = 100  # ms per frame
        self.ani_last_update_bg = pygame.time.get_ticks()
        
        self.ani_frame_index_player = 0
        self.ani_frame_time_player = 300
        self.ani_last_update_player = pygame.time.get_ticks()
        
        
        self.load_assets()
        
 
    def load_assets(self):
        pygame.mixer.music.load(path.join("assets","sounds","game-bg.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1,0.0)
        
        # sound effects
        self.sound_eat = pygame.mixer.Sound(path.join("assets","sounds","eat.wav"))
        self.sound_eat.set_volume(0.4)
        self.sound_missed = pygame.mixer.Sound(path.join("assets","sounds","failed.wav"))
        self.sound_missed.set_volume(0.1)
        self.sound_gameover = pygame.mixer.Sound(path.join("assets","sounds","game-over.wav"))
        
        # background 
        self.frames_background = [pygame.image.load(path.join("assets", "sky", "resized", f"sky{f}.png")) for f in range(11)]
        
        # player
        self.frames_player = [pygame.image.load(path.join("assets","alien",f"alien{f}.png")) for f in range(4)]
        self.image_player = self.frames_player[0]
        self.player_rect = self.image_player.get_rect()
        self.player_rect.topleft = (8,64)
            
        self.image_coin = pygame.image.load(path.join("assets","sprites","coin.png"))
        self.rect_coin = self.image_coin.get_rect()
        
        # coin
        self.image_coin = pygame.image.load(path.join("assets","sprites","coin.png"))
        self.coin_rect = self.image_coin.get_rect()
        self.coin_rect.x = SC_WIDTH + BUFFER_DISTACNE
        self.coin_rect.y = randint(54,SC_HEIGHT- self.coin_rect.height-4) 
        
        # fonts
        self.FONT_LARGE = pygame.font.Font(path.join("assets","fonts","PixeloidSans.ttf"),64)
        self.FONT_MEDIUM = pygame.font.Font(path.join("assets","fonts","PixeloidSans.ttf"),32)
        self.FONT_SMALL = pygame.font.Font(path.join("assets","fonts","PixeloidSans.ttf"),16)
        
        # texts
        self.text_AlienTheCoinEater = self.FONT_LARGE.render("AlienTheCoinEater",True,YELLOW)
        self.text_AlienTheCoinEater_rect = self.text_AlienTheCoinEater.get_rect()
        self.text_AlienTheCoinEater_rect.center = (CENTER_WIDTH, CENTER_HEIGHT)
        
        # self.text_Score = self.FONT_MEDIUM.render(f"Score: {self.player_score}", True, WHITE)
        # self.text_Score_rect = self.text_Score.get_rect()
        # self.text_Score_rect.topleft = (8,8)
        
        self.lives_txt = "* * * * *"
        # self.text_Lives = self.FONT_MEDIUM.render(self.lives_txt, True, WHITE)
        # self.text_Lives_rect = self.text_Lives.get_rect()
        # self.text_Lives_rect.topright = (SC_WIDTH-8,16)
        
        self.text_GameOver = self.FONT_LARGE.render("Game Over",  True, RED)
        self.text_GameOver_rect = self.text_GameOver.get_rect()
        self.text_GameOver_rect.center = (CENTER_WIDTH, CENTER_HEIGHT)
        
        self.text_PAUSE = self.FONT_LARGE.render("PAUSE", True, YELLOW)
        self.text_PAUSE_rect = self.text_PAUSE.get_rect()
        self.text_PAUSE_rect.bottomright = (SC_WIDTH - 8, SC_HEIGHT - 8 )
        
        self.text_GotoMenu = self.FONT_SMALL.render("Press \"M\" to go to Main Menu", True, YELLOW)
        self.text_GotoMenu_rect = self.text_GotoMenu.get_rect()
        self.text_GotoMenu_rect.center = (CENTER_WIDTH, CENTER_HEIGHT + 50)
        
        self.text_Continue = self.FONT_SMALL.render("Press \"C\" to Start another Round", True, RED)
        self.text_Continue_rect = self.text_Continue.get_rect()
        self.text_Continue_rect.center = self.text_GotoMenu_rect.center
        self.text_Continue_rect.y += 28
        
    def animation_player(self):
        # player (alien) ani
        now = pygame.time.get_ticks()
        if now - self.ani_last_update_player > self.ani_frame_time_player:
            self.ani_last_update_player = now
            self.ani_frame_index_player = (self.ani_frame_index_player +1) % len(self.frames_player)
        
    
    def animation_background(self):
        # background ani
        now = pygame.time.get_ticks()
        if now - self.ani_last_update_bg > self.ani_frame_time_bg:
            self.ani_last_update_bg = now
            self.ani_frame_index_bg = (self.ani_frame_index_bg +1) % len(self.frames_background) # always return numbers between 0 and list_length
    
    
    def coin_controll(self):     
        self.coin_rect.x -= self.coin_velocity
        if self.coin_rect.x <= 0:
            self.coin_rect.x = SC_WIDTH + BUFFER_DISTACNE
            self.coin_rect.y = randint(54,SC_HEIGHT- self.coin_rect.height-4) 
            
            self.player_lives -= 1
            
            match self.player_lives:
                case 4:
                    self.lives_txt = "* * * *"
                case 3:
                    self.lives_txt = "* * *"
                case 2:
                    self.lives_txt = "* *"
                case 1:
                    self.lives_txt = "*"
                case 0:
                    self.lives_txt = ""
                    self.game_over = True
                    self.sound_gameover.play()
        
            self.sound_missed.play()
                    
        self.game_surface.blit(self.image_coin, self.coin_rect)
        
        self.text_Lives = self.FONT_MEDIUM.render(self.lives_txt, True, WHITE)
        self.text_Lives_rect = self.text_Lives.get_rect()
        self.text_Lives_rect.topright = (SC_WIDTH-8,16)
           
        if self.player_rect.colliderect(self.coin_rect):
            self.player_score += 1
            self.sound_eat.play()
            self.coin_rect.x = SC_WIDTH + BUFFER_DISTACNE
            self.coin_rect.y = randint(54,SC_HEIGHT- self.coin_rect.height-4) 
            self.coin_velocity += COIN_ACCELERATION
            self.player_velocity += PLAYER_ACCELERATION

            
        self.text_Score = self.FONT_MEDIUM.render(f"Score: {self.player_score}", True, WHITE)
        self.text_Score_rect = self.text_Score.get_rect()
        self.text_Score_rect.topleft = (8,8)
                
        
    def intro(self):
        show_time = pygame.time.get_ticks() + 2000
        while pygame.time.get_ticks() <= show_time:
            self.game_surface.blit(self.text_AlienTheCoinEater,self.text_AlienTheCoinEater_rect)
            pygame.display.update()
        
    
    def render(self):
        self.animation_background()
        current_background = self.frames_background[self.ani_frame_index_bg] # because we are adding float speed
        self.game_surface.blit(current_background,(0,16))
        
        self.animation_player()
        self.image_player = self.frames_player[self.ani_frame_index_player]
        self.game_surface.blit(self.image_player, self.player_rect)
        # pygame.draw.rect(self.game_surface, GREEN, self.player_rect, 1) # player collision
        
        self.coin_controll()
        # pygame.draw.rect(self.game_surface, GREEN, self.coin_rect, 1) # coin collision
        
        
        # UI
        pygame.draw.rect(self.game_surface, DARK_BLUE, ((0,0),(SC_WIDTH,54))) 
        self.game_surface.blit(self.text_Score, self.text_Score_rect)
        self.game_surface.blit(self.text_Lives, self.text_Lives_rect)
        # TODO texts
        # self.game_surface.blit(self.text_GameOver, self.text_GameOver_rect)
        # self.game_surface.blit(self.text_GotoMenu, self.text_GotoMenu_rect)
        # self.game_surface.blit(self.text_PAUSE, self.text_PAUSE_rect)

     
    
        pygame.display.update()
        
    def controller(self):
        keys = pygame.key.get_pressed()
        if keys[K_w] and self.player_rect.y > 56:
            self.player_rect.y -= self.player_velocity
        if keys[K_s] and self.player_rect.y < (SC_HEIGHT-self.player_rect.height):
            self.player_rect.y += self.player_velocity
        if keys[K_a] and self.player_rect.x > 0:
            self.player_rect.x -= self.player_velocity
        if keys[K_d] and self.player_rect.x < (SC_WIDTH-self.player_rect.width):
            self.player_rect.x += self.player_velocity
    
    
    def pause_surface(self):
        pause_surface = pygame.Surface(SC_SIZE)
        pause_surface.fill(YELLOW)
        pause_surface.set_alpha(1)
        self.game_surface.blit(pause_surface,(0,0))
        
        self.game_surface.blit(self.text_PAUSE, self.text_PAUSE_rect)
        self.text_GotoMenu = self.FONT_SMALL.render("Press \"M\" to go to Main Menu", True, YELLOW)
        self.game_surface.blit(self.text_GotoMenu, self.text_GotoMenu_rect)
        
        pygame.display.update()
        
    def gameover_surface(self):
        over_surface = pygame.Surface(SC_SIZE)
        over_surface.fill(RED)
        over_surface.set_alpha(1)
        self.game_surface.blit(over_surface,(0,0))
        pygame.mixer.music.pause()
        
        self.game_surface.blit(self.text_GameOver, self.text_GameOver_rect)
        self.text_GotoMenu = self.FONT_SMALL.render("Press \"M\" to go to Main Menu", True, RED)
        self.game_surface.blit(self.text_GotoMenu, self.text_GotoMenu_rect)
        self.game_surface.blit(self.text_Continue, self.text_Continue_rect)
       
        pygame.display.update()
    
    
    def reset_game(self):
        self.game_over = False
        
        # reset player
        self.player_rect.topleft = (8, 64)
        self.player_score = 0
        self.player_velocity = PLAYER_STARTING_VELOCITY
        
        
        # reset coin
        self.coin_velocity = COIN_STARTING_VELOCITY
        self.coin_rect.x = SC_WIDTH + BUFFER_DISTACNE
        self.coin_rect.y = randint(54, SC_HEIGHT - self.coin_rect.height - 4)
        
        # reset lives
        self.player_lives = PLAYER_LIVES
        self.lives_txt = "* * * * *"
        self.text_Lives = self.FONT_MEDIUM.render(self.lives_txt, True, WHITE)
        self.text_Lives_rect = self.text_Lives.get_rect()
        self.text_Lives_rect.topright = (SC_WIDTH-8,16)
        
        
        
    def main_loop(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return "Quit"
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause = not self.pause
                    if (self.pause and event.key == K_m) or (self.game_over and event.key == K_m):
                        print("Back to MainMenu!")
                        return "Menu"
                    if self.game_over and event.key == K_c:
                        self.reset_game()
                        print("reset")
           
                    
            if not self.show_intro:
                self.intro()
                self.show_intro = True
            
            if self.pause:
                pygame.mixer.music.pause()
                self.pause_surface()
            else:
                if self.game_over:
                    pygame.mixer.music.pause()
                    self.gameover_surface()
                else:
                    pygame.mixer.music.unpause()
                    self.controller()
                    self.render()
            
            
            
            
            self.clock.tick(FPS)
                
        
                    


if __name__ == "__main__":
    game = Game()
    game.main_loop()