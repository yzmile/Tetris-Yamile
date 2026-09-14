import pygame
import random

pygame.init()

# =========================
# CONFIGURACIÓN
# =========================

TAMANO_BLOQUE = 30
FILAS = 20
COLUMNAS = 10

ANCHO = COLUMNAS * TAMANO_BLOQUE
ALTO = FILAS * TAMANO_BLOQUE

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tetris")

reloj = pygame.time.Clock()


# =========================
# COLORES
# =========================

NEGRO = (0, 0, 0)
GRIS = (50, 50, 50)
BLANCO = (255, 255, 255)

CIAN = (0, 240, 240)
AMARILLO = (240, 240, 0)
MORADO = (160, 0, 240)
NARANJA = (255, 140, 0)
AZUL = (0, 100, 240)
VERDE = (0, 200, 0)
ROJO = (240, 0, 0)


# =========================
# FUENTES
# =========================

fuente = pygame.font.Font(None, 32)
fuente_titulo = pygame.font.Font(None, 70)
fuente_grande = pygame.font.Font(None, 45)


# =========================
# PIEZAS
# =========================

PIEZAS = [

    # O
    [
        [1, 1],
        [1, 1]
    ],

    # I
    [
        [1, 1, 1, 1]
    ],

    # T
    [
        [0, 1, 0],
        [1, 1, 1]
    ],

    # L
    [
        [1, 0],
        [1, 0],
        [1, 1]
    ],

    # J
    [
        [0, 1],
        [0, 1],
        [1, 1]
    ],

    # S
    [
        [0, 1, 1],
        [1, 1, 0]
    ],

    # Z
    [
        [1, 1, 0],
        [0, 1, 1]
    ]
]


COLORES_PIEZAS = [
    AMARILLO,
    CIAN,
    MORADO,
    NARANJA,
    AZUL,
    VERDE,
    ROJO
]


# =========================
# VARIABLES DEL JUEGO
# =========================

tablero = []

puntuacion = 0
lineas_totales = 0
nivel = 1

velocidad_caida = 500
tiempo_caida = 0

juego_terminado = False


# =========================
# ESTADO DE LA PANTALLA
# =========================

pantalla_actual = "menu"


# =========================
# CREAR TABLERO
# =========================

def crear_tablero():

    nuevo_tablero = []

    for i in range(FILAS):

        fila_tablero = []

        for j in range(COLUMNAS):
            fila_tablero.append(0)

        nuevo_tablero.append(fila_tablero)

    return nuevo_tablero


# =========================
# NUEVA PIEZA
# =========================

def nueva_pieza():

    global indice_pieza
    global pieza_actual
    global color_actual
    global fila
    global columna
    global juego_terminado

    indice_pieza = random.randrange(len(PIEZAS))

    pieza_actual = PIEZAS[indice_pieza]
    color_actual = COLORES_PIEZAS[indice_pieza]

    fila = 0
    columna = 4

    for i in range(len(pieza_actual)):

        for j in range(len(pieza_actual[i])):

            if pieza_actual[i][j] == 1:

                if tablero[fila + i][columna + j] != 0:

                    juego_terminado = True


# =========================
# ROTAR PIEZA
# =========================

def rotar_pieza():

    filas_pieza = len(pieza_actual)
    columnas_pieza = len(pieza_actual[0])

    nueva_pieza = []

    for j in range(columnas_pieza):

        nueva_fila = []

        for i in range(filas_pieza - 1, -1, -1):

            nueva_fila.append(pieza_actual[i][j])

        nueva_pieza.append(nueva_fila)

    return nueva_pieza


# =========================
# COMPROBAR BAJADA
# =========================

def puede_bajar():

    nueva_fila = fila + 1

    for i in range(len(pieza_actual)):

        for j in range(len(pieza_actual[i])):

            if pieza_actual[i][j] == 1:

                fila_tablero = nueva_fila + i
                columna_tablero = columna + j

                if fila_tablero >= FILAS:
                    return False

                if tablero[fila_tablero][columna_tablero] != 0:
                    return False

    return True


# =========================
# COMPROBAR MOVIMIENTO
# =========================

def puede_mover(direccion):

    nueva_columna = columna + direccion

    for i in range(len(pieza_actual)):

        for j in range(len(pieza_actual[i])):

            if pieza_actual[i][j] == 1:

                columna_tablero = nueva_columna + j
                fila_tablero = fila + i

                if columna_tablero < 0:
                    return False

                if columna_tablero >= COLUMNAS:
                    return False

                if tablero[fila_tablero][columna_tablero] != 0:
                    return False

    return True


# =========================
# COMPROBAR ROTACIÓN
# =========================

