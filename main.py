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


def iniciar_juego():
    print("\nIniciando juego...")
    print("El tablero se agregará próximamente.")


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