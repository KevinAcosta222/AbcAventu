import pygame
import os
import subprocess

# Inicializar Pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Configuración de pantalla
WIDTH_INICIO, HEIGHT_INICIO = 1000, 700
WIDTH_MENU, HEIGHT_MENU = 1300, 700
screen = pygame.display.set_mode((WIDTH_INICIO, HEIGHT_INICIO))
pygame.display.set_caption("Menú de Juego")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 180, 160)
TEXT_COLOR = (255,255,0)

# Fuentes
font = pygame.font.Font(None, 50)
font_button = pygame.font.Font(None, 30)
fuente_jugar = pygame.font.Font("PanasChill.ttf", 60)

# Logo
logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (400, 300))

# Fondo
fondo_inicio = pygame.image.load("FONDO.png")
fondo_inicio = pygame.transform.scale(fondo_inicio, (WIDTH_INICIO, HEIGHT_INICIO))

fondo_menu = pygame.image.load("FONDO.png")
fondo_menu = pygame.transform.scale(fondo_menu, (WIDTH_MENU, HEIGHT_MENU))

# Texto intermitente para botón jugar
class Texto:
    texto = "JUGAR"
    size = 60
    color = TEXT_COLOR
    font = fuente_jugar
    coord = (WIDTH_INICIO // 2, 380)
    parpadeando = True
    parpadear = pygame.USEREVENT + 1
    pygame.time.set_timer(parpadear, 800)

texto_jugar = Texto()

# Funciones para mostrar texto

def mostrarTextoTTF(texto):
    fuente = texto.font
    superficie = fuente.render(texto.texto, True, texto.color)
    rect = superficie.get_rect(center=texto.coord)
    screen.blit(superficie, rect)

def intermitenteTextoTTF(texto):
    for evento in pygame.event.get([texto.parpadear]):
        if evento.type == texto.parpadear:
            texto.parpadeando = not texto.parpadeando
    if texto.parpadeando:
        mostrarTextoTTF(texto)

# Botón de salir
btn_salir = pygame.Rect(WIDTH_INICIO // 2 - 75, 450, 150, 60)

# Cargar imágenes botones menú
button_images = {
    "Abecedario": pygame.image.load("abecedario.png"),
    "Colores": pygame.image.load("colores.png"),
    "Números": pygame.image.load("numeros.png"),
    "Vocabulario": pygame.image.load("vocabulario.png"),
    "Cuentos": pygame.image.load("cuentos.png")
}

# Redimensionar imágenes
button_size = (200, 200)
for key in button_images:
    button_images[key] = pygame.transform.scale(button_images[key], button_size)

# Posiciones botones menú tipo pirámide
buttons = [
    {"name": "Abecedario", "pos": (250, 100), "script": "abecedario.py"},
    {"name": "Colores", "pos": (550, 100), "script": "colores.py"},
    {"name": "Números", "pos": (850, 100), "script": "numeros.py"},
    {"name": "Vocabulario", "pos": (400, 350), "script": "vocabulario.py"},
    {"name": "Cuentos", "pos": (700, 350), "script": "cuentos.py"}
]

# Estados del menú
MENU_INICIO = 0
MENU_CATEGORIAS = 1
estado = MENU_INICIO

# Función para dibujar botones menú
def draw_buttons():
    screen.blit(fondo_menu, (0, 0))
    for button in buttons:
        img = button_images[button["name"]]
        x, y = button["pos"]
        screen.blit(img, (x, y))

        text_surface = font_button.render(button["name"], True, WHITE)
        text_rect = text_surface.get_rect(center=(x + 92, y + 210 + 9))
        pygame.draw.rect(screen, GREEN, (x + 15, y + 200, 160, 35), border_radius=15)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

# Bucle principal
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    if estado == MENU_INICIO:
        screen.blit(fondo_inicio, (0, 0))
        screen.blit(logo, (WIDTH_INICIO // 2 - 200, 50))
        intermitenteTextoTTF(texto_jugar)

        pygame.draw.rect(screen, BLUE, btn_salir, border_radius=10)
        text_salir = font.render("Salir", True, WHITE)
        screen.blit(text_salir, text_salir.get_rect(center=btn_salir.center))

    elif estado == MENU_CATEGORIAS:
        draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if estado == MENU_INICIO:
                if btn_salir.collidepoint(event.pos):
                    running = False
                elif pygame.Rect(WIDTH_INICIO // 2 - 100, 350, 200, 60).collidepoint(event.pos):
                    estado = MENU_CATEGORIAS
                    screen = pygame.display.set_mode((WIDTH_MENU, HEIGHT_MENU))
            elif estado == MENU_CATEGORIAS:
                for button in buttons:
                    x, y = button["pos"]
                    rect_img = pygame.Rect(x, y, 200, 200)
                    rect_text = pygame.Rect(x + 15, y + 200, 160, 35)
                    if rect_img.collidepoint(event.pos) or rect_text.collidepoint(event.pos):
                        subprocess.run(["python", button["script"]])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
