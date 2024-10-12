import sys
import pygame
import random
from leaderboard_db import LeaderBoardDataBase
from window import Window

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FONT1 = pygame.font.SysFont("Impact", 90)
FONT2 = pygame.font.SysFont("Impact", 75)

BUTTON_WIDTH = SCREEN_WIDTH / 3
BUTTON_HEIGHT = SCREEN_HEIGHT / 5

MAX_NAME_LENGTH = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Preload images
def loadImage(imagePath):
    try:
        return pygame.image.load(imagePath)
    except:
        print(f"Could not load image {imagePath}")
        sys.exit()

images = {
    "playButton": loadImage("assets/playbutton.png"),
    "leaderboardButton": loadImage("assets/leaderboardbutton.png"),
    "quitButton": loadImage("assets/quitbutton.png"),
    "menuButton": loadImage("assets/menubutton.png"),
    "resumeButton": loadImage("assets/resumebutton.png"),
    "restartButton": loadImage("assets/restartbutton.png"),
    "confirmButton": loadImage("assets/confirmbutton.png"),
    "pauseButton": loadImage("assets/pausebutton.png"),
    "blankButton": loadImage("assets/blankbutton.png"),
    "characterUp": loadImage("assets/characterUp.png"),
    "characterDown": loadImage("assets/characterDown.png"),
    "obstacle": loadImage("assets/obstacle.png")
}

class Character():
    def __init__(self):
        self.change_direction = False
        self.startingPosition = [50, 500]
        self.speed = 1.3
        self.positionX = self.startingPosition[0]
        self.positionY = self.startingPosition[1]
        self.size = 40
        self.name = ""

    def changeDirection(self):
        self.change_direction = not self.change_direction

    def move(self):
        self.positionX += self.speed
        if self.change_direction:
            self.positionY += self.speed
        else:
            self.positionY -= self.speed

    def resetPosition(self):
        self.positionX = self.startingPosition[0]
        self.positionY = self.startingPosition[1]

    def resetSpeed(self):
        self.speed = 1.3

    def update(self):
        if self.change_direction:
            characterImage = images["characterDown"]
        else:
            characterImage = images["characterUp"]
        self.move()
        characterImage = pygame.transform.scale(characterImage, (self.size, self.size))
        screen.blit(characterImage, (self.positionX, self.positionY))


class Obstacle():
    image = None
    def __init__(self, characterX, characterY, characterMinimumDistance):
        self.image = None
        self.minSize = 90
        self.maxSize = 180
        self.size = random.randint(self.minSize, self.maxSize)
        self.positionX = random.randint(0, SCREEN_WIDTH - self.size)
        self.positionY = random.randint(0, SCREEN_HEIGHT - self.size)
        while self.positionX < characterX + characterMinimumDistance and \
                self.positionY < characterY + characterMinimumDistance and \
                self.positionY > characterY - characterMinimumDistance:
            self.positionX = random.randint(0, SCREEN_WIDTH - self.size)
            self.positionY = random.randint(0, SCREEN_HEIGHT - self.size)

    def update(self):
        if Obstacle.image != None:
            image = pygame.transform.scale(Obstacle.image, (self.size, self.size))
            screen.blit(image, (self.positionX, self.positionY))

    def collisionDetection(self, positionX, positionY, size):
        if ((positionX < self.positionX and positionX + size > self.positionX) or
            (positionX > self.positionX and positionX < self.positionX + self.size)) and \
           ((positionY < self.positionY and positionY + size > self.positionY) or
            (positionY > self.positionY and positionY < self.positionY + self.size)) or \
            positionY >= SCREEN_HEIGHT - size or positionY <= 0:
            return True
        return False


class GameWindow(Window):
    def __init__(self, screen):
        super().__init__(screen, "black")
        self.characterObstacleBuffer = 300
        self.obstacles = []
        self.totalObstacles = 6
        self.maxObstacles = 12
        self.score = 0
        self.character = Character()

    def updateAll(self):
        self.update()
        self.character.update()
        for obstacle in self.obstacles:
            obstacle.update()

    def restart(self):
        self.score = 0
        self.character.resetPosition()
        self.character.resetSpeed()
        self.addObstacles()

    def addObstacles(self):
        while True:
            self.obstacles.clear()
            for i in range(self.totalObstacles):
                obstacle = Obstacle(self.character.startingPosition[0], self.character.startingPosition[1], self.characterObstacleBuffer)
                self.obstacles.append(obstacle)

            grid = []
            gridSize = self.character.size
            gridWidth = SCREEN_WIDTH // gridSize
            gridHeight = SCREEN_HEIGHT // gridSize

            for i in range(gridHeight):
                gridRow = []
                for j in range(gridWidth):
                    collision = False
                    testPositionX = SCREEN_WIDTH // gridSize * j
                    testPositionY = SCREEN_HEIGHT // gridSize * i
                    for n in range(len(self.obstacles)):
                        if self.obstacles[n].collisionDetection(testPositionX, testPositionY, gridSize):
                            collision = True
                            break
                    gridRow.append(True if collision else False)
                grid.append(gridRow)

            # Test level is valid using player movement
            unvisited = []
            current = (self.character.startingPosition[1] // gridHeight, self.character.startingPosition[0] // gridWidth)
            unvisited.append(current)

            while unvisited:
                current = unvisited.pop(0)
                row = current[0]
                col = current[1]
                if col == gridWidth - 1:
                    return
                if (row + 1, col + 1) not in unvisited and row + 1 < gridHeight and col + 1 < gridWidth and grid[row + 1][col + 1] == False:
                    unvisited.append((row + 1, col + 1))
                if (row - 1, col + 1) not in unvisited and row - 1 >= 0 and row - 1 <= gridHeight and col + 1 <= gridWidth and grid[row - 1][col + 1] == False:
                    unvisited.append((row - 1, col + 1))
                if (row, col + 1) not in unvisited and row <= gridHeight and col + 1 < gridWidth and grid[row][col + 1] == False:
                    unvisited.append((row, col + 1))

    def setObstacleImage(self, image):
        Obstacle.image = image

    def checkCompletion(self):
        if self.character.positionX >= SCREEN_WIDTH - self.character.size:
            self.character.resetPosition()
            self.score += 50
            if self.character.speed < 1.4:
                self.character.speed = self.character.speed * 1.06
            if self.totalObstacles < self.maxObstacles:
                self.totalObstacles += 2
            self.addObstacles()
            return True

    def checkCollision(self):
        for i in range(len(self.obstacles)):
            if self.obstacles[i].collisionDetection(self.character.positionX, self.character.positionY, self.character.size):
                return True
        return False


class Game:
    def __init__(self):
        self.gameScreen = GameWindow(screen, images)
        self.leaderBoardDB = LeaderBoardDataBase()

    def run(self):
        while self.gameScreen.character.name == "":
            self.nameSelection()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.leaderBoardDB.update(self.gameScreen.character.name, self.gameScreen.score)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.pauseMenu()
                    if event.key == pygame.K_SPACE:
                        self.gameScreen.character.changeDirection()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.gameScreen.buttons:
                        if button.inputTest(pygame.mouse.get_pos()):
                            break

            self.gameScreen.character.move()
            self.gameScreen.texts[0].setText(str(self.gameScreen.score))
            self.gameScreen.updateAll()
            self.gameScreen.checkCompletion()

            if self.gameScreen.checkCollision():
                self.leaderBoardDB.update(self.gameScreen.character.name, self.gameScreen.score)
                self.gameScreen.restart()
                return self.menuScreen()

            pygame.display.update()

    def restartGame(self):
        self.gameScreen.restart()
        return self.run()

