def mostrar_menu():
    print("=== TETRIS ===")
    print("1. Jugar")
    print("2. Instrucciones")
    print("3. Salir")


def main():
    while True:
        mostrar_menu()

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Iniciando juego...")

        elif opcion == "2":
            print("Las instrucciones aparecerán aquí.")

        elif opcion == "3":
            print("Saliendo del juego...")
            break

        else:
            print("Opción no válida.")


main()