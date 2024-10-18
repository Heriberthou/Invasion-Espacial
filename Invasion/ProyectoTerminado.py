import pygame
import random
import time
import math
from pygame import mixer
import sys
import io

# Inicializa pygame
pygame.init()

# Crear pantalla
pantalla = pygame.display.set_mode((1280, 720))

# Titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.png")

# Agregar música
mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)

# Variables del jugador
img_jugador = pygame.image.load("naveespacial.png")
jugador_x = 608
jugador_y = 656
jugador_x_cambio = 0

# Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

def fuente_bytes(fuentes):
    with open(fuentes, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("ovni.png"))
    enemigo_x.append(random.randint(0, 1200))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(9)
    enemigo_y_cambio.append(40)

# Variables de Bala
balas = []
img_bala = pygame.image.load("bala.png")

# Puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("freesansbold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10
# Texto final de juego
fuente_final = pygame.font.Font(fuente_como_bytes,40)
fuente_tiempo = pygame.font.Font('freesansbold.ttf', 32)






def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (500, 340))

def texto_tiempo(tiempos):
    mi_fuente_tiempo = fuente_tiempo.render(f"Record: {tiempos} segundo(s)", True, (255, 255, 255))
    pantalla.blit(mi_fuente_tiempo, (500, 440))


def texto_salida():
    mi_fuente_salida = fuente_final.render("Presiona cualquier tecla para salir", True, (255, 255, 255))
    pantalla.blit(mi_fuente_salida, (400, 600))

def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje : {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Variables del boom
img_boom = pygame.image.load("blast.png")
booms = []

# Función jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Función enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# Función disparar bala
def disparar_bala(x, y):
    pantalla.blit(img_bala, (x + 16, y + 10))

# Función aparecer boom
def aparecer_boom(x, y):
    booms.append({"x": x, "y": y, "t": time.time()})

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y1 - y2, 2))
    return distancia < 32

# Loop del juego
se_ejecuta = True
juego_terminado = False
inicio_final = 0
marcador = time.time()
esperar_salida = False

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            se_ejecuta = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -8
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio = 8
            if event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                nueva_bala = {"x": jugador_x, "y": jugador_y, "velocidad": -5}
                balas.append(nueva_bala)
            if esperar_salida:  # Permitir cerrar el juego si estamos en la pantalla de salida
                se_ejecuta = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    jugador_x += jugador_x_cambio
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 1216:
        jugador_x = 1216

    if not juego_terminado:
        for e in range(cantidad_enemigos):
            if enemigo_y[e] > 600:
                for k in range(cantidad_enemigos):
                    enemigo_y[k] = 1000
                if not juego_terminado:
                    fin = mixer.Sound("gameover.wav")
                    fin.play()
                    inicio_final = time.time()  # Registrar el tiempo cuando se muestra el texto final
                    juego_terminado = True

            enemigo_x[e] += enemigo_x_cambio[e]
            if enemigo_x[e] <= 0:
                enemigo_x_cambio[e] = 30
                enemigo_y[e] += enemigo_y_cambio[e]
            elif enemigo_x[e] >= 1216:
                enemigo_x_cambio[e] = -30
                enemigo_y[e] += enemigo_y_cambio[e]

            for bala in balas[:]:
                if hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"]):
                    aparecer_boom(enemigo_x[e], enemigo_y[e])
                    sonido_colision = mixer.Sound("boom.wav")
                    sonido_colision.play()
                    balas.remove(bala)
                    puntaje += 1
                    enemigo_x[e] = random.randint(0, 736)
                    enemigo_y[e] = random.randint(20, 200)
                    break

            enemigo(enemigo_x[e], enemigo_y[e], e)

        for bala in balas[:]:
            bala["y"] += bala["velocidad"]
            pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
            if bala["y"] < 0:
                bala_perdida = mixer.Sound("perdido.wav")
                bala_perdida.play()
                aparecer_boom(bala["x"], 0)
                balas.remove(bala)

        for boom in booms[:]:
            pantalla.blit(img_boom, (boom["x"], boom["y"]))
            if time.time() - boom["t"] > 0.5:
                booms.remove(boom)

    if juego_terminado:
        texto_final()
        tiempo = inicio_final - marcador
        tiempo = math.ceil(tiempo)
        texto_tiempo(tiempo)
        texto_salida()
        esperar_salida = True

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()

pygame.quit()
sys.exit()
