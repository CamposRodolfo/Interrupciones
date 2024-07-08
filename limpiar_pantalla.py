import os

# Función para limpiar la pantalla
def limpiar_pantalla():
    # Verificar el sistema operativo
    sistema_operativo = os.name
    if sistema_operativo == 'nt':  # Windows
        _ = os.system('cls')
    else:  # Unix/Linux/MacOS
        _ = os.system('clear')

# Ejemplo de uso
print("Contenido antes de limpiar la pantalla")
input("Presiona Enter para continuar...")
limpiar_pantalla()
print("Pantalla limpiada")