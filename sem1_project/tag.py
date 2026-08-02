import pygame

pygame.init()
pygame.mixer.init()




"""fixed variables"""
FPS = 60

#window settings
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YOU'RE IT!!")


#font
FONT = pygame.font.SysFont(None, 50)
FONT_TWO = pygame.font.SysFont(None, 25)
FONT_THREE = pygame.font.SysFont(None, 35)

#colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

#player settings
#global
PLAYER_SIZE = 40
PLAYER_SPEED = 9
#for IT
SPEED_INCREASE_PER_SECOND = 0.2 
MAX_SPEED = 12
#starting positions 
BLUE_START = (215, 200)
RED_START = (600, 675)

#secret
SECRET_ZONE_Y_RANGE = (650, 890)
SECRET_ZONE_MAX_X = 940




"""classes"""
'''1'''
class Player:

    def __init__(self, x, y, color, controls):
        self.x = x
        self.y = y
        self.color = color
        self.controls = controls  

    def get_rect(self):
        return pygame.Rect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, keys, speed):

        player_rect = self.get_rect()

        new_x = 0
        new_y = 0

        if keys[self.controls['left']]:
            new_x -= speed
        if keys[self.controls['right']]:
            new_x += speed
        if keys[self.controls['up']]:
            new_y -= speed
        if keys[self.controls['down']]:
            new_y += speed

        player_rect.x += new_x                                      #check horizontal collisions
        for obstacle in OBSTACLES:
            if player_rect.colliderect(obstacle.rect):
                if new_x > 0:
                    player_rect.right = obstacle.rect.left
                elif new_x < 0:
                    player_rect.left = obstacle.rect.right

        player_rect.y += new_y                                       #check vertical collisions
        for obstacle in OBSTACLES:
            if player_rect.colliderect(obstacle.rect):
                if new_y > 0:
                    player_rect.bottom = obstacle.rect.top
                elif new_y < 0:
                    player_rect.top = obstacle.rect.bottom
                                                                          
        if SECRET_ZONE_Y_RANGE[0] <= player_rect.y <= SECRET_ZONE_Y_RANGE[1]:        #parameters for a secret zone/ escape route
            player_rect.x = max(0, min(player_rect.x, SECRET_ZONE_MAX_X))
        else:
            player_rect.x = max(0, min(player_rect.x, WIDTH - PLAYER_SIZE))

        player_rect.y = max(0, min(player_rect.y, HEIGHT - PLAYER_SIZE))

        self.x = player_rect.x
        self.y = player_rect.y

    def draw(self, is_it):
        if is_it:
            pygame.draw.rect(WIN, YELLOW, (self.x - 5, self.y - 5, PLAYER_SIZE + 10, PLAYER_SIZE + 10))
        pygame.draw.rect(WIN, self.color, (self.x, self.y, PLAYER_SIZE, PLAYER_SIZE))

    def reset(self, start_pos):
        self.x, self.y = start_pos


'''2'''
class Obstacle:

    def __init__(self, x, y, width, height, color=YELLOW):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)

#obstacle list
OBSTACLES = [Obstacle(345, 0, 212, 160), Obstacle(438, 220, 25, 450), Obstacle(360, 408, 240, 25), Obstacle(120, 40, 25, 220), Obstacle(40, 140, 220, 20), Obstacle(760, 30, 30, 300), Obstacle(650, 160, 180, 25), Obstacle(110, 650, 20, 180), Obstacle(40, 760, 220, 30), Obstacle(800, 600, 25, 250), Obstacle(720, 760, 180, 35), Obstacle(700, 480, 50, 50), Obstacle(250, 600, 90, 90), Obstacle(200, 300, 70, 70), Obstacle(550, 480, 35, 35), Obstacle(400, 820, 200, 20)]
             #clock box


