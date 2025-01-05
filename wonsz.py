

import pygame
import random
#setting pygame
pygame.init()

rectSize = 75

sizeX = 16 * rectSize
sizeY = 12 * rectSize

screen = pygame.display.set_mode((sizeX,sizeY))

running = True

clickX = -1
clickY = -1
# map

fieldX = 16
fieldY = 12
def set_map(x, y):
    
    for i in range(x+1):
        pygame.draw.line(screen,(100,100,100), (i*rectSize, 0),(i*rectSize, rectSize*y))
        
    for j in range(y+1):
        pygame.draw.line(screen,(100,100,100), (0, j*rectSize),(rectSize*x, j*rectSize))
        
def body(x,y, color):
    
    pos_x = x*rectSize
    pos_y = y*rectSize
    
    pygame.draw.rect(screen, color, (pos_x, pos_y, rectSize, rectSize))
    
    

    


    
class Snake:
    def __init__(self):
        self.dead = False
        self.x = 0
        self.y = 0
        self.direction = 2
        # 1=>N 2=>E 3=>S 4 =>W
        self.head_color = (0,45,15)
        self.tail_color = (0,75,25)
        self.tailX = [-1]
        self.tailY = [-1]
        self.possiblePlace = [0, 0, 15, 11]

    def reset(self, x=0, y=0):
        self.dead = False
        self.x = 0
        self.y = 0
        self.direction = 2
        self.tailX = [x]
        self.tailY = [y]



    def print(self, food_name):
        for i in range(food_name.ret_eaten()):
            body(self.tailX[-i - 1], self.tailY[-i - 1], self.tail_color)

        body(self.x, self.y, self.head_color)
        
    
    def ret_x(self):
        return self.x
        
    def ret_y(self):
        return self.y
        

    def ret_dir(self):
        return self.direction
        
    def go_e(self):
        if self.x < self.possiblePlace[2]:
            self.x += 1   
        else:
            self.death()
                 
    def go_n(self):
        if self.y > self.possiblePlace[1]:
            self.y -= 1
        else:
            self.death()
            
    def go_s(self):
        if self.y < self.possiblePlace[3]:
            self.y += 1
        else:
            self.death()
     
    def go_w(self):
        if self.x > self.possiblePlace[0]:
            self.x -= 1
        else:
            self.death()
            
    def set_dir(self, direction):
            if direction == 1:
                self.direction = 1
                
            if direction == 2:
                self.direction = 2
                
            if direction == 3:
                self.direction = 3
                
            if direction == 4:
                self.direction = 4

    def move(self):
            if self.direction == 1:
                self.go_n()
                
            if self.direction == 2:
                self.go_e()
                
            if self.direction == 3:
                self.go_s()
                
            if self.direction == 4:
                self.go_w()
                
    def death(self):
        self.dead = True
                
    def is_dead(self):
        return self.dead

    def check_eat_self(self):
        for i in range(len(self.tailX) - 1):
            if self.tailX[i] == self.ret_x() and self.tailY[i] == self.ret_y():
                self.death()


class SnakeWithGun(Snake):
    def __init__(self):
        super().__init__()





class Food:
    def __init__(self,x,y):
        self.x = 0
        self.y = 0
        self.eaten = True
        self.timesEaten = 0
        self.possiblePlace = [0,0,15,11]

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.eaten = True
        self.timesEaten = 0


    def ret_eaten(self):
        return self.timesEaten
        
    def ret_x(self):
        return self.x
        
    def ret_y(self):
        return self.y
        
    def tracker(self, snake):
        collision = True
        if self.eaten:

            while collision:
                collision = False
                self.x = random.randint(self.possiblePlace[0], self.possiblePlace[2])
                self.y = random.randint(self.possiblePlace[1], self.possiblePlace[3])
                for i in range(len(snake.tailX)):
                    if snake.tailX[i-1] == self.x:
                        if snake.tailY[i-1] == self.y:
                            collision = True

            self.eaten = False
            
    def eat(self):
            self.eaten= True
            self.timesEaten += 1
            
def button(x, y, xs, ys, color=(0,0,0)):
    pygame.draw.rect(screen, color, (x*rectSize, y*rectSize, xs*rectSize, ys*rectSize))
    if x*rectSize <= clickX <= (x + xs)*rectSize:
        if y*rectSize <= clickY <= (y + ys)*rectSize:

            return True



font = pygame.font.SysFont('Comic Sans MS', rectSize)
def text(x, y, txt, color=(200,200,200)):
    text_surface = font.render(txt, False,color)
    screen.blit(text_surface,(x*rectSize, y*rectSize))

    
ticks = 0
sec = 0
rec =0

