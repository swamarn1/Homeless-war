import pygame

pygame.init()

# ================= GAMEPLAY =================
class Gameplay:
    def __init__(self, screen, num_players=1):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.num_players = num_players

        # ================= CONFIG =================
        self.velocidade_andar = 6
        self.forca_pulo = -20
        self.gravidade = 1

        self.player_width = 125
        self.player_height = 125
        self.chao_y = self.screen.get_height() // 2 + 330

        # ================= PLAYER =================
        self.p1 = self.create_player(self.screen.get_width() // 2 - 200)
        self.p2 = (
            self.create_player(self.screen.get_width() // 2 + 200)
            if self.num_players == 2 else None
        )

        # ================= BACKGROUND =================
        self.background = pygame.image.load(
            "Assets/images/cenario_certo.png"
        ).convert()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )

    # ================= PLAYER BASE =================
    def create_player(self, x):
        return {
            "x": x,
            "y": self.chao_y,
            "y_vel": 0,
            "no_chao": True,
            "virado_esquerda": False,
            "current_animation": None,
            "current_frame": 0,
            "animation_timer": 0,
            "idle": self.load_animation(
                ["Assets/images/mendigos/jose_idle.png"]
            ),
        }

    def load_animation(self, paths):
        frames = []
        for path in paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(
                img, (self.player_width, self.player_height)
            )
            frames.append(img)
        return frames

    def update_animation(self, p):
        p["animation_timer"] += 0.15
        if p["animation_timer"] >= 1:
            p["animation_timer"] = 0
            p["current_frame"] = (
                p["current_frame"] + 1
            ) % len(p["current_animation"])

    # ================= LOOP =================
    def loop(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.handle_player(
                self.p1, keys,
                pygame.K_a, pygame.K_d, pygame.K_w
            )

            if self.p2:
                self.handle_player(
                    self.p2, keys,
                    pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP
                )

            self.draw()

    # ================= PLAYER CONTROL =================
    def handle_player(self, p, keys, left, right, jump):
        # --- MOVIMENTO HORIZONTAL ---
        if keys[left]:
            p["x"] -= self.velocidade_andar
            p["virado_esquerda"] = True

        if keys[right]:
            p["x"] += self.velocidade_andar
            p["virado_esquerda"] = False

        # --- PAREDES ---
        p["x"] = max(
            0,
            min(p["x"], self.screen.get_width() - self.player_width)
        )

        # --- PULO ---
        if keys[jump] and p["no_chao"]:
            p["y_vel"] = self.forca_pulo
            p["no_chao"] = False

        # --- GRAVIDADE ---
        p["y_vel"] += self.gravidade
        p["y"] += p["y_vel"]

        # --- CHÃO ---
        if p["y"] >= self.chao_y:
            p["y"] = self.chao_y
            p["y_vel"] = 0
            p["no_chao"] = True

        # --- ANIMAÇÃO ---
        p["current_animation"] = p["idle"]
        self.update_animation(p)

    # ================= DRAW =================
    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.draw_player(self.p1)
        if self.p2:
            self.draw_player(self.p2)

        pygame.display.update()

    def draw_player(self, p):
        img = p["current_animation"][p["current_frame"]]
        if p["virado_esquerda"]:
            img = pygame.transform.flip(img, True, False)
        self.screen.blit(img, (p["x"], p["y"]))

# ================= START PARA TESTE =================
if __name__ == "__main__":
    LARGURA, ALTURA = 1280, 720
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Homeless War")
    game = Gameplay(screen, num_players=1)
    game.loop()
    pygame.quit()