'''3'''
class Scoreboard:

    def __init__(self):
        self.scores = {1: 0, 2: 0}
        self.round_times = []

    def record_round(self, round_number, it_player, round_time):

        if self.round_times:
            previous_time = self.round_times[-1]
            other_player = 2 if it_player == 1 else 1

            if round_time < previous_time:    #scoring system
                self.scores[it_player] += 1
                print(f"Round {round_number}: {round_time:.2f}s (faster than {previous_time:.2f}s) — Player {it_player} scores.")
            else:
                self.scores[other_player] += 1
                print(f"Round {round_number}: {round_time:.2f}s (slower than {previous_time:.2f}s) — Player {other_player} scores.")
        else:
            print(f"Round {round_number}: {round_time:.2f}s (first round, no comparison)")

        self.round_times.append(round_time)

    def get_winner_message(self):
        if self.scores[1] > self.scores[2]:   #determine the winner
            return "Blue Wins."
        elif self.scores[2] > self.scores[1]:
            return "Red Wins."
        else:
            return "It's a Tie."

   
'''4'''
class RoundManager:

    def __init__(self, total_rounds=6):
        self.total_rounds = total_rounds
        self.round_number = 1
        self.round_start_player = 1
        self.it_player = 1
        self.round_start_time = pygame.time.get_ticks()

    def get_elapsed_seconds(self):                                              #to get time in seconds for each round
        elapsed_ms = pygame.time.get_ticks() - self.round_start_time
        return elapsed_ms / 1000

    def start_next_round(self):
        self.round_start_player = 2 if self.round_start_player == 1 else 1      #switch players to start next round
        self.it_player = self.round_start_player                                #switch IT
        self.round_start_time = pygame.time.get_ticks()
        self.round_number += 1

    def is_game_over(self):
        return self.round_number > self.total_rounds


'''5'''
class Tagging:

    def __init__(self, blue, red, round_manager, scoreboard):
        self.blue = blue
        self.red = red
        self.round_manager = round_manager
        self.scoreboard = scoreboard

    def tag(self):

        new_it_player = check_tag(self.blue, self.red, self.round_manager.it_player)     #runs a function to check who is IT

        if new_it_player != self.round_manager.it_player:                                #if tag update scoreboard
            round_time = self.round_manager.get_elapsed_seconds()
            self.scoreboard.record_round(self.round_manager.round_number, self.round_manager.it_player, round_time)

            self.blue.reset(BLUE_START)                                                     #reset positions
            self.red.reset(RED_START)

            self.round_manager.start_next_round()                                           #reset round
        else:
            self.round_manager.it_player = new_it_player


'''6'''
class SoundControl:

    def __init__(self):
        self.beep_sound = pygame.mixer.Sound("countdown_beep.wav")
        self.go_sound = pygame.mixer.Sound("go.wav")

    def play_beep(self):
        self.beep_sound.play()

    def play_go(self):
        self.go_sound.play()







"""functions"""

def check_tag(blue, red, it_player):

    if blue.get_rect().colliderect(red.get_rect()):
        if it_player == 1:
            it_player = 2
        else:
            it_player = 1

    return it_player



def get_it_speed(elapsed_seconds): 
    return min(PLAYER_SPEED + SPEED_INCREASE_PER_SECOND * elapsed_seconds, MAX_SPEED)



def wait_for_start():  #wait screen for intro

    waiting_to_start = True

    while waiting_to_start:
        draw_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting_to_start = False

    return False 




def wait_for_close(scoreboard): #wait screen outro

    waiting_to_close = True

    while waiting_to_close:
        draw_winner_screen(scoreboard)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
          
    return False






"""DRAWWING FUNCTIONS"""
def draw_background():  
    WIN.fill(BLACK)