#normal
head1 = Snake()
head2 = Snake()
head2.head_color = (0, 15, 45)
head2.tail_color = (0, 25, 75)
food1 = Food(0, 0)
food2 = Food(8,0)
food1.reset(0,0)
food2.reset(8,0)
head1.reset(0,0)
head2.reset(8,0)
#with guns
head3 = SnakeWithGun()



# window set
clock = pygame.time.Clock()
fps = 60
action1 = True
action2 = True
game = False
game_mode = 0
p1_alive = True
p2_alive = True
p1_score = 0
p2_score = 0
speed = 2.0
score = 0
#run loop
while running:
    #frame initiation
    bg_col = 0 # random.randint(0,125) #colorblind disco mode
    pygame.draw.rect(screen, (bg_col, bg_col, bg_col), pygame.Rect(0, 0, sizeX, sizeY))
    ticks += 1
    rec = sec

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickX, clickY = event.pos

        if event.type == pygame.KEYDOWN and game:
            if event.key == pygame.K_w and head1.ret_dir() != 3 and action1:
                head1.set_dir(1)
                head3.set_dir(1)
                action1 = False

            if event.key == pygame.K_d and head1.ret_dir() != 4 and action1:
                head1.set_dir(2)
                head3.set_dir(2)
                action1 = False

            if event.key == pygame.K_s and head1.ret_dir() != 1 and action1:
                head1.set_dir(3)
                head3.set_dir(3)
                action1 = False

            if event.key == pygame.K_a and head1.ret_dir() != 2 and action1:
                head1.set_dir(4)
                head3.set_dir(4)
                action1 = False


            if event.key == pygame.K_UP and head2.ret_dir() != 3 and action2:
                head2.set_dir(1)
                action2 = False

            if event.key == pygame.K_RIGHT and head2.ret_dir() != 4 and action2:
                head2.set_dir(2)
                action2 = False

            if event.key == pygame.K_DOWN and head2.ret_dir() != 1 and action2:
                head2.set_dir(3)
                action2 = False

            if event.key == pygame.K_LEFT and head2.ret_dir() != 2 and action2:
                head2.set_dir(4)
                action2 = False

    # lobby
    if not game:
        #start button
        button(2, 2, 12, 4, (50, 50, 50))
        if clickX >= 0 and clickY >= 0:
            if button(2, 2, 12, 4):
                clickX = -1
                clickY = -1
                game = True
                score = 0
                ticks = -40
                if game_mode == 1:
                    head1.possiblePlace = [0, 0, 15, 11]
                    food1.possiblePlace = [0, 0, 15, 11]
                if game_mode == 0:
                    head1.possiblePlace = [0, 0, 7, 11]
                    head2.possiblePlace = [8, 0, 15, 11]
                    head2.x = 8
                    food1.possiblePlace = [0, 0, 7, 11]
                    food2.possiblePlace = [8, 0, 15, 11]
                if game_mode == 2:
                    head3.possiblePlace=[0, 0, 15, 11]
                    food1.possiblePlace = [0, 0, 15, 11]




        # speed down button
        button(4, 6, 2, 2,(0, 100, 0))
        if button(4, 6, 2, 2,(0, 100, 0)) and speed !=1:
            speed /= 2
            clickX = -1
            clickY = -1

        # speed up button
        button(10, 6, 2, 2, (100, 0, 0))
        if button(10, 6, 2, 2, (100, 0, 0)) and speed !=16:
            speed *=2
            clickX = -1
            clickY = -1
    #gamemode
        button(0,10, 2, 6,(100,100,100))
        if button(0,10, 2, 6,(100,100,100)):
            clickX = -1
            clickY = -1
            game_mode += 1
            if game_mode >= 3:
                game_mode = 0



        if game_mode == 0:
            text(2, 10, 'mode : pvp')
        if game_mode == 1:
            text(2, 10, 'mode : solo')
        if game_mode == 2:
            text(2,10,'guns')


    # text
        #speed
        text(7, 7, str(speed))
        text(7, 6, 'speed')
        #score
        text(0,0, ('last score: '+str(score)))


    if game and game_mode == 1:
        if ticks >= 20/speed:

            sec += 1
            ticks = 0
        # there will be in game keyboard management for phones, tablets, ect.
            clickX = -1
            clickY = -1

        # move
        if rec != sec and p1_alive:
            head1.move()
            head1.tailX.append(head1.ret_x())
            head1.tailY.append(head1.ret_y())
            action1 = True

        #tracking food and tails
            #food
        if head1.ret_x() == food1.ret_x() and head1.ret_y() == food1.ret_y():
            food1.eat()

        food1.tracker(head1)

            #tail
        head1.tailX = head1.tailX[-food1.ret_eaten() - 1:]
        head1.tailY = head1.tailY[-food1.ret_eaten() - 1:]

        #death check
        head1.check_eat_self()
        score = (food1.timesEaten-1) * speed

        #printing
        body(food1.ret_x(), food1.ret_y(), (100, 25, 0))
        head1.print(food1)
        if head1.is_dead():
            text(5,6,('score : '+str(score)))
            p1_alive = False

        if not p1_alive:
            if clickX != -1 or clickY != -1:
                game = False
                clickX = -1
                clickY = -1
                p1_alive = True
                head1.reset()
                food1.reset(0,0)
        set_map(fieldX, fieldY)

    
    if game and game_mode == 0:

        if ticks >= 20/speed:

            sec += 1
            ticks = 0

        if p1_alive:
            head1.print(food1)
        if p2_alive:
            head2.print(food2)




        if rec != sec:
            if p1_alive:
                head1.move()
                head1.tailX.append(head1.ret_x())
                head1.tailY.append(head1.ret_y())
                action1 = True


            if p2_alive:
                head2.move()
                head2.tailX.append(head2.ret_x())
                head2.tailY.append(head2.ret_y())
                action2 = True


        if not p1_alive:
            p1_score = (food1.timesEaten-1) * speed
            text(0, 0, str(p1_score))

        if not p2_alive:
            p2_score = (food2.timesEaten-1) * speed
            text(8, 0, str(p2_score))


        # tracking food and tails
            # food
        if head1.ret_x() == food1.ret_x() and head1.ret_y() == food1.ret_y():
            food1.eat()

        if head2.ret_x() == food2.ret_x() and head2.ret_y() == food2.ret_y():
            food2.eat()

        food1.tracker(head1)
        food2.tracker(head2)

        # tail
        head1.tailX = head1.tailX[-food1.ret_eaten() - 1:]
        head1.tailY = head1.tailY[-food1.ret_eaten() - 1:]

        head2.tailX = head2.tailX[-food2.ret_eaten() - 1:]
        head2.tailY = head2.tailY[-food2.ret_eaten() - 1:]

        #death check
        head2.check_eat_self()
        head1.check_eat_self()

        if head1.is_dead():
            p1_alive = False
        if head2.is_dead():
            p2_alive = False

        if not p1_alive and not p2_alive:
            if p1_score > p2_score:
                text(5,6,'player 1 won', (0, 75,25))

            if p2_score > p1_score:
                text(5,6,'player 2 won', (0, 25, 75))

            if p2_score == p1_score:
                text(6,6,'draw')

            if clickX != -1 or clickY != -1:
                game = False
                p1_alive = True
                p2_alive = True
                p1_score = 0
                p2_score = 0
                food1.reset(0, 0)
                food2.reset(8, 0)
                head1.reset(0, 0)
                head2.reset(8, 0)
                clickX = -1
                clickY = -1

        #printing
        body(food1.ret_x(), food1.ret_y(), (100, 25, 0))
        body(food2.ret_x(), food2.ret_y(), (100, 25, 0))
        set_map(fieldX, fieldY)
        pygame.draw.rect(screen, (100, 100, 100), ((8 * rectSize) - 1, 0, 3, 12 * rectSize))


    if game and game_mode == 2:
        if ticks >= 20 / speed:
            sec += 1
            ticks = 0
            # there will be in game keyboard management for phones, tablets, ect.
            clickX = -1
            clickY = -1

        # move
        if rec != sec and p1_alive:
            head3.move()
            head3.tailX.append(head3.ret_x())
            head3.tailY.append(head3.ret_y())
            action1 = True

        # tracking food and tails
        # food
        if head3.ret_x() == food1.ret_x() and head3.ret_y() == food1.ret_y():
            food1.eat()

        food1.tracker(head1)

        # tail
        head3.tailX = head3.tailX[-food1.ret_eaten() - 1:]
        head3.tailY = head3.tailY[-food1.ret_eaten() - 1:]

        # death check
        head3.check_eat_self()
        score = (food1.timesEaten - 1) * speed

        # printing
        body(food1.ret_x(), food1.ret_y(), (100, 25, 0))
        head3.print(food1)
        if head3.is_dead():
            text(5, 6, ('score : ' + str(score)))
            p1_alive = False

        if not p1_alive:
            if clickX != -1 or clickY != -1:
                game = False
                clickX = -1
                clickY = -1
                p1_alive = True
                head3.reset()
                food1.reset(0, 0)
        set_map(fieldX, fieldY)

    #text(0,0,str(clickX)+str(clickY))
    clickX = -1
    clickY = -1
    pygame.display.flip()
    clock.tick(fps)
    
    


