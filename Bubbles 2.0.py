#_Imports__________________________________________________________________________________
import pygame, random, os, sys
from pygame.constants import MOUSEBUTTONDOWN
pygame.init()


#_Classes__________________________________________________________________________________
"""         Settings            """
class Settings(object):
    # window
    title                   = "Bubble Shooter 2.0"
    width, height, border   = 1440, 900, 10
    fps60, fps30            = 60, 30
    # game variables
    game_paused             = True
    stats_enabled           = False
    score                   = 0
    # paths
    file_path               = os.path.dirname(os.path.abspath(__file__))
    images_path             = os.path.join(file_path, "images")
    sounds_path             = os.path.join(file_path, "sounds")

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)


"""         Cursor          """
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image  = pygame.image.load(os.path.join(Settings.images_path, "Diamond_Sword.png")).convert_alpha()
        self.image  = pygame.transform.scale(self.image, (30, 35))
        self.rect   = self.image.get_rect()

    def update_cursor(self):
        self.rect.topleft = pygame.mouse.get_pos()


"""         Keyboard            """
class Keyboard(pygame.sprite.Sprite):
    def __init__(self):
        pass

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()

            # quit Game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    print("Quitting Game...")               
                    pygame.quit(), sys.exit()

                # enable/disable statistic
                elif event.key == pygame.K_F3:
                    if Settings.stats_enabled == False:
                        Settings.stats_enabled = True
                        print("Statistic enabled")
                    elif Settings.stats_enabled == True:
                        Settings.stats_enabled = False
                        print("Statistic disabled")
                        
                # pause/continue game
                elif event.key == pygame.K_p:
                    if Settings.game_paused == False:
                        Settings.game_paused = True
                        print("Game Paused")
                    elif Settings.game_paused == True:
                        Settings.game_paused = False
                        print("Game Continued")


"""         Bubbles         """
class Bubbles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sizex                          = random.randint(30, 60)
        self.sizey                          = self.sizex

        self.image                          = pygame.image.load(os.path.join(Settings.images_path, "Bubble.png")).convert_alpha()
        self.image                          = pygame.transform.scale(self.image, (self.sizex, self.sizey))

        self.rect                           = self.image.get_rect()
        self.rect.centery                   = random.randint(0, Settings.width)
        self.rect.centerx                   = random.randint(0, Settings.height)
        self.rect_combined                  = self.rect.centerx, self.rect.centery

        self.mouse_pos_x, self.mouse_pos_y  = pygame.mouse.get_pos()
        self.grow_factor                    = 0


    def update(self):
        # If Mouse hovers above bubble -> change cursor Image | If Mouse-click on Bubble -> delete it
        if self.rect.centerx >= self.mouse_pos_x and self.rect.centery >= self.mouse_pos_y:
            Settings.score += 1
            self.kill()               


