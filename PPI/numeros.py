import pygame 
import sys

# Inicializar Pygame
pygame.init()

# Tamaño pantalla
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Numeros")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 200, 100)

# Cargar imágenes de fondo
fondo_inicio = pygame.image.load("ConectaLosPuntos.png")  # Imagen con letrero
fondo_inicio = pygame.transform.scale(fondo_inicio, (WIDTH, HEIGHT))

fondo_juego = pygame.image.load("CLP.png")  # Imagen del juego
fondo_juego = pygame.transform.scale(fondo_juego, (WIDTH, HEIGHT))

# Fuente
font = pygame.font.SysFont(None, 40)

# Puntos del 1 al 10
points = [
    (150, 200), (250, 150), (350, 180), (450, 160), (550, 200),
    (600, 300), (500, 400), (400, 420), (300, 350), (200, 300)
]

# Variables
current_index = 0
selected_points = []
radius = 18
clock = pygame.time.Clock()
estado = "MENU"

# Botones
btn_jugar = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 150, 200, 60)
btn_volver = pygame.Rect(WIDTH - 200, HEIGHT - 70, 180, 50)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if estado == "MENU":
                if btn_jugar.collidepoint(mouse_pos):
                    estado = "JUEGO"
                    current_index = 0
                    selected_points = []

            elif estado == "JUEGO":
                # Clic en punto
                if current_index < len(points):
                    px, py = points[current_index]
                    distance = ((mouse_pos[0] - px) ** 2 + (mouse_pos[1] - py) ** 2) ** 0.5
                    if distance < radius:
                        selected_points.append((px, py))
                        current_index += 1

                # Clic en volver al menú
                if btn_volver.collidepoint(mouse_pos):
                    estado = "MENU"

    # --- DIBUJAR ---
    if estado == "MENU":
        screen.blit(fondo_inicio, (0, 0))
        pygame.draw.rect(screen, BLUE, btn_jugar, border_radius=15)
        jugar_text = font.render("Jugar", True, WHITE)
        screen.blit(jugar_text, jugar_text.get_rect(center=btn_jugar.center))

    elif estado == "JUEGO":
        screen.blit(fondo_juego, (0, 0))

        # Dibujar líneas conectadas
        if len(selected_points) > 1:
            pygame.draw.lines(screen, GREEN, False, selected_points, 4)

        # Dibujar los 10 puntos
        for i, (x, y) in enumerate(points):
            color = BLUE if i == current_index else BLACK
            pygame.draw.circle(screen, color, (x, y), radius)
            label = font.render(str(i + 1), True, WHITE)
            screen.blit(label, label.get_rect(center=(x, y)))

        # Botón volver al menú
        pygame.draw.rect(screen, BLUE, btn_volver, border_radius=15)
        volver_text = font.render("Volver al menú", True, WHITE)
        screen.blit(volver_text, volver_text.get_rect(center=btn_volver.center))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
