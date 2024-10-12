import sys
import pygame
from leaderboard_db import LeaderBoardDataBase
from window import Window
from game_window import GameWindow

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

FONT1 = pygame.font.SysFont("Impact", 90)
FONT2 = pygame.font.SysFont("Impact", 75)

BUTTON_WIDTH = SCREEN_WIDTH/3
BUTTON_HEIGHT = SCREEN_HEIGHT/5


MAX_NAME_LENGTH = 15


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def quitGame():
    if nameMenu.name:
        leaderboardDB.update(nameMenu.name, gameScreen.score)
    pygame.quit()
    sys.exit()

#preload images

def loadImage(imagePath):
    try:
        return pygame.image.load(imagePath)
    except:
        print(f"Could not load image {imagePath}")
        quitGame()

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


leaderboardDB = LeaderBoardDataBase()

CentreX = SCREEN_WIDTH/2

class GameScreen(GameWindow):
    def setup(self, nameWindow, pauseWindow, mainWindow):
        self.nameWindow = nameWindow
        self.pauseWindow = pauseWindow
        self.mainWindow = mainWindow
        self.addButton(SCREEN_WIDTH-20, 20, images["pauseButton"], pauseWindow.execute, 50, 50)
        self.addText(FONT2, str(self.score), 10, 0)
        self.setObstacleImage(images["obstacle"])
        self.addObstacles()

    def execute(self):
        self.updateAll()
        self.handleEvents()

    def handleEvents(self): 
        while self.nameWindow.name == "":
            self.nameWindow.execute()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.pauseWindow.execute()
                    if event.key == pygame.K_SPACE:
                        self.character.changeDirection()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.inputTest(pygame.mouse.get_pos()):
                            break

            self.texts[0].setText(str(self.score))
            self.updateAll()

            if self.checkCompletion():
                self.addObstacles()

            if self.checkCollision():
                leaderboardDB.update(self.nameWindow.name, self.score)
                self.restart()
                return(self.mainWindow.execute())
            
            pygame.display.update()

class LeaderBoard(Window):
    def setup(self, mainWindow):
        self.addButton(SCREEN_WIDTH/5, SCREEN_HEIGHT/9, images["menuButton"], mainWindow.execute)
        self.addButton(SCREEN_WIDTH/5, SCREEN_HEIGHT/3, images["quitButton"], quitGame)
        self.addImage(BUTTON_WIDTH*1.8, BUTTON_HEIGHT*9, SCREEN_WIDTH*9/13, SCREEN_HEIGHT/2, images["blankButton"])

    def update(self):
        self.texts.clear()
        topPlayers = leaderboardDB.getTopPlayers()
        for i, (playerName, highScore) in enumerate(topPlayers):
                self.addText(FONT1, f"{i+1}. {playerName}:", SCREEN_WIDTH*3/7, SCREEN_HEIGHT*1.5*i/10)
                self.addText(FONT1, str(highScore), SCREEN_WIDTH*6/7, SCREEN_HEIGHT*1.5*i/10)
            
        if nameMenu.name:
            playerRank = leaderboardDB.getPlayerRank(nameMenu.name)
            playerHighScore = leaderboardDB.getPlayer(nameMenu.name)[1]
            self.addText(FONT1, f"{playerRank}. {nameMenu.name}", SCREEN_WIDTH*3/7, SCREEN_HEIGHT*8/10)
            self.addText(FONT1, f"{playerHighScore}", SCREEN_WIDTH*6/7, SCREEN_HEIGHT*8/10)
        super().update()

class NameMenu(Window):
    def __init__(self, screen):
        super().__init__(screen)
        self.name = ""

    def setup(self, gameWindow):
        self.gameWindow = gameWindow
        self.addText(FONT1, "Enter Your Name Here", SCREEN_WIDTH*0.3, SCREEN_HEIGHT*0.45)
        self.addButton(CentreX, SCREEN_HEIGHT-150,  images["confirmButton"], gameWindow.execute)
        self.addImage(BUTTON_WIDTH*1.3, BUTTON_HEIGHT, CentreX, SCREEN_HEIGHT/2, images["blankButton"])

    def handleEvents(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.inputTest(pygame.mouse.get_pos()):
                            if leaderboardDB.getPlayer(self.name):
                                self.name = ""
                                self.texts[0].setText("This Name Is Taken")
                                self.update()
                            else:
                                leaderboardDB.update(self.name, self.gameWindow.score)
                            return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif len(self.name) < MAX_NAME_LENGTH:
                        self.name += event.unicode
                    self.texts[0].setText(self.name)
                    self.update()
                    pygame.display.update()


class PauseMenu(Window):
    def setup(self, gameWindow, mainWindow):
        self.addButton(CentreX, SCREEN_HEIGHT/3-180, images["resumeButton"], gameWindow.execute)
        self.addButton(CentreX, SCREEN_HEIGHT*2/3-180, images["restartButton"], gameWindow.restart)
        self.addButton(CentreX, SCREEN_HEIGHT-180, images["menuButton"], mainWindow.execute)

class MainMenu(Window):
    def setup(self, gameWindow, leaderboardWindowReference):
        self.addButton(CentreX, SCREEN_HEIGHT/3-180, images["playButton"], gameWindow.execute)
        self.addButton(CentreX, SCREEN_HEIGHT*2/3-180, images["leaderboardButton"], leaderboardWindowReference.execute)
        self.addButton(CentreX, SCREEN_HEIGHT-180, images["quitButton"], quitGame)


mainMenu = MainMenu(screen)
leaderboardScreen = LeaderBoard(screen)
nameMenu = NameMenu(screen)
pauseMenu = PauseMenu(screen)
gameScreen = GameScreen(screen)

#windows must first be instantiated before they are allowed to reference each other
mainMenu.setup(gameScreen, leaderboardScreen)
leaderboardScreen.setup(mainMenu)
nameMenu.setup(gameScreen)
pauseMenu.setup(gameScreen, mainMenu)
gameScreen.setup(nameMenu, pauseMenu, mainMenu)
mainMenu.execute()