def puede_rotar(nueva_pieza):

    for i in range(len(nueva_pieza)):

        for j in range(len(nueva_pieza[i])):

            if nueva_pieza[i][j] == 1:

                nueva_fila = fila + i
                nueva_columna = columna + j

                if nueva_fila >= FILAS:
                    return False

                if nueva_columna < 0:
                    return False

                if nueva_columna >= COLUMNAS:
                    return False

                if tablero[nueva_fila][nueva_columna] != 0:
                    return False

    return True


# =========================
# FIJAR PIEZA
# =========================

def fijar_pieza():

    for i in range(len(pieza_actual)):

        for j in range(len(pieza_actual[i])):

            if pieza_actual[i][j] == 1:

                tablero[fila + i][columna + j] = color_actual


# =========================
# ELIMINAR LÍNEAS
# =========================

def eliminar_lineas():

    global puntuacion
    global lineas_totales
    global nivel
    global velocidad_caida

    filas_nuevas = []

    for fila_tablero in tablero:

        if 0 in fila_tablero:

            filas_nuevas.append(fila_tablero)

    lineas_eliminadas = FILAS - len(filas_nuevas)

    if lineas_eliminadas == 1:
        puntuacion += 100

    elif lineas_eliminadas == 2:
        puntuacion += 300

    elif lineas_eliminadas == 3:
        puntuacion += 500

    elif lineas_eliminadas == 4:
        puntuacion += 800

    lineas_totales += lineas_eliminadas

    nivel = (lineas_totales // 10) + 1

    velocidad_caida = max(
        100,
        500 - ((nivel - 1) * 50)
    )

    for i in range(lineas_eliminadas):

        filas_nuevas.insert(
            0,
            [0] * COLUMNAS
        )

    for i in range(FILAS):

        tablero[i] = filas_nuevas[i]


# =========================
# DIBUJAR TABLERO
# =========================

def dibujar_tablero():

    for fila_tablero in range(FILAS):

        for columna_tablero in range(COLUMNAS):

            x = columna_tablero * TAMANO_BLOQUE
            y = fila_tablero * TAMANO_BLOQUE

            pygame.draw.rect(
                pantalla,
                GRIS,
                (
                    x,
                    y,
                    TAMANO_BLOQUE,
                    TAMANO_BLOQUE
                ),
                1
            )

            if tablero[fila_tablero][columna_tablero] != 0:

                pygame.draw.rect(
                    pantalla,
                    tablero[fila_tablero][columna_tablero],
                    (
                        x,
                        y,
                        TAMANO_BLOQUE,
                        TAMANO_BLOQUE
                    )
                )


# =========================
# DIBUJAR PIEZA
# =========================

def dibujar_pieza():

    for i in range(len(pieza_actual)):

        for j in range(len(pieza_actual[i])):

            if pieza_actual[i][j] == 1:

                x = (columna + j) * TAMANO_BLOQUE
                y = (fila + i) * TAMANO_BLOQUE

                pygame.draw.rect(
                    pantalla,
                    color_actual,
                    (
                        x,
                        y,
                        TAMANO_BLOQUE,
                        TAMANO_BLOQUE
                    )
                )


# =========================
# DIBUJAR INFORMACIÓN
# =========================

def dibujar_informacion():

    texto_puntos = fuente.render(
        "Puntos: " + str(puntuacion),
        True,
        BLANCO
    )

    texto_nivel = fuente.render(
        "Nivel: " + str(nivel),
        True,
        BLANCO
    )

    pantalla.blit(texto_puntos, (5, 5))
    pantalla.blit(texto_nivel, (5, 30))


# =========================
# GAME OVER
# =========================

def dibujar_game_over():

    texto = fuente_titulo.render(
        "GAME OVER",
        True,
        ROJO
    )

    texto_reinicio = fuente.render(
        "R = Reiniciar",
        True,
        BLANCO
    )

    texto_menu = fuente.render(
        "ESC = Menú",
        True,
        BLANCO
    )

    x = (ANCHO - texto.get_width()) // 2
    y = ALTO // 2 - 70

    pantalla.blit(texto, (x, y))

    x2 = (ANCHO - texto_reinicio.get_width()) // 2

    pantalla.blit(
        texto_reinicio,
        (x2, y + 70)
    )

    x3 = (ANCHO - texto_menu.get_width()) // 2

    pantalla.blit(
        texto_menu,
        (x3, y + 110)
    )


# =========================
# REINICIAR JUEGO
# =========================

def reiniciar_juego():

    global tablero
    global puntuacion
    global lineas_totales
    global nivel
    global velocidad_caida
    global tiempo_caida
    global juego_terminado

    tablero = crear_tablero()

    puntuacion = 0
    lineas_totales = 0
    nivel = 1

    velocidad_caida = 500
    tiempo_caida = 0

    juego_terminado = False

    nueva_pieza()


# ==================================================
# MENÚ PRINCIPAL
# ==================================================

def dibujar_menu():

    pantalla.fill(NEGRO)

    titulo = fuente_titulo.render(
        "TETRIS",
        True,
        CIAN
    )

    jugar = fuente_grande.render(
        "1 - JUGAR",
        True,
        BLANCO
    )

    instrucciones = fuente_grande.render(
        "2 - INSTRUCCIONES",
        True,
        BLANCO
    )

    salir = fuente_grande.render(
        "3 - SALIR",
        True,
        BLANCO
    )

    x_titulo = (ANCHO - titulo.get_width()) // 2

    pantalla.blit(
        titulo,
        (x_titulo, 100)
    )

    pantalla.blit(
        jugar,
        (75, 250)
    )

    pantalla.blit(
        instrucciones,
        (35, 320)
    )

    pantalla.blit(
        salir,
        (75, 390)
    )


# ==================================================
# INSTRUCCIONES
# ==================================================

def dibujar_instrucciones():

    pantalla.fill(NEGRO)

    titulo = fuente_grande.render(
        "INSTRUCCIONES",
        True,
        CIAN
    )

    texto1 = fuente.render(
        "Flechas izquierda/derecha: mover",
        True,
        BLANCO
    )

    texto2 = fuente.render(
        "Flecha arriba: rotar",
        True,
        BLANCO
    )

    texto3 = fuente.render(
        "Flecha abajo: bajar",
        True,
        BLANCO
    )

    texto4 = fuente.render(
        "R: reiniciar",
        True,
        BLANCO
    )

    texto5 = fuente.render(
        "ESC: volver al menu",
        True,
        BLANCO
    )

    x = (ANCHO - titulo.get_width()) // 2

    pantalla.blit(
        titulo,
        (x, 80)
    )

    pantalla.blit(
        texto1,
        (25, 200)
    )

    pantalla.blit(
        texto2,
        (25, 250)
    )

    pantalla.blit(
        texto3,
        (25, 300)
    )

    pantalla.blit(
        texto4,
        (25, 350)
    )

    pantalla.blit(
        texto5,
        (25, 400)
    )


# =========================
# INICIAR
# =========================

tablero = crear_tablero()

nueva_pieza()


# =========================
# BUCLE PRINCIPAL
# =========================

ejecutando = True


while ejecutando:

    tiempo = reloj.tick(60)

    tiempo_caida += tiempo


    # =========================
    # EVENTOS
    # =========================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            ejecutando = False


        if evento.type == pygame.KEYDOWN:

            # =========================
            # MENÚ
            # =========================

            if pantalla_actual == "menu":

                if evento.key == pygame.K_1:

                    reiniciar_juego()

                    pantalla_actual = "juego"


                elif evento.key == pygame.K_2:

                    pantalla_actual = "instrucciones"


                elif evento.key == pygame.K_3:

                    ejecutando = False


            # =========================
            # INSTRUCCIONES
            # =========================

            elif pantalla_actual == "instrucciones":

                if evento.key == pygame.K_ESCAPE:

                    pantalla_actual = "menu"


            # =========================
            # JUEGO
            # =========================

            elif pantalla_actual == "juego":

                if evento.key == pygame.K_ESCAPE:

                    pantalla_actual = "menu"


                if juego_terminado:

                    if evento.key == pygame.K_r:

                        reiniciar_juego()

                else:

                    # Izquierda
                    if evento.key == pygame.K_LEFT:

                        if puede_mover(-1):
                            columna -= 1


                    # Derecha
                    if evento.key == pygame.K_RIGHT:

                        if puede_mover(1):
                            columna += 1


                    # Bajar
                    if evento.key == pygame.K_DOWN:

                        if puede_bajar():
                            fila += 1


                    # Rotar
                    if evento.key == pygame.K_UP:

                        nueva_pieza_rotada = rotar_pieza()

                        if puede_rotar(nueva_pieza_rotada):

                            pieza_actual = nueva_pieza_rotada


    # =========================
    # ACTUALIZAR JUEGO
    # =========================

    if pantalla_actual == "juego":

        if not juego_terminado:

            if tiempo_caida >= velocidad_caida:

                if puede_bajar():

                    fila += 1

                else:

                    fijar_pieza()

                    eliminar_lineas()

                    nueva_pieza()

                tiempo_caida = 0


    # =========================
    # DIBUJAR
    # =========================

    if pantalla_actual == "menu":

        dibujar_menu()


    elif pantalla_actual == "instrucciones":

        dibujar_instrucciones()


    elif pantalla_actual == "juego":

        pantalla.fill(NEGRO)

        dibujar_tablero()

        if not juego_terminado:

            dibujar_pieza()

        dibujar_informacion()

        if juego_terminado:

            dibujar_game_over()


    pygame.display.flip()


pygame.quit()