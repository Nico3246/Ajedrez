# menus.py

from jugar import jugarAjedrezHumanoVsHumano, jugarAjedrezHumanoVsIA

def menu_principal():
    print("\n")
    print("┌" + "─"*32 + "┐")
    print("│{:^32}│".format("Ajedrez IA"))
    print("├" + "─"*32 + "┤")
    print("│ 1. Humano vs Humano           │")
    print("│ 2. Humano vs Alfa-Beta IA     │")
    print("│ 3. Salir                      │")
    print("└" + "─"*32 + "┘")
    try:
        return int(input("Selecciona una opción: "))
    except ValueError:
        return 0

def main():
    while True:
        opc = menu_principal()
        if opc == 1:
            jugarAjedrezHumanoVsHumano()
        elif opc == 2:
            jugarAjedrezHumanoVsIA()
        elif opc == 3:
            print("¡Adiós!")
            break
        else:
            print("Opción inválida, inténtalo de nuevo.")

if __name__ == "__main__":
    main()
