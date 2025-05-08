import pygame
import sys
import random

pygame.init()

# Tamaño de la pantalla
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("¡Qué Desorden! Abecedario en Inglés")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 102, 255)

# Fuente
font = pygame.font.SysFont(None, 40)

# Cargar imágenes
fondo_menu = pygame.transform.scale(pygame.image.load("QD.png"), (WIDTH, HEIGHT))
fondo_juego = pygame.transform.scale(pygame.image.load("QDA.png"), (WIDTH, HEIGHT))
estrella_img = pygame.transform.scale(pygame.image.load("estrella.png"), (64, 64))

# Botones
btn_jugar = pygame.Rect(400, 570, 200, 60)
btn_volver = pygame.Rect(790, 620, 180, 50)
btn_reiniciar = pygame.Rect(400, 400, 200, 60)

# Estado del juego
estado = "MENU"

# Letras
abecedario = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
letras_base = random.sample(abecedario, len(abecedario))
letras_drag = []
letras_target = []
letras_animando = []
letra_seleccionada = None
offset_x, offset_y = 0, 0
incorrect_flash = None
flash_timer = 0

# Crear áreas de letras arrastrables
def crear_letras():
    letras_drag.clear()
    for i, letra in enumerate(letras_base):
        x = 50 + (i % 13) * 70
        y = 580 + (i // 13) * 70
        letras_drag.append({
            "letra": letra,
            "rect": pygame.Rect(x, y, 50, 50),
            "colocada": False,
            "base_pos": (x, y)
        })

# Crear áreas de estrellas destino
def crear_estrellas():
    letras_target.clear()
    posiciones = [
    (395, 40), (515, 40), (638, 40), (760, 40), (879, 40),
    (395, 120), (515, 120), (638, 120), (760, 120), (879, 120),
    (395, 200), (515, 200), (638, 200), (760, 200), (879, 200),
    (395, 280), (515, 280), (638, 280), (760, 280), (879, 280),
    (395, 360), (515, 360), (638, 360), (760, 360), (879, 360),
    (638, 432)
    ]
    for i, letra in enumerate(abecedario):
        x, y = posiciones[i]
        letras_target.append({
            "letra": letra,
            "rect": pygame.Rect(x, y, 60, 60),
            "ocupado": False
        })

crear_letras()
crear_estrellas()

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if estado == "MENU":
                if btn_jugar.collidepoint(mx, my):
                    estado = "JUEGO"

            elif estado == "JUEGO":
                if btn_volver.collidepoint(mx, my):
                    estado = "MENU"
                for letter in letras_drag:
                    if (letter["rect"].collidepoint(mx, my)
                            and not letter["colocada"]):
                        letra_seleccionada = letter
                        offset_x = mx - letter["rect"].x
                        offset_y = my - letter["rect"].y
                        break

            elif estado == "FIN":
                if btn_reiniciar.collidepoint(mx, my):
                    letras_base = random.sample(abecedario, len(abecedario))
                    crear_letras()
                    crear_estrellas()
                    estado = "JUEGO"

        elif event.type == pygame.MOUSEMOTION:
            if letra_seleccionada:
                letra_seleccionada["rect"].x = event.pos[0] - offset_x
                letra_seleccionada["rect"].y = event.pos[1] - offset_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if letra_seleccionada and estado == "JUEGO":
                dropped = False
                for target in letras_target:
                    if (target["rect"].collidepoint(letra_seleccionada["rect"].center)
                            and not target["ocupado"]):
                        if letra_seleccionada["letra"] == target["letra"]:
                            letras_animando.append({
                                "obj": letra_seleccionada,
                                "inicio": letra_seleccionada["rect"].center,
                                "destino": target["rect"].center,
                                "tiempo": 0,
                                "duracion": 300,
                                "target": target
                            })
                        
                        else:
                            incorrect_flash = target
                            flash_timer = 300
                            letra_seleccionada["rect"].topleft = letra_seleccionada["base_pos"]
                        dropped = True
                        break
                if not dropped:
                    letra_seleccionada["rect"].topleft = letra_seleccionada["base_pos"]
                letra_seleccionada = None
            

    if estado == "MENU":
        screen.blit(fondo_menu, (0, 0))
        pygame.draw.rect(screen, BLUE, btn_jugar, border_radius=15)
        screen.blit(font.render("JUGAR", True, WHITE),
                    font.render("JUGAR", True, WHITE).get_rect(center=btn_jugar.center))

    elif estado == "JUEGO":
        screen.blit(fondo_juego, (0, 0))
        pygame.draw.rect(screen, BLUE, btn_volver, border_radius=15)
        screen.blit(font.render("VOLVER", True, WHITE),
                    font.render("VOLVER", True, WHITE).get_rect(center=btn_volver.center))

        for t in letras_target:
            screen.blit(estrella_img, t["rect"].topleft)
            if t["ocupado"]:
                text = font.render(t["letra"], True, GREEN)
                screen.blit(text, text.get_rect(center=t["rect"].center))

        if incorrect_flash and flash_timer > 0:
            pygame.draw.rect(screen, RED, incorrect_flash["rect"], 5, border_radius=8)
            flash_timer -= dt
        else:
            incorrect_flash = None

        for letter in letras_drag:
            if not letter["colocada"]:
                pygame.draw.rect(screen, BLUE, letter["rect"], border_radius=8)
                txt = font.render(letter["letra"], True, WHITE)
                screen.blit(txt, txt.get_rect(center=letter["rect"].center))

        nuevas_animaciones = []
        for anim in letras_animando:
            anim["tiempo"] += dt
            progreso = min(anim["tiempo"] / anim["duracion"], 1)
            x = anim["inicio"][0] + (anim["destino"][0] - anim["inicio"][0]) * progreso
            y = anim["inicio"][1] + (anim["destino"][1] - anim["inicio"][1]) * progreso
            anim["obj"]["rect"].center = (x, y)

            if progreso < 1:
                nuevas_animaciones.append(anim)
            else:
                anim["obj"]["colocada"] = True
                anim["target"]["ocupado"] = True
                anim["obj"]["rect"].center = anim["destino"]
        letras_animando = nuevas_animaciones

        if all(t["ocupado"] for t in letras_target):
            estado = "FIN"

    elif estado == "FIN":
        screen.fill(WHITE)
        msg = font.render("¡FELICITACIONES!", True, GREEN)
        screen.blit(msg, msg.get_rect(center=(WIDTH//2, 200)))
        pygame.draw.rect(screen, GREEN, btn_reiniciar, border_radius=15)
        screen.blit(font.render("REINICIAR", True, WHITE),
                    font.render("REINICIAR", True, WHITE).get_rect(center=btn_reiniciar.center))

    pygame.display.flip()

pygame.quit()
sys.exit()
