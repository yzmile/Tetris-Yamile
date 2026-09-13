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


# NUEVA FUNCIÓN
def mostrar_tablero(tablero):
    print("ESTOY EN MOSTRAR_TABLERO")

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

    tablero = crear_tablero()

    tablero[5][4] = 1

    mostrar_tablero(tablero)

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
