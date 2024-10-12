import pygame
import sys
from ui_elements import Button, Text, Image

class Window():
    def __init__(self, screen, backgroundColour = "white"):
        self.screen = screen
        self.buttons = []
        self.texts = []
        self.images = []
        self.backgroundColour = backgroundColour

    def update(self):
        self.screen.fill(self.backgroundColour)
        for image in self.images:
            image.update(self.screen)
        for text in self.texts:
            text.update(self.screen)
        for button in self.buttons:
            button.update(self.screen)

    def handleEvents(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.inputTest(pygame.mouse.get_pos()):
                            if button.function:
                                return button.function()

    def execute(self):
        self.update()
        pygame.display.update()
        self.handleEvents()

    def addButton(self, positionX, positionY, image, function=None, width=700, height=200):
        button_surface = pygame.transform.scale(image, (width, height))
        button = Button(button_surface, positionX, positionY, function)
        self.buttons.append(button)

    def addText(self, font, text, positionX, positionY, colour="white"):
        text = Text(font, text, positionX, positionY, colour)
        self.texts.append(text)

    def addImage(self, width, height, positionX, positionY, image):
        image_surface = pygame.transform.scale(image, (width, height))
        self.images.append(Image(image_surface, positionX, positionY))