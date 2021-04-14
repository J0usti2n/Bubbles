#_Imports________________________________________________________________
import pygame, random, os, sys
pygame.init()


#_Classes________________________________________________________________
"""         Settings        """
class Settings(object):
    title                       = "Minecraft Bubble Shooter"
    width, height, bordersize   = 1440, 900, 10                         # 8:5 Aspect Ratio
    fps, fps30                  = 60, 30                                # If Game paused, fps switching to 30 and switch up again to 60 when game is unpaused

    paused  = True
    stats   = False
    score   = 0

    file_path   = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "images")
    sounds_path = os.path.join(file_path, "sounds")

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)




"""         Cursor          """
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image  =  pygame.image.load(os.path.join(Settings.images_path, "Diamond_Sword.png")).convert_alpha()      
        self.image  = pygame.transform.scale(self.image, (30,35))
        self.rect   = self.image.get_rect()

    def update(self):
        self.rect.left, self.rect.top        = pygame.mouse.get_pos()



"""         Control         """
class Control(pygame.sprite.Sprite):
    def __init__(self):
        pass

    # Input
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()

            # Keyboard
            if event.type == pygame.KEYDOWN:
                # quit game
                if event.key == pygame.K_ESCAPE:
                    print("Quitting Game...")               # Debug
                    pygame.quit(), sys.exit()

                # enable/disable Statistic
                elif event.key == pygame.K_F3:
                    if Settings.stats == False:
                        Settings.stats = True
                        print("Statistic enabled")
                    elif Settings.stats == True:
                        Settings.stats = False
                        print("Statistic disabled")
                        
                # pause game / continue game
                elif event.key == pygame.K_p:
                    if Settings.paused == False:
                        Settings.paused = True
                        print("Game Paused")
                    elif Settings.paused == True:
                        Settings.paused = False
                        print("Game Continued")

            # Mouse input            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())




"""         Bubbles         """
class Bubbles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size   = random.randint(30, 60) 

        self.image  = pygame.image.load(os.path.join(Settings.images_path, "Bubble.png")).convert_alpha()
        self.image  = pygame.transform.scale(self.image, (self.size, self.size))

        self.rect           = self.image.get_rect()
        self.rect.centerx   = random.randrange(Settings.bordersize, Settings.width - Settings.bordersize - self.size)
        self.rect.centery   = random.randrange(Settings.bordersize, Settings.height - Settings.bordersize - self.size)

        self.hit            = False



"""         Game            """
class Game(object):
    def __init__(self):
        pygame.display.set_caption(Settings.title)
        self.screen             = pygame.display.set_mode(Settings.get_dim())
        self.clock              = pygame.time.Clock()

        self.start              = pygame.image.load(os.path.join(Settings.images_path, "Background.png")).convert()
        self.start              = pygame.transform.scale(self.start, (Settings.width, Settings.height))
        self.start_rect         = self.start.get_rect()

        self.background         = pygame.image.load(os.path.join(Settings.images_path, "Background_Night.png")).convert()
        self.background         = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect    = self.background.get_rect()

        pygame.mixer.music.load(os.path.join(Settings.sounds_path, "Minecraft-C418-Strad.mp3"))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(.25)

        self.control, self.cursor, self.bubbles = Control(), Cursor(), Bubbles()

        self.mice  = pygame.sprite.Group()
        self.mice.add(self.cursor)

        self.done           = False
        self.first_enter    = True


        self.font, self.font2, self.color   = pygame.font.SysFont("Arial", 18, True, False), pygame.font.SysFont("Arial", 36, True, False), (255, 255, 255)
        self.render_welcome                 = self.font2.render(str("Welcome to \"Minecraft Bubble Shooter\""), True, self.color)
        self.render_continue                = self.font.render(str("Press [P] to Continue the Game"), True, self.color)
        self.render_paused                  = self.font2.render(str("Game Paused!"), True, self.color)
        self.render_stats                   = self.font.render(str("Press [F3] to see some Stats e.g. Mouse Position"), True, self.color)


    def update_text(self):
        # Variables needs to be in update method because otherwise they would be static
        self.show_score                     = self.font.render(str(Settings.score), True, self.color)
        self.position, self.render_pos      = self.font.render(str("Position:"), True, self.color), self.font.render(str(pygame.mouse.get_pos()), True, self.color)
        self.click, self.render_click       = self.font.render(str("Click:"), True, self.color), self.font.render(str(pygame.mouse.get_pressed()), True, self.color)
        self.fps_target, self.render_fps    = self.font.render(str("FPS:"), True, self.color), self.font.render(str(self.clock), True, self.color)


    def update(self):
        self.clock.tick(Settings.fps)
        self.screen.blit(self.start, self.start_rect)
        self.control.input()
        self.mice.update()
        self.mice.draw(self.screen)

        # When the game runs at the first time, you first get an Welcome screenw including some informations
        if Settings.paused and self.first_enter == True:

            pygame.mouse.set_visible(True)

            self.screen.blit(self.render_welcome,   ((Settings.width - Settings.bordersize)/4,      (Settings.height - Settings.bordersize)/2))
            self.screen.blit(self.render_continue,  ((Settings.width - Settings.bordersize)/2.5,    (150 + Settings.height - Settings.bordersize)/2))
            self.screen.blit(self.render_stats,     ((Settings.width - Settings.bordersize)/2.85,   (190 + Settings.height - Settings.bordersize)/2))


        # Pause screen will be shown
        elif Settings.paused == True and self.first_enter == False:
    
            self.screen.blit(self.show_score, (Settings.width/2, Settings.height/10))
            self.screen.blit(self.render_paused, (Settings.width/2.456, Settings.height/2))
            self.screen.blit(self.render_continue, (Settings.width/2.5, 50 + Settings.height/2))


        if Settings.paused == False:
            self.first_enter = False
            pygame.mouse.set_visible(False)
            self.screen.blit(self.background, self.background_rect), self.screen.blit(self.show_score, (1380, 10))
            self.mice.draw(self.screen)


            # Statistics 
            if Settings.stats == True:
                pygame.mouse.set_visible(True)
                self.screen.blit(self.fps_target, (10, 10)), self.screen.blit(self.render_fps, (100, 10))
                self.screen.blit(self.position, (10, 40)), self.screen.blit(self.render_pos, (100, 40))
                self.screen.blit(self.click, (10, 70)), self.screen.blit(self.render_click, (100, 70))

        pygame.display.flip()




    def run(self):
        while not self.done:
            self.update()
            self.update_text()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True




"""         Execute         """
if __name__ == '__main__':
    game = Game()
    game.run(), pygame.quit()