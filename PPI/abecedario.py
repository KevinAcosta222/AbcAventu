import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1300, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Abecedario")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

# Fuente
font = pygame.font.Font(None, 50)

# Fondo (puedes usar el mismo fondo del menú si quieres)
fondo = pygame.image.load("FONDO.png")
fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

# Botón de volver
btn_volver = pygame.Rect(WIDTH - 220, HEIGHT - 80, 200, 60)

# Bucle principal
running = True
while running:
    screen.blit(fondo, (0, 0))

    # Dibujar botón
    pygame.draw.rect(screen, BLUE, btn_volver, border_radius=10)
    text_volver = font.render("Volver al menú", True, WHITE)
    screen.blit(text_volver, text_volver.get_rect(center=btn_volver.center))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if btn_volver.collidepoint(event.pos):
                running = False  # Cierra esta ventana

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
