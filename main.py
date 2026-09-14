import pygame
import random

pygame.init()

# =========================
# CONFIGURACIÓN
# =========================

TAMANO_BLOQUE = 30
FILAS = 20
COLUMNAS = 10

ANCHO_TABLERO = COLUMNAS * TAMANO_BLOQUE
ANCHO_PANEL = 200

ANCHO = ANCHO_TABLERO + ANCHO_PANEL
ALTO = FILAS * TAMANO_BLOQUE

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tetris")

reloj = pygame.time.Clock()


# =========================
# COLORES
# =========================

NEGRO = (0, 0, 0)
GRIS = (50, 50, 50)
GRIS_OSCURO = (25, 25, 25)
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

fuente = pygame.font.Font(None, 28)
fuente_grande = pygame.font.Font(None, 40)
fuente_titulo = pygame.font.Font(None, 70)


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
# ESTADO DE PANTALLA
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
# PRÓXIMA PIEZA
# =========================

def crear_proxima_pieza():

    global indice_proxima
    global pieza_proxima
    global color_proxima

    indice_proxima = random.randrange(len(PIEZAS))

    pieza_proxima = PIEZAS[indice_proxima]
    color_proxima = COLORES_PIEZAS[indice_proxima]


# =========================
# ROTAR
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
# DIBUJAR BLOQUE
# =========================

def dibujar_bloque(x, y, color):

    pygame.draw.rect(
        pantalla,
        color,
        (
            x,
            y,
            TAMANO_BLOQUE,
            TAMANO_BLOQUE
        )
    )

    # Borde
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (
            x,
            y,
            TAMANO_BLOQUE,
            TAMANO_BLOQUE
        ),
        1
    )


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

                dibujar_bloque(
                    x,
                    y,
                    tablero[fila_tablero][columna_tablero]
                )


# =========================
# DIBUJAR PIEZA ACTUAL
# =========================

def dibujar_pieza():

    for i in range(len(pieza_actual)):

        for j in range(len(pieza_actual[i])):

            if pieza_actual[i][j] == 1:

                x = (columna + j) * TAMANO_BLOQUE
                y = (fila + i) * TAMANO_BLOQUE

                dibujar_bloque(
                    x,
                    y,
                    color_actual
                )


# =========================
# DIBUJAR PRÓXIMA PIEZA
# =========================

def dibujar_proxima_pieza():

    titulo = fuente_grande.render(
        "SIGUIENTE",
        True,
        BLANCO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO_TABLERO + 25,
            40
        )
    )

    # Área de la próxima pieza

    pygame.draw.rect(
        pantalla,
        GRIS_OSCURO,
        (
            ANCHO_TABLERO + 20,
            90,
            160,
            130
        )
    )

    pygame.draw.rect(
        pantalla,
        GRIS,
        (
            ANCHO_TABLERO + 20,
            90,
            160,
            130
        ),
        2
    )

    ancho = len(pieza_proxima[0]) * TAMANO_BLOQUE
    alto = len(pieza_proxima) * TAMANO_BLOQUE

    inicio_x = ANCHO_TABLERO + 20 + (160 - ancho) // 2
    inicio_y = 90 + (130 - alto) // 2

    for i in range(len(pieza_proxima)):

        for j in range(len(pieza_proxima[i])):

            if pieza_proxima[i][j] == 1:

                x = inicio_x + j * TAMANO_BLOQUE
                y = inicio_y + i * TAMANO_BLOQUE

                dibujar_bloque(
                    x,
                    y,
                    color_proxima
                )


# =========================
# PANEL LATERAL
# =========================

def dibujar_panel():

    pygame.draw.rect(
        pantalla,
        GRIS_OSCURO,
        (
            ANCHO_TABLERO,
            0,
            ANCHO_PANEL,
            ALTO
        )
    )

    pygame.draw.line(
        pantalla,
        GRIS,
        (
            ANCHO_TABLERO,
            0
        ),
        (
            ANCHO_TABLERO,
            ALTO
        ),
        2
    )

    dibujar_proxima_pieza()

    texto_puntos = fuente.render(
        "Puntos",
        True,
        BLANCO
    )

    numero_puntos = fuente_grande.render(
        str(puntuacion),
        True,
        CIAN
    )

    texto_nivel = fuente.render(
        "Nivel",
        True,
        BLANCO
    )

    numero_nivel = fuente_grande.render(
        str(nivel),
        True,
        AMARILLO
    )

    texto_lineas = fuente.render(
        "Líneas",
        True,
        BLANCO
    )

    numero_lineas = fuente_grande.render(
        str(lineas_totales),
        True,
        VERDE
    )

    pantalla.blit(
        texto_puntos,
        (
            ANCHO_TABLERO + 25,
            270
        )
    )

    pantalla.blit(
        numero_puntos,
        (
            ANCHO_TABLERO + 25,
            300
        )
    )

    pantalla.blit(
        texto_nivel,
        (
            ANCHO_TABLERO + 25,
            360
        )
    )

    pantalla.blit(
        numero_nivel,
        (
            ANCHO_TABLERO + 25,
            390
        )
    )

    pantalla.blit(
        texto_lineas,
        (
            ANCHO_TABLERO + 25,
            450
        )
    )

    pantalla.blit(
        numero_lineas,
        (
            ANCHO_TABLERO + 25,
            480
        )
    )


