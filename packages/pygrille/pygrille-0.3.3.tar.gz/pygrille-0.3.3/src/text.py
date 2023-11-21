import pygame
import os.path


class Text:
    def __init__(self, font: str = None, size: int = None, text: str = None, pos: tuple = None, colour: tuple = None):
        """
        Initializes a Text object with the given font, size, text, position and color.
        If any of the arguments are not provided, default values are used.
        """
        if font is None:
            font = "Arial"
        if size is None:
            size = 30
        if text is None:
            text = ""
        if pos is None:
            pos = (0,0)
        if colour is None:
            colour = (0,0,0)
        self.fontstr = font
        self.font = None
        self.size = size
        self.text = text
        self.pos = pos
        self.colour = colour
        self.render = None
        self.makefont()
        self.rendertext()

    def makefont(self):
        """
        Creates a font object from the given font name and size.
        If the font name is a path to a font file, the font is loaded from that file.
        Otherwise, the system font is used.
        """
        if os.path.exists(self.fontstr):
            self.font = pygame.font.Font(self.font, self.size)
        else:
            self.font = pygame.font.SysFont(self.fontstr, self.size)

    def rendertext(self):
        """
        Renders the text using the current font and color, and updates the 'render' attribute.
        """
        self.render = self.font.render(self.text, False, self.colour)

    def draw(self, screen: pygame.Surface):
        """
        Draws the text on the given screen surface at the current position.
        """
        screen.blit(self.render, (self.pos[0], self.pos[1]))

    def get_text(self):
        """
        Returns the current text of the object
        """
        return self.text

    def set_text(self, text: str):
        """
        Sets the text of the object to the given text and updates the render
        """
        self.text = text
        self.rendertext()

    def change_font(self, font: str):
        """
        Changes the font of the text object and updates the render
        """
        self.font = font
        self.makefont()
        self.rendertext()

    def change_size(self, size: int):
        """
        Changes the size of the font and updates the render
        """
        self.size = size
        self.makefont()
        self.rendertext()

    def move(self, newpos: tuple):
        """
        Changes the position of the text object
        """
        self.pos = newpos

    def change_colour(self, colour: tuple):
        """
        Changes the color of the text object and updates the render
        """
        self.colour = colour