"""         Game                """
class Game(object):
    def __init__(self):
        # Window
        pygame.display.set_caption(Settings.title)
        self.screen                 = pygame.display.set_mode(Settings.get_dim())
        self.clock                  = pygame.time.Clock()

        # Start and pause background
        self.pause_screen           = pygame.image.load(os.path.join(Settings.images_path, "Background.png")).convert()
        self.pause_screen           = pygame.transform.scale(self.pause_screen, (Settings.width, Settings.height))
        self.pause_screen_rect      = self.pause_screen.get_rect()

        # Game background
        self.background             = pygame.image.load(os.path.join(Settings.images_path, "Background_Game.png")).convert()
        self.background             = pygame.transform.scale(self.background, (Settings.width, Settings.height))
        self.background_rect        = self.background.get_rect()

        # Classes
        self.cursor, self.keyboard, self.bubbles = Cursor(), Keyboard(), Bubbles()

        # Spritegroups
        self.mouse                  = pygame.sprite.Group()
        self.mouse.add(self.cursor)
        self.all_bubbles = pygame.sprite.Group()

        self.done                   = False
        self.first_enter            = True
        self.spawncounter            = 100

        # Music
        pygame.mixer.music.load(os.path.join(Settings.sounds_path, "Minecraft-C418-Strad.mp3"))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(.25)


    def update_text(self):
        self.font, self.font2, self.color   = pygame.font.SysFont("Arial", 18, True, False), pygame.font.SysFont("Arial", 36, True, False), (255, 255, 255)
        self.render_welcome                 = self.font2.render(str("Welcome to \"Minecraft Bubble Shooter\""), True, self.color)
        self.render_continue                = self.font.render(str("Press [P] to Continue the Game"), True, self.color)
        self.render_paused                  = self.font2.render(str("Game Paused!"), True, self.color)
        self.render_stats                   = self.font.render(str("Press [F3] to see some Stats e.g. Mouse Position"), True, self.color)
        

        self.show_score                         = self.font.render(str(Settings.score), True, self.color)
        self.position, self.render_pos          = self.font.render(str("Position:"),    True, self.color), self.font.render(str(pygame.mouse.get_pos()), True, self.color)
        self.click, self.render_click           = self.font.render(str("Click:"),       True, self.color), self.font.render(str(pygame.mouse.get_pressed()), True, self.color)
        self.fps_target, self.render_fps        = self.font.render(str("FPS:"),         True, self.color), self.font.render(str(self.clock), True, self.color)
        self.render_res, self.resx, self.resy   = self.font.render(str("Resolution:"),  True, self.color), self.font.render(str(Settings.width), True, self.color), self.font.render(str(Settings.height), True, self.color)


    def create_bubbles(self):
        for i in range(0, 3):
            self.bubbles     = Bubbles()
            self.all_bubbles.add(self.bubbles)
            self.spawncounter = 0


    def update_window(self):
        self.clock.tick(Settings.fps60)
        self.screen.blit(self.pause_screen, self.pause_screen_rect)
        self.keyboard.input(),  self.cursor.update_cursor()
        self.mouse.update(),    self.mouse.draw(self.screen)


    def update_game(self):
        if Settings.game_paused and self.first_enter == True:
            pygame.mouse.set_visible(True)
            self.screen.blit(self.render_welcome,   ((Settings.width - Settings.border)/3.8,    (Settings.height - Settings.border)/2))
            self.screen.blit(self.render_continue,  ((Settings.width - Settings.border)/2.5,    (170 + Settings.height - Settings.border)/2))
            self.screen.blit(self.render_stats,     ((Settings.width - Settings.border)/2.9,    (220 + Settings.height - Settings.border)/2))

        # Pause screen will be shown
        elif Settings.game_paused == True and self.first_enter == False:
            pygame.mouse.set_visible(True)
            self.screen.blit(self.show_score,       ((Settings.width - Settings.border)/2, Settings.height/10))
            self.screen.blit(self.render_paused,    (Settings.width/2.45, Settings.height/2))
            self.screen.blit(self.render_continue,  (Settings.width/2.5, 50 + Settings.height/2))

        if Settings.game_paused == False:
            self.first_enter = False
            pygame.mouse.set_visible(False)
            self.screen.blit(self.background,   self.background_rect), self.screen.blit(self.show_score, (1380, 10))
            self.all_bubbles.update(),          self.all_bubbles.draw(self.screen)
            self.mouse.draw(self.screen)

            # Statistics 
            if Settings.stats_enabled == True:
                pygame.mouse.set_visible(True)

                self.screen.blit(self.fps_target, (10, 10)),    self.screen.blit(self.render_fps, (115, 10))
                self.screen.blit(self.render_res, (10, 40)),    self.screen.blit(self.resx, (115, 40)), self.screen.blit(self.resy, (165, 40))
                self.screen.blit(self.position, (10, 70)),      self.screen.blit(self.render_pos, (115, 70))
                self.screen.blit(self.click, (10, 100)),        self.screen.blit(self.render_click, (115, 100))

        pygame.display.flip()


    def run(self):
        while not self.done:
            self.update_text()
            self.update_window()
            self.update_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            if self.spawncounter >= 100:
                self.create_bubbles()
            else: 
                self.spawncounter += 1


"""         Execute         """
if __name__ == '__main__':
    game = Game()
    game.run(), pygame.quit()