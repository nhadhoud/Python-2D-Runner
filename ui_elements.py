class Button():
    def __init__(self, image, positionX, positionY, function):
        self.image = image
        self.positionX = positionX
        self.positionY = positionY
        self.rect = self.image.get_rect(center = (self.positionX,self.positionY))
        self.function = function

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def inputTest(self, position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            return True


class Text():
    def __init__(self,font,text,positionX,positionY,colour):
        self.font = font
        self.positionX = positionX
        self.positionY = positionY
        self.colour = colour
        self.text_surface = font.render((text),True,self.colour)

    def update(self, screen):
        screen.blit(self.text_surface,(self.positionX,self.positionY))

    def setText(self,text):
        self.text_surface = self.font.render((text),True,self.colour)
        

class Image():
    def __init__(self,image_surface,positionX,positionY):
        self.positionX = positionX
        self.positionY = positionY
        self.image_surface = image_surface
        self.rect = image_surface.get_rect(center = (self.positionX,self.positionY))

    def update(self, screen):
        screen.blit(self.image_surface, self.rect)