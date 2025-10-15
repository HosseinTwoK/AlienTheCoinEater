# scene controller module
from settings import *
from mainmenu import Menu
from game import Game


def main():
    current_scene = "mainmenu"
    
    show = True
    while show:
        if current_scene == "mainmenu":
            scene_one = Menu()
            state = scene_one.main_loop() # "Play", "Quit"
            
            if state == "Play":
                current_scene = "game"
            elif state == "Quit":
                show = False
        elif current_scene == "game": # "Menu", "Quit"
            scene_two = Game()
            state = scene_two.main_loop()
            
            if state == "Menu":
                current_scene = "mainmenu"
            elif state == "Quit":
                show = False
                
                
                
                
if __name__ == "__main__":
    main()