import pygame

from board import Board


class GUI:
    """
    Contains & shows:
    - moves
    - revert button
    - restart button
    - start button
    - stop button
    - save button
    - load button
    """

    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 20)

        self.undo_btn = self.font.render('undo', True, (0, 0, 0))
        self.start_btn = self.font.render('start', True, (0, 0, 0))
        self.stop_btn = self.font.render('stop', True, (0, 0, 0))
        self.restart_btn = self.font.render('restart', True, (0, 0, 0))
        self.save_btn = self.font.render('save', True, (0, 0, 0))
        self.load_btn = self.font.render('load', True, (0, 0, 0))

        self.undo_btn_hover = False
        self.start_btn_hover = False
        self.stop_btn_hover = False
        self.restart_btn_hover = False
        self.save_btn_hover = False
        self.load_btn_hover = False

        self.padding = 5
        self.btn_width = 100
        self.btn_height = 30
        self.btn_color = (200, 120, 100)
        self.btn_hover_color = (200-30, 120-30, 100-30)


    def handle_mouse(self, mx, my, is_click=False, board=None):
        self.restart_btn_hover = False
        self.start_btn_hover = False
        self.stop_btn_hover = False
        self.undo_btn_hover = False
        self.save_btn_hover = False
        self.load_btn_hover = False

        if mx >= self.padding and mx <= self.padding + self.btn_width and my >= 605 and my <= 605 + self.btn_height:
            self.restart_btn_hover = True
            if is_click and board is not None:
                board.restart()
        if mx >= self.padding and mx <= self.padding + self.btn_width and my >= 640 and my <= 640 + self.btn_height:
            self.start_btn_hover = True
            if is_click and board is not None:
                pass
        if mx >= self.padding and mx <= self.padding + self.btn_width and my >= 675 and my <= 675 + self.btn_height:
            self.stop_btn_hover = True
            if is_click and board is not None:
                pass

        x = self.padding + self.btn_width + 2*self.padding
        if mx >= x and mx <= x + self.btn_width and my >= 605 and my <= 605 + self.btn_height:
            self.undo_btn_hover = True
            if is_click and board is not None:
                pass
        if mx >= x and mx <= x + self.btn_width and my >= 640 and my <= 640 + self.btn_height:
            self.save_btn_hover = True
            if is_click and board is not None:
                board.save()
        if mx >= x and mx <= x + self.btn_width and my >= 675 and my <= 675 + self.btn_height:
            self.load_btn_hover = True
            if is_click and board is not None:
                board.load()


    def draw(self, display):
        
        # first col
        pygame.draw.rect(display, self.btn_hover_color if self.restart_btn_hover else self.btn_color, [self.padding, 605, self.btn_width, self.btn_height])
        display.blit(self.restart_btn, (10, 607))

        pygame.draw.rect(display, self.btn_hover_color if self.start_btn_hover else self.btn_color, [self.padding, 640, self.btn_width, self.btn_height])
        display.blit(self.start_btn, (10, 642))

        pygame.draw.rect(display, self.btn_hover_color if self.stop_btn_hover else self.btn_color, [self.padding, 675, self.btn_width, self.btn_height])
        display.blit(self.stop_btn, (10, 679))

        # second col
        x = self.padding + self.btn_width + 2*self.padding
        pygame.draw.rect(display, self.btn_hover_color if self.undo_btn_hover else self.btn_color, [x, 605, self.btn_width, self.btn_height])
        display.blit(self.undo_btn, (x + 10, 607))

        pygame.draw.rect(display, self.btn_hover_color if self.save_btn_hover else self.btn_color, [x, 640, self.btn_width, self.btn_height])
        display.blit(self.save_btn, (x + 10, 642))

        pygame.draw.rect(display, self.btn_hover_color if self.load_btn_hover else self.btn_color, [x, 675, self.btn_width, self.btn_height])
        display.blit(self.load_btn, (x + 10, 679))


