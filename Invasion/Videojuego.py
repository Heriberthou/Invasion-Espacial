import pygame
import random
import time  # Importar la biblioteca de tiempo
import math
from pygame import mixer
#Inicializa pygame
pygame.init()

#Crear pantalla
pantalla = pygame.display.set_mode((1280, 720))


#Titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo.png")

# agregar musica

mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)
#mixer.music.set_volume(0.5)

#variables del jugador
img_jugador = pygame.image.load("rocket.png")
jugador_x = 608
jugador_y = 556
jugador_x_cambio = 0
#jugador_y_cambio = 0

#variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("nave.png"))
    enemigo_x.append(random.randint(0, 1200))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(9)
    enemigo_y_cambio.append(40)


# Variables Bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 8
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf',32)
texto_x = 10
texto_y = 10

# texto final de juego
fuente_final = pygame.font.Font('freesansbold.ttf',32)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True,(255,255,255) )
    pantalla.blit(mi_fuente_final, (500, 340))

def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje : {puntaje}",True,(255,255,255))
    pantalla.blit(texto,(x,y))

# Variables del boom
img_boom = pygame.image.load("blast.png")
booms = []
boom_x = 0
boom_start_time = 0


# Funcion jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))
#Función enemigo
def enemigo(x,y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))
# Funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))
def aparecer_boom(x, y):
    global boom_visible, boom_start_time
    boom_visible = True
    boom_start_time = time.time()  # Registrar el tiempo actual
    pantalla.blit(img_boom, (x + 16, y + 10))

def hay_colision(x1,y1,x2,y2):
    distancia = math.sqrt(math.pow(x2 - x1,2) + math.pow(y1- y2,2))
    if distancia < 32:
        return True
    else:
        return False


#loop del juego (Ciclo del juego que permite que no se cierre)
se_ejecuta = True
while se_ejecuta:
    # poll for events

    pantalla.blit(fondo,(0,0))
    # pygame.QUIT event means the user clicked X to close your window
    #pantalla.fill((205, 144, 228))
    # Iterar eventos
    for event in pygame.event.get():

        # Evento cerrar
        if event.type == pygame.QUIT:
            se_ejecuta = False
        # Evento presionar flechas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador_x_cambio = -8
            if event.key == pygame.K_RIGHT:
                jugador_x_cambio = 8
            if event.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                boom_x = bala_x
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                nuevo_boom = {
                    "x": jugador_x,
                    "y": 0,
                    "t":  boom_start_time
                }
                booms.append(nuevo_boom)
                balas.append(nueva_bala)
            #if event.key == pygame.K_UP:
            #   jugador_y_cambio = -0.5
            #if event.key == pygame.K_DOWN:
            #   jugador_y_cambio = 0.5"""

        # Evento soltar flechas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
           #if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                #jugador_y_cambio = 0
    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio
    #jugador_y += jugador_y_cambio

    # Mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 1216:
        jugador_x = 1216
    #if jugador_y <= 0:
    #    jugador_y = 0
    #elif jugador_y >= 656:
    #    jugador_y = 656"""

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 6.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 1216:
            enemigo_x_cambio[e] = -6
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        for bala in balas:
            cont = 0
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                tiempo = time.time()
                booms[cont]["t"] = tiempo
                booms[cont]["y"] = bala["y"]
                pantalla.blit(img_boom, (booms[cont]["x"] + 16, enemigo_y[e]  + 10))
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break
            cont += 1

        enemigo(enemigo_x[e], enemigo_y[e], e)

#        # colision
#       colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
#        if colision:
 #           sonido_colision = mixer.Sound("Golpe.mp3")
  #          sonido_colision.play()
   #         bala_y = 500
    #        bala_visible = False
     #       boom_y = enemigo_y[e]
      #      aparecer_boom(boom_x,boom_y)
       #     puntaje += 1
        #    enemigo_x[e] = random.randint(0, 1200)
         #   enemigo_y[e] = random.randint(50, 200)
        #enemigo(enemigo_x[e], enemigo_y[e], e)


    #if bala_visible:
   #     disparar_bala(bala_x, bala_y)
  #      bala_y -= bala_y_cambio
 #   if bala_y <= 0:
#        bala_visible = False
  #      boom_y = 0
 #       aparecer_boom(bala_x, 0)
#        bala_y = 500

# Movimiento bala
    for bala in balas:
        cont = 0
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            booms[cont]["y"] = 0
            pantalla.blit(img_boom, (booms[cont]["x"] + 16, 0 + 10))
            balas.remove(bala)
        cont += 1
    for boom in booms:
        pantalla.blit(img_bala, (boom["x"] + 16, boom["y"] + 10))
        if time.time() - boom["t"] > 0.5:
           booms.remove(boom)




        # Verificar si la imagen boom debe desaparecer

#    if boom_visible:
#        # Mostrar imagen boom
#        pantalla.blit(img_boom, (boom_x + 16, boom_y + 10))
#        # Comprobar si han pasado 1 segundo
#        if time.time() - boom_start_time > 0.5 or bala_visible == True:
#            boom_visible = False




    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x,texto_y)

    # Actualizar
    pygame.display.update()





