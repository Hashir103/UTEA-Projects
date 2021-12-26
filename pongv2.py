# UTEA August 14, 2019
# Get modules
import pygame
import sys
import time

# For getting screen resolution
import ctypes
user32 = ctypes.windll.user32

# Background colours
backgroundDark = (25, 25, 25)
backgroundLite = (200, 200, 200)

# Game resolution
screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)

# Launches game window for us
pygame.init()

# Create the window our game will take place in
gameWindow = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)

# Name of program
pygame.display.set_caption("Pong v2")

# Setup Text box on screen
font = pygame.font.Font('freesansbold.ttf', 16)
someText = font.render('Pong v2 - Press esc to exit', True, (255, 255, 255))
textRect = someText.get_rect()
textRect.center = (screenWidth//2, 25)

# Setup our clock so we can keep track of time
clock = pygame.time.Clock()

# Game Score variables
player1 = 0
player2 = 0
winningScore = 3

# Game Winning
font = pygame.font.Font('freesansbold.ttf', 16)
someText3 = font.render(f'First to {winningScore} wins ', True, (255, 255, 255))
textRect3 = someText3.get_rect()
textRect3.center = (screenWidth//2, 85)

# Game Score Text
font = pygame.font.Font('freesansbold.ttf', 32)
someText2 = font.render(f'{player1} - {player2}', True, (255, 255, 255))
textRect2 = someText2.get_rect()
textRect2.center = (screenWidth//2, 60)

class Ball:
    def __init__(self, xPos, yPos, radius, color, xSpeed = 0, ySpeed = 0):
        self.xPos = xPos
        self.yPos = yPos
        self.radius = radius
        self.color = color
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed


    def move(self):
        self.xPos += self.xSpeed
        self.yPos += self.ySpeed

    def wallDetect(self):

        # Variables used in and out of this class
        global player1
        global player2
        global font
        global winningScore
        global someText2

        # Right Wall
        if (self.xPos <= 0):
            player2  += 1
            someText2 = font.render(f'{player1} - {player2}', True, (255, 255, 255))
            gameWindow.blit(someText, textRect)
            gameWindow.blit(someText3, textRect3)
            gameWindow.blit(someText2, textRect2)
            leftPaddle.draw()
            rightPaddle.draw()
            
            pygame.display.update()
            time.sleep(1.5)
            gameBall.draw()
            self.xPos = screenWidth//2
            self.yPos = screenHeight//2
            self.xSpeed = 6
            self.ySpeed = 7

            if (player2 == winningScore):
                someText2 = font.render('The Ai has won! Restarting in 3 seconds..', True, (255, 0, 0))
                textRect2.center = (screenWidth/3, screenHeight//2)
                gameWindow.blit(someText2, textRect2)
                pygame.display.update()
                time.sleep(3)
                player1 = 0
                player2 = 0
                someText2 = font.render(f'{player1} - {player2}', True, (255, 255, 255))
                gameWindow.blit(someText, textRect)
                gameWindow.blit(someText3, textRect3)
                textRect2.center = (screenWidth//2, 60)
                gameWindow.blit(someText2, textRect2)
                leftPaddle.draw()
                rightPaddle.draw()
                gameBall.draw()
                pygame.display.update()
            
        # Left wall
        if (self.xPos + self.radius >= screenWidth):
            player1  += 1
            someText2 = font.render(f'{player1} - {player2}', True, (255, 255, 255))
            gameWindow.blit(someText, textRect)
            gameWindow.blit(someText3, textRect3)
            gameWindow.blit(someText2, textRect2)
            leftPaddle.draw()
            rightPaddle.draw()
            pygame.display.update()
            time.sleep(1.5)
            gameBall.draw()
            self.xPos = screenWidth//2
            self.yPos = screenHeight//2
            self.xSpeed = 6
            self.ySpeed = 7

            if (player1 == winningScore):
                textRect2.center = (screenWidth//3, screenHeight//2)
                someText2 = font.render("You won! Restarting in 3 seconds..", True, (0, 255, 0))
                gameWindow.blit(someText2, textRect2)
                pygame.display.update()
                time.sleep(3)
                player1 = 0
                player2 = 0
                someText2 = font.render(f'{player1} - {player2}', True, (255, 255, 255))
                gameWindow.blit(someText, textRect)
                gameWindow.blit(someText3, textRect3)
                textRect2.center = (screenWidth//2, 60)
                gameWindow.blit(someText2, textRect2)
                leftPaddle.draw()
                rightPaddle.draw()
                gameBall.draw()
                pygame.display.update()
        
        
        # Top or bottom wall
        if (self.yPos <= 0 or self.yPos + self.radius >= screenHeight):
            self.ySpeed *= -1

        someText2 = font.render(f'{player1} - {player2}', True, (255, 255, 255))
            
    def draw(self):
        pygame.draw.circle(gameWindow, self.color, (self.xPos, self.yPos), self.radius)

class Paddle:

    def __init__(self, xPos, yPos, width, height, color, speed = 10, isAi = False):
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.isAi = isAi
        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)

    def getBall(self, aBall):
        self.aBall = aBall
 
    def ballCollide(self):
        # 4 conditions must be met for this collide to work
        if (self.aBall.xPos >= self.xPos and self.aBall.xPos - self.aBall.radius <= self.xPos + self.width and self.aBall.yPos + self.aBall.radius >= self.yPos and self.aBall.yPos - self.aBall.radius <= self.yPos + self.height):
            self.aBall.xSpeed *= -1       
            if (self.aBall.xSpeed <-5 and self.aBall.xSpeed >-12):
                self.aBall.xSpeed += -1
                self.aBall.ySpeed += -1
            if (self.aBall.xSpeed >5 and self.aBall.xSpeed <12):
                self.aBall.xSpeed += 1
                self.aBall.ySpeed += 1

    def move(self):
        if (not self.isAi):
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                if (self.yPos - self.speed <= 0):
                    self.yPos = 0
                else:
                    self.yPos -= self.speed

            if pressed[pygame.K_DOWN]:
                if (self.yPos + self.speed >= screenHeight - self.height):
                    self.yPos = screenHeight - self.height
                self.yPos += self.speed

        else:
            # Ai moves up
            if (self.aBall.yPos < self.yPos):
               self.yPos -= self.speed
            # Ai moves down
            elif (self.aBall.yPos > self.yPos + self.height):
                self.yPos += self.speed

        self.rect = pygame.Rect(self.xPos, self.yPos, self.width, self.height)
            
    
    def draw(self):
        pygame.draw.rect(gameWindow, self.color, self.rect)
        
gameBall = Ball (screenWidth//2, screenHeight//2, 8,(255, 255, 255), 6, 7)
leftPaddle = Paddle (screenWidth/50, screenHeight/6, screenWidth/100, screenHeight/8, (255, 255, 255), 8)
rightPaddle = Paddle (screenWidth - screenWidth/50, screenHeight/6, screenWidth/100, screenHeight/8, (255, 255, 255), 8, True)

# Main game loop
# While loop - Condition is forever
while True:
    pressed = pygame.key.get_pressed()
    # Iterates through the events pygame is tracking
    for  event in pygame.event.get():

        # Checks one event to see if it is a quit event
        if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
            
            # If it is a quit game, quit pygame and exit sys
            pygame.quit()
            sys.exit()

    # Fills our game window background with a colour of our choice
    gameWindow.fill(backgroundDark)

    # Draw ball and paddles & boundaries
    gameBall.move()

    leftPaddle.getBall(gameBall)
    rightPaddle.getBall(gameBall)
    leftPaddle.move()
    rightPaddle.move()

    # Ball detect
    leftPaddle.ballCollide()
    rightPaddle.ballCollide()
    gameBall.wallDetect()
    
    # Draw ball
    gameBall.draw()
    leftPaddle.draw()
    rightPaddle.draw()

    # Draw text
    gameWindow.blit(someText, textRect)
    gameWindow.blit(someText2, textRect2)
    gameWindow.blit(someText3, textRect3)

    # Updates the gameWindow's graphics
    pygame.display.update()

    # Sets maximum framerate of game
    clock.tick(60)
