from game import Game
from settings import *


class Menu():
    def __init__(self):
        pygame.init()
        
        self.display_surface = pygame.display.set_mode(SC_SIZE)
        pygame.display.set_caption(TITLE_MENU)
        # icon 
        icon = pygame.image.load(path.join("assets","icon","alien.ico"))
        pygame.display.set_icon(icon)
        
        self.clock = pygame.time.Clock()
        
        self.running = True
        
        self.hovered_play = False
        self.hovered_exit = False
        
        self.clicked_play = False
        self.clicked_exit = False
        
        self.load_assets()
        
    
    def load_assets(self):
        # background
        self.image_bg = pygame.image.load(path.join("assets","ui","menu-bg.png")).convert()
        
        self.image_button_play = pygame.image.load(path.join("assets","ui","button-play.png")).convert()
        self.button_play = self.image_button_play.get_rect()
        self.button_play.center = (CENTER_WIDTH, CENTER_HEIGHT-50)
        
        self.image_button_exit = pygame.image.load(path.join("assets","ui","button-exit.png")).convert()
        self.button_exit = self.image_button_exit.get_rect()
        self.button_exit.center = (CENTER_WIDTH, CENTER_HEIGHT+50)
        
        self.image_pointer = pygame.image.load(path.join("assets","ui","pointer.png"))
        self.pointer_rect = self.image_pointer.get_rect()
        
        # hover sound effect
        self.sound_hover = pygame.mixer.Sound(path.join("assets","ui","button-hover.wav"))
        self.sound_hover.set_volume(0.3)
        pygame.mixer.music.load(path.join("assets","ui","menu-music.wav"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1,0.0)
        

        myfont = pygame.font.Font(path.join("assets","fonts","PixeloidSans.ttf"),16)
        self.text_created = myfont.render("myFirstPygameProject \"amHossein\"",True, DARK_BLUE)
        self.text_created = pygame.transform.rotate(self.text_created,90)
        self.text_created_rect = self.text_created.get_rect()
        self.text_created_rect.topright = (SC_WIDTH-1,1)
        
        
    def render(self):
        self.display_surface.blit(self.image_bg,(0,0))
        
        self.display_surface.blit(self.image_button_play, self.button_play)
        self.display_surface.blit(self.image_button_exit, self.button_exit)
        
        self.display_surface.blit(self.text_created, self.text_created_rect)
        
        if self.hovered_play:
            # NOTE here i understood topright is tuple of (x,y) while right alon is only position x
            # but we can use midright to use the tople format
            self.pointer_rect.topright = (self.button_play.topleft[0] - 10, self.button_play.topleft[1])
            self.display_surface.blit(self.image_pointer, self.pointer_rect)
            pygame.draw.rect(self.display_surface,(255,255,0),self.button_play,2)
        if self.hovered_exit:
            self.pointer_rect.topright = (self.button_exit.topleft[0] - 10, self.button_exit.topleft[1])
            self.display_surface.blit(self.image_pointer, self.pointer_rect)
            pygame.draw.rect(self.display_surface,(255,255,0),self.button_exit,2)
        
        pygame.display.update()
        
    
    def main_loop(self):
        already_hovered_play = False
        already_hovered_exit = False
        while self.running:
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    print("Exit Button Clicked! (Menu Display)")
                    self.running = False
                    return "Quit"
                if event.type == MOUSEMOTION:
                    self.hovered_play = self.button_play.collidepoint(event.pos) 
                    self.hovered_exit = self.button_exit.collidepoint(event.pos)
                    
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.clicked_play = self.button_play.collidepoint(event.pos)
                    self.clicked_exit = self.button_exit.collidepoint(event.pos)

            
            if self.hovered_play and not(already_hovered_play):
                self.sound_hover.play()
            if self.hovered_exit and not(already_hovered_exit):
                self.sound_hover.play()

           
            already_hovered_play = self.hovered_play
            already_hovered_exit = self.hovered_exit
            
            if self.clicked_play:
                print("Starting the Game...")
                pygame.mixer.music.pause()
                return "Play"
            if self.clicked_exit:
                print("Exit Button Clicked!")
                return "Quit"
                
                        
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        
        
        
        
if __name__ == "__main__":
    menu = Menu()
    menu.main_loop()