# A non copyrighted version of Floppy Bird
# Hashir Sami
# UTEA August 14, 2019

import random
import pygame
import sys
import os

class FlappyBird():

    def __init__(self):

        # Environment parameters
        self.screenWidth = 800
        self.screenHeight = 600
        
        # Game parameters
        self.gravity = 0.25
        self.gameSpeed = 5
        self.score = 0
        self.frame = 0
        self.bird = Bird()
        self.pipes = []
        # Background Parameters
        self.image = pygame.image.load("background.png")
        self.imgRect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.screenWidth, self.screenHeight))

        pygame.init()
        self.gameWindow = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()

    def applyGravity(self):
        self.bird.ySpeed += self.gravity

    def runGame(self):
        self.generatePipe(100, 200)
        while True:
            pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()
                # if pressed[pygame.K_F5]:
                #     os.execl('flappybird.py')

                    
            self.frame += 1
            
            self.bird.flap()
            self.applyGravity()
            self.bird.updatePosition()

            if (self.frame % 120 == 0):
                self.generatePipe(100,200)
                
            self.gameWindow.blit(self.image, self.imgRect)
            self.gameWindow.blit(self.bird.birdImage, self.bird.birdRect)
            self.drawPipes()

            pygame.display.update()

            self.checkCollision()

            self.clock.tick(60)

    def generatePipe(self, minHeight, maxHeight):
        
        height = random.randint(minHeight, maxHeight)
        top = random.randint(0, self.screenHeight - height)
        
        self.pipes.append(Pipe( self.screenWidth + 10, top, 80, height, self.screenHeight))

    def drawPipes(self):
        
        for pipe in self.pipes:
            pipe.move(self.gameSpeed)
            self.gameWindow.blit(pipe.pipe1Image, pipe.pipe1Rect)
            self.gameWindow.blit(pipe.pipe2Image, pipe.pipe2Rect)

        if self.pipes[0].left + self.pipes[0].width < 0:
            self.pipes.pop(0)

    def checkCollision(self):
        if self.bird.birdRect.colliderect(self.pipes[0].pipe1Rect) or self.bird.birdRect.colliderect(self.pipes[0].pipe2Rect):
            self.gameSpeed = 0
                
        
        
class Bird:

    def __init__(self):
        self.size = 30
        self.xPos = 40
        self.yPos = 300
        self.thrust = -1
        self.ySpeed = 0
        
        self.birdImage = pygame.image.load("bird.png")
        self.birdImage = pygame.transform.scale(self.birdImage, (self.size, self.size))
        self.birdRect = self.birdImage.get_rect()
        self.birdRect = self.birdRect.move( (self.xPos, self.yPos) )

    def flap(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.ySpeed += self.thrust

    def updatePosition(self):
        self.yPos += self.ySpeed
        if (self.yPos <= 0):
            self.yPos = 0
            self.ySpeed = 0
        elif (self.yPos + self.size >= 600):
            self.yPos = 600 - self.size
            self.ySpeed = 0

        self.birdRect.top = self.yPos
        
            
class Pipe():

    def __init__(self, left, top, width, height, screenHeight):
        self.left = left
        self.top = top
        self.height = height
        self.width = width

        self.pipe1Rect = pygame.Rect(self.left, 0, self.width, self.top)
        self.pipe1Image = pygame.image.load("pipe.png")
        self.pipe1Image = pygame.transform.scale(self.pipe1Image, (self.width, self.top))

        self.pipe2Rect = pygame.Rect(self.left, self.top + self.height, self.width, screenHeight - self.top - self.height)
        self.pipe2Image = pygame.image.load("pipe.png")
        self.pipe2Image = pygame.transform.scale(self.pipe2Image, (self.width, screenHeight - self.top - self.height))
        self.pipe2Image = pygame.transform.flip(self.pipe2Image, False, True)

    def move(self, gameSpeed):
        self.left -= gameSpeed
        self.pipe1Rect.left = self.left
        self.pipe2Rect.left = self.left

game = FlappyBird()
game.runGame()
