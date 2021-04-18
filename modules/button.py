import pygame

# Button class
class Button:
    def __init__(self, screen, x, y, w, h, text, call_back):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.call_back = call_back

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (220, 220, 220)
    color = WHITE

    def click(self, click_position):
        x, y = click_position
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            self.call_back()

    def hover(self, hover_position):
        x, y = hover_position
        if self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h:
            self.color = self.GREY
            self.draw_button()
        else:
            self.color = self.WHITE
            self.draw_button()

    def draw_button(self):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(self.screen, self.color, rect)
        outline = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(self.screen, self.BLACK, outline, 3)
        FONT = pygame.font.SysFont('comicsans', 45)
        text = FONT.render(self.text, 1, self.BLACK)
        position = (self.x + (self.w  - text.get_width()) // 2, self.y + (self.h - text.get_height()) // 2)
        self.screen.blit(text, position)