def draw_start_screen():

    WIN.fill(BLACK)

    title_text = FONT.render("Welcome To YOU'RE IT!!", True, YELLOW)
    next_text = FONT.render("Press SPACE to start", True, WHITE)
    instruction_text_blue = FONT.render("Blue: WASD", True, BLUE)
    instruction_text_red = FONT.render("Red: Arrow Keys", True, RED)
    instruction_general1 = FONT_TWO.render("Blue player starts as IT.", True, WHITE)
    instruction_general = FONT_TWO.render("Dont Get Tagged!  IT will get faster over time.", True, WHITE)

    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 200))
    WIN.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2 + 300))
    WIN.blit(instruction_text_red, (WIDTH // 2 - instruction_text_red.get_width() // 2, HEIGHT // 2 -10))
    WIN.blit(instruction_text_blue, (WIDTH // 2 - instruction_text_blue.get_width() // 2, HEIGHT // 2 - 60))
    WIN.blit(instruction_general1, (WIDTH // 2 - instruction_general1.get_width() // 2, HEIGHT // 2 + 100))
    WIN.blit(instruction_general, (WIDTH // 2 - instruction_general.get_width() // 2, HEIGHT // 2 + 130))

    pygame.display.update()


def draw_countdown(sounds):

    clock = pygame.time.Clock()

    for count in ["3", "2", "1", "RUN LIKE THE WIND!"]:

        if count == "RUN LIKE THE WIND!":
            sounds.play_go()
        else:
            sounds.play_beep()

        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 1000:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            WIN.fill(BLACK)

            count_text = FONT.render(count, True, YELLOW)
            WIN.blit(count_text, (WIDTH // 2 - count_text.get_width() // 2, HEIGHT // 2 - count_text.get_height() // 2))

            pygame.display.update()
            clock.tick(FPS)


def draw_ui(elapsed_seconds, round_number, scores):  #game UI

    timer_text = FONT.render(f"Time: {elapsed_seconds:.1f}s", True, BLACK)          #timer text
    WIN.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))

    round_text = FONT.render(f"Round: {round_number}/6", True, BLACK)               #round number
    WIN.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, 70))

    score_text = FONT_THREE.render(f"Blue: {scores[1]}   Red: {scores[2]}", True, BLACK)  #scores
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 120))


def draw_winner_screen(scoreboard):     

    WIN.fill(YELLOW)

    message = scoreboard.get_winner_message()

    winner_text = FONT.render(message, True, BLACK)
    score_text = FONT.render(f"Final Score  —  Blue: {scoreboard.scores[1]}   Red: {scoreboard.scores[2]}", True, BLACK)
    thankyou_text = FONT.render(f"Thanks for playing!", True, BLACK)
    
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 70))
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 -15))
    WIN.blit(thankyou_text, (WIDTH // 2 - thankyou_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.update()







"""MAIN GAME LOOP"""
def main():

    clock = pygame.time.Clock()

    player_quit = wait_for_start()    #wait for space or quit
    if player_quit:
        pygame.quit()
        return

    sounds = SoundControl()
    draw_countdown(sounds)


    run = True

    #2 players
    blue = Player(BLUE_START[0], BLUE_START[1], BLUE, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s})
    red = Player(RED_START[0], RED_START[1], RED, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN})


    round_manager = RoundManager()
    scoreboard = Scoreboard()
    tag_check = Tagging(blue, red, round_manager, scoreboard)



    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        
        keys = pygame.key.get_pressed() #inputs


        elapsed_seconds = round_manager.get_elapsed_seconds()    #IT speed increase over time in each round
        it_speed = get_it_speed(elapsed_seconds)                 


        blue.move(keys, it_speed if round_manager.it_player == 1 else PLAYER_SPEED)      #player movements
        red.move(keys, it_speed if round_manager.it_player == 2 else PLAYER_SPEED)       


        tag_check.tag()       #check for tag


        draw_background()

        for obstacle in OBSTACLES:
            obstacle.draw()

        draw_ui(elapsed_seconds, round_manager.round_number, scoreboard.scores)

        #draw players (yellow outline if IT)
        blue.draw(round_manager.it_player == 1)           
        red.draw(round_manager.it_player == 2)

        if round_manager.is_game_over():                #game over check
            run = False

        # Update display
        pygame.display.update()

    player_quit_end = wait_for_close(scoreboard)         #WINNER screen and waiting for quit
    if player_quit_end:
        pygame.quit()
        return
    

if __name__ == "__main__":
    main()
