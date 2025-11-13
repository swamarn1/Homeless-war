import pygame

class Gameplay:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.speed = 10
        self.running = True
        
        # --- hitbox ---
        self.hitbox_largura = 135
        self.hitbox_altura = 200

        # --- Tamanho da imagem ---
        self.imagem_largura = 200
        self.imagem_altura = 200

        # --- Pega a resolução da tela ---
        info = pygame.display.Info()
        self.largura, self.altura = info.current_w, info.current_h

        # --- Centraliza o personagem (pela hitbox) ---
        self.x = self.largura // 2 - self.hitbox_largura // 2
        self.y = self.altura // 2 - self.hitbox_altura // 2

        # --- Background ---
        self.background = pygame.image.load("Assets/images/preto.png").convert()
        self.background = pygame.transform.scale(self.background, (self.largura, self.altura))

        # --- Player ---
        self.player_image = pygame.image.load("Assets/images/mendigos/jose_idle#1.png").convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (self.imagem_largura, self.imagem_altura))

    def loop(self):
        while self.running:
            self.clock.tick(60)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Movimento
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.x -= self.speed
            if keys[pygame.K_d]:
                self.x += self.speed
            if keys[pygame.K_w]:
                self.y -= self.speed
            if keys[pygame.K_s]:
                self.y += self.speed
            if keys[pygame.K_ESCAPE]:
                self.running = False  # Volta pro menu

            # --- Limites da tela (com base na hitbox) ---
            if self.x < 0:
                self.x = 0
            if self.x + self.hitbox_largura > self.largura:
                self.x = self.largura - self.hitbox_largura
            if self.y < 0:
                self.y = 0
            if self.y + self.hitbox_altura > self.altura:
                self.y = self.altura - self.hitbox_altura

            # --- Desenho ---
            self.screen.blit(self.background, (0, 0))
            # Centraliza a imagem em relação à hitbox
            self.screen.blit(
                self.player_image,
                (self.x - (self.imagem_largura - self.hitbox_largura) // 2,
                 self.y - (self.imagem_altura - self.hitbox_altura))
            )

            pygame.display.update()
