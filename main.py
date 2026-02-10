import pygame
import sys
from gameplay.game import Gameplay  # importa a classe, mas não roda o jogo

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
        self.estado = "menu"  # menu | select_players

        mid_x = SCREEN_WIDTH // 2 - 160
        start_y = SCREEN_HEIGHT // 2
        gap = 90

        self.background = pygame.image.load(
            "Assets/images/homeless_war_background.jpeg"
        ).convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_WIDTH - 290, SCREEN_HEIGHT)
        )

        # --- BOTÕES DO MENU PRINCIPAL ---
        self.menu_buttons = [
            Button("Iniciar Jogo", (mid_x, start_y), self.ir_select_players),
            Button("Opções", (mid_x, start_y + gap), self.show_options),
            Button("Sair", (mid_x, start_y + 2 * gap), self.exit_game),
        ]

        # --- BOTÕES DE SELEÇÃO DE JOGADORES ---
        self.player_buttons = [
            Button("1 Jogador", (mid_x, start_y), lambda: self.start_game(1)),
            Button("2 Jogadores", (mid_x, start_y + gap), lambda: self.start_game(2)),
            Button("Voltar", (mid_x, start_y + 2 * gap), self.voltar_menu),
        ]

        self.running = True

    # ===== CALLBACKS =====
    def ir_select_players(self):
        self.estado = "select_players"

    def voltar_menu(self):
        self.estado = "menu"

    def start_game(self, modo_jogo):
        print(f"Iniciando jogo com {modo_jogo} jogador(es)")
        game = Gameplay(self.screen, modo_jogo)
        game.loop()

    def show_options(self):
        print("Abrindo opções...")

    def exit_game(self):
        pygame.quit()
        sys.exit()

    # ===== DRAW =====
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        if self.estado == "menu":
            for btn in self.menu_buttons:
                btn.draw(self.screen, mouse_pos)

        elif self.estado == "select_players":
            for btn in self.player_buttons:
                btn.draw(self.screen, mouse_pos)

    # ===== LOOP =====
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.estado == "menu":
                        for btn in self.menu_buttons:
                            btn.check_click(mouse_pos)

                    elif self.estado == "select_players":
                        for btn in self.player_buttons:
                            btn.check_click(mouse_pos)

            self.draw()
            pygame.display.update()

# === Rodar o menu principal ===
if __name__ == "__main__":
    menu = Menu(screen)
    menu.run()
