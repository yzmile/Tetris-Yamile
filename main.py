import time


def mostrar_menu():
    print("=== TETRIS ===")
    print("1. Jugar")
    print("2. Instrucciones")
    print("3. Salir")


def mostrar_instrucciones():
    print("\n=== INSTRUCCIONES ===")
    print("El objetivo es completar líneas con las piezas.")
    print("Las piezas caen desde la parte superior.")
    print("Completá una línea para eliminarla.")
    print("No dejes que las piezas lleguen hasta arriba.")


# NUEVA FUNCIÓN
def crear_tablero():
    filas = 20
    columnas = 10

    tablero = []

    for i in range(filas):
        fila = []

        for j in range(columnas):
            fila.append(0)

        tablero.append(fila)

    return tablero
pieza_o = [
    [1, 1],
    [1, 1]
]
def limpiar_tablero(tablero):
    for i in range(20):
        for j in range(10):
            tablero[i][j] = 0

def colocar_pieza_o(tablero, fila, columna):
    for i in range(2):
        for j in range(2):
            if pieza_o[i][j] == 1:
                tablero[fila + i][columna + j] = "[]"
def puede_bajar(tablero, fila, columna):
    if fila + 2 >= 20:
        return False

    if tablero[fila + 2][columna] != 0:
        return False

    if tablero[fila + 2][columna + 1] != 0:
        return False

    return True

def puede_mover(tablero, fila, columna, direccion):
    nueva_columna = columna + direccion

    if nueva_columna < 0:
        return False

    if nueva_columna + 1 >= 10:
        return False

    if tablero[fila][nueva_columna] != 0:
        return False

    if tablero[fila + 1][nueva_columna] != 0:
        return False

    return True


# NUEVA FUNCIÓN
def mostrar_tablero(tablero):

    print()

    for fila in tablero:
        print("|", end="")

        for espacio in fila:
            if espacio == 0:
                print(" .", end="")
            else:
                print(" []", end="")

        print(" |")

    print()

def iniciar_juego():
    print("\n=== JUEGO ===")

    tablero_fijo = crear_tablero()

    for pieza in range(2):

        fila = 1
        columna = 4

        while puede_bajar(tablero_fijo, fila, columna):
            tablero = crear_tablero()

            for i in range(20):
                for j in range(10):
                    tablero[i][j] = tablero_fijo[i][j]

            colocar_pieza_o(tablero, fila, columna)
            mostrar_tablero(tablero)

            time.sleep(0.5)

            if puede_mover(tablero_fijo, fila, columna, 1):
                columna = columna + 1

            fila = fila + 1

        colocar_pieza_o(tablero_fijo, fila, columna)

        print("La pieza quedó fija.")
    
def main():
    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            iniciar_juego()

        elif opcion == "2":
            mostrar_instrucciones()

        elif opcion == "3":
            print("Saliendo del juego...")
            break

        else:
            print("Opción no válida.")

        print()


main()
