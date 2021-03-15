import pygame
import sys
import random
import math
from settings import *

pygame.init()


#initializing the Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ROCK PAPER SCISSOR")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.player_name = PLAYER_NAME
        self.player_wins = 0
        self.computer_wins = 0
        self.wins_necessary = math.ceil(BEST_OF/2)
        self.COMP_url = 'Assets/Logo.png'
        self.USER_url = 'Assets/Logo.png'
        self.result = ""
        self.computer = ""
        self.user = ""

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


############################ HELPER FUNCTIONS ##################################
	
	#Draw text function to write text on screen
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    # choose url & (r/s/p) for computer
    def computer_choice(self):
        computer = random.choice(['r', 'p', 's'])
        if computer == "r":
            COMP_url = 'Assets/R_rock.png'

        if computer == "p":
            COMP_url = 'Assets/R_paper.png'

        if computer == "s":
            COMP_url = 'Assets/R_scissor.png'

        return (computer, COMP_url)

    # compare user and computer and return result for each round
    def play_result(self):
        if self.user == self.computer:
            return "Tie"
        
        if (self.user == 'r' and self.computer == 's') or (self.user == 's' and self.computer == 'p') or (self.user == 'p' and self.computer == 'r'):
            self.player_wins = self.player_wins + 1
            return "Victory"

        self.computer_wins = self.computer_wins + 1
        return "Defect"

    def reset(self):
        self.player_wins = 0
        self.computer_wins = 0
        self.COMP_url = 'Assets/Logo.png'
        self.USER_url = 'Assets/Logo.png'
        self.result = ""
        self.computer = ""
        self.user = ""
        return "playing"


########################### STARTING FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    # display starting screen
    def start_draw(self):
        self.screen.fill(BLACK)
        
        # display Logo
        IMG = pygame.image.load(LOGO)
        IMG = pygame.transform.scale(IMG, (int(150), int(150)))
        self.screen.blit(IMG, (50, 50, 150, 150))

        # Heading of the Game
        self.draw_text('ROCK PAPER SCISSOR', self.screen, [WIDTH//2+80, HEIGHT//2-220], 60, WHITE, START_FONT, centered=True)
                       
        self.draw_text('r       -       "Rock"', self.screen, [WIDTH//2-150, HEIGHT//2-45], 30, CYAN, START_FONT, centered=False)
        self.draw_text('p       -       "Paper"', self.screen, [WIDTH//2-150, HEIGHT//2-15], 30, CYAN, START_FONT, centered=False)
        self.draw_text('s       -       "Scissor"', self.screen, [WIDTH//2-150, HEIGHT//2+15], 30, CYAN, START_FONT, centered=False)

        self.draw_text('Note :-', self.screen, [120, HEIGHT//2+150], 20, RED, START_FONT, centered=False)
        self.draw_text('"Rock" beats "Scissor"', self.screen, [200, HEIGHT//2+150], 20, WHITE, 'arial', centered=False)
        self.draw_text('"Sciccor" beats "Paper"', self.screen, [200, HEIGHT//2+180], 20, WHITE, 'arial', centered=False)
        self.draw_text('"Paper" beats "Rock', self.screen, [200, HEIGHT//2+210], 20, WHITE, 'arial', centered=False)

        self.draw_text('PUSH SPACE TO PLAY', self.screen, [WIDTH//2, HEIGHT-50], 20, GREY, START_FONT, centered=True)
                       
        pygame.display.update()


########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if self.player_wins < self.wins_necessary and self.computer_wins < self.wins_necessary:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.user = "r" 
                        self.USER_url = 'Assets/L_rock.png'
                        (self.computer, self.COMP_url) = self.computer_choice()
                        self.result = self.play_result()
                    
                    if event.key == pygame.K_p:
                        self.user = "p"
                        self.USER_url = 'Assets/L_paper.png'
                        (self.computer, self.COMP_url) = self.computer_choice()
                        self.result = self.play_result()
                        
                    if event.key == pygame.K_s:
                        self.user = "s"
                        self.USER_url = 'Assets/L_scissor.png'
                        (self.computer, self.COMP_url) = self.computer_choice()
                        self.result = self.play_result()
                        
            else:
                self.state = 'game over'

    # display playing screen
    def playing_draw(self):
        self.screen.fill(BLACK)

        self.draw_text('Best of "{}"'.format(BEST_OF), self.screen, [WIDTH-150, HEIGHT//2-320], 25, GREY, 'arial',)
        self.draw_text('Enter Your Choice? (r, p, s)', self.screen, [WIDTH//2-13, HEIGHT//2-250], 25, BLUE, START_FONT, centered=True)
        self.draw_text('{0} : {1}'.format(self.player_name, self.player_wins), self.screen, [WIDTH//2-300, HEIGHT//2-200], 20, WHITE, START_FONT)
        self.draw_text('Comp : {}'.format(self.computer_wins), self.screen, [WIDTH//2+200, HEIGHT//2-200], 20, WHITE, START_FONT)

        U_IMG = pygame.image.load(self.USER_url)
        U_IMG = pygame.transform.scale(U_IMG, (int(150), int(150)))
        self.screen.blit(U_IMG, (WIDTH//2-300, HEIGHT//2, 150, 150))

        C_IMG = pygame.image.load(self.COMP_url)
        C_IMG = pygame.transform.scale(C_IMG, (int(150), int(150)))
        self.screen.blit(C_IMG, (WIDTH//2+200, HEIGHT//2, 150, 150))

        self.draw_text(self.result, self.screen, [WIDTH//2, HEIGHT//2], 25, WHITE, 'arial')
        
        pygame.display.update()

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    # Displaying GAME OVER screen
    def game_over_draw(self):
        self.screen.fill(BLACK)
        gameover_bg = pygame.image.load(GAME_OVER_url)
        gameover_bg = pygame.transform.scale(gameover_bg, (WIDTH-20, HEIGHT-20))
        self.screen.blit(gameover_bg, (25, 10, WIDTH-20, HEIGHT-20))
        
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  52, RED, START_FONT, centered=True)
        
        # checking & display final result
        if self.player_wins > self.computer_wins:
            self.draw_text("VICTORY", self.screen, [WIDTH//2, HEIGHT//2-100],  50, (190, 190, 190), "arial", centered=True)
        else:
            self.draw_text("DEFECT", self.screen, [WIDTH//2, HEIGHT//2-100],  50, (190, 190, 190), "arial", centered=True)

        
        self.draw_text('{0} : {1}'.format(self.player_name, self.player_wins), self.screen, [WIDTH//2, HEIGHT//2],  20, (190, 190, 190), "arial", centered=True)
        self.draw_text('Comp : {}'.format(self.computer_wins), self.screen, [WIDTH//2, HEIGHT//2+50],  20, (190, 190, 190), "arial", centered=True)
        
        self.draw_text("PRESS SPACE TO PLAY", self.screen, [WIDTH//2, HEIGHT-150],  15, (190, 190, 190), "arial", centered=True)
        self.draw_text("PRESS ESC TO QUIT", self.screen, [WIDTH//2, HEIGHT-100],  15, (190, 190, 190), "arial", centered=True)
        pygame.display.update()


# To start the game / To run starting screen
if __name__ == "__main__":
    app = Game()
    app.run()