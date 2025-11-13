import pygame
import sys
from gameplay.game import Gameplay

pygame.init()

# === Configurações da tela ===
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Homeless War")
FONT = pygame.font.Font("Assets/Fonts/PressStart2P-Regular.ttf", 50)

WHITE = (255, 255, 255)
HIGHLIGHT = (249, 178, 51)

# === Classe do botão ===
class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.callback = callback
        self.default_color = WHITE
        self.highlight_color = HIGHLIGHT
        self.label_default = FONT.render(self.text, True, self.default_color)
        self.label_highlight = FONT.render(self.text, True, self.highlight_color)
        self.rect = self.label_default.get_rect(center=pos)

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            surface.blit(self.label_highlight, self.rect)
        else:
            surface.blit(self.label_default, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

# === Classe do menu ===
class Menu:
    def __init__(self, screen):
        self.screen = screen
        mid_x = SCREEN_WIDTH // 2 - 160
        start_y = SCREEN_HEIGHT // 2
        gap = 90

        self.background = pygame.image.load("Assets/images/homeless_war_background.jpeg").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH - 290, SCREEN_HEIGHT ))

        self.buttons = [
            Button("Iniciar Jogo", (mid_x, start_y), self.start_game),
            Button("Opções", (mid_x, start_y + gap), self.show_options),
            Button("Sair", (mid_x, start_y + 2 * gap), self.exit_game),
        ]

        self.running = True

    def start_game(self):
        game = Gameplay(self.screen)
        game.loop()

    def show_options(self):
        print("Abrindo opções...")

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.draw(self.screen, mouse_pos)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            self.draw()
            pygame.display.update()

# === Rodar o menu principal ===
if __name__ == "__main__":
    menu = Menu(screen)
    menu.run()