# =========================
# GAME OVER
# =========================

def dibujar_game_over():

    # Oscurecer tablero

    superficie = pygame.Surface(
        (ANCHO_TABLERO, ALTO)
    )

    superficie.set_alpha(180)

    superficie.fill(NEGRO)

    pantalla.blit(
        superficie,
        (0, 0)
    )

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

    x = (
        ANCHO_TABLERO -
        texto.get_width()
    ) // 2

    y = ALTO // 2 - 70

    pantalla.blit(
        texto,
        (x, y)
    )

    x2 = (
        ANCHO_TABLERO -
        texto_reinicio.get_width()
    ) // 2

    pantalla.blit(
        texto_reinicio,
        (x2, y + 70)
    )

    x3 = (
        ANCHO_TABLERO -
        texto_menu.get_width()
    ) // 2

    pantalla.blit(
        texto_menu,
        (x3, y + 110)
    )


# =========================
# REINICIAR
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

    crear_proxima_pieza()


# ==================================================
# MENÚ
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

    x_titulo = (
        ANCHO -
        titulo.get_width()
    ) // 2

    pantalla.blit(
        titulo,
        (x_titulo, 100)
    )

    pantalla.blit(
        jugar,
        (145, 250)
    )

    pantalla.blit(
        instrucciones,
        (105, 320)
    )

    pantalla.blit(
        salir,
        (145, 390)
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
        "Izquierda / Derecha: mover",
        True,
        BLANCO
    )

    texto2 = fuente.render(
        "Arriba: rotar",
        True,
        BLANCO
    )

    texto3 = fuente.render(
        "Abajo: bajar",
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

    x = (
        ANCHO -
        titulo.get_width()
    ) // 2

    pantalla.blit(
        titulo,
        (x, 80)
    )

    pantalla.blit(
        texto1,
        (110, 200)
    )

    pantalla.blit(
        texto2,
        (110, 250)
    )

    pantalla.blit(
        texto3,
        (110, 300)
    )

    pantalla.blit(
        texto4,
        (110, 350)
    )

    pantalla.blit(
        texto5,
        (110, 400)
    )


# =========================
# INICIAR
# =========================

tablero = crear_tablero()

nueva_pieza()

crear_proxima_pieza()


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

                    if evento.key == pygame.K_LEFT:

                        if puede_mover(-1):
                            columna -= 1


                    if evento.key == pygame.K_RIGHT:

                        if puede_mover(1):
                            columna += 1


                    if evento.key == pygame.K_DOWN:

                        if puede_bajar():
                            fila += 1


                    if evento.key == pygame.K_UP:

                        nueva_pieza_rotada = rotar_pieza()

                        if puede_rotar(nueva_pieza_rotada):

                            pieza_actual = nueva_pieza_rotada


    # =========================
    # CAÍDA
    # =========================

    if pantalla_actual == "juego":

        if not juego_terminado:

            if tiempo_caida >= velocidad_caida:

                if puede_bajar():

                    fila += 1

                else:

                    fijar_pieza()

                    eliminar_lineas()

                    # La pieza siguiente pasa a ser la actual

                    pieza_actual = pieza_proxima
                    color_actual = color_proxima

                    global_dummy = 0

                    global_dummy += 1

                    global_dummy = 0

                    # Elegir una nueva próxima pieza

                    indice_proxima = random.randrange(
                        len(PIEZAS)
                    )

                    pieza_proxima = PIEZAS[indice_proxima]

                    color_proxima = COLORES_PIEZAS[
                        indice_proxima
                    ]

                    fila = 0
                    columna = 4

                    # Comprobar Game Over

                    for i in range(len(pieza_actual)):

                        for j in range(len(pieza_actual[i])):

                            if pieza_actual[i][j] == 1:

                                if tablero[
                                    fila + i
                                ][
                                    columna + j
                                ] != 0:

                                    juego_terminado = True

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

        dibujar_panel()

        if juego_terminado:

            dibujar_game_over()


    pygame.display.flip()


pygame.quit()