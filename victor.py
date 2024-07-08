import pandas as pd
from tabulate import tabulate

# Definir la tabla de interrupciones
interrupt_table = [
    [0, 1, "Reloj de Sistema"],
    [1, 2, "Teclado"],
    [2, None, "Reservada al Controlador PIC"],
    [3, 11, "COM2 y COM4"],
    [4, 12, "COM1 y COM3"],
    [5, 13, "Libre"],
    [6, 14, "Controlador Floppy"],
    [7, 15, "Puerto Paralelo - Impresora"],
    [8, 3, "Reloj (tics) en tiempo real CMOS"],
    [9, 4, "Libre para Tarjeta de Red, Sonido, Puerto SCSI"],
    [10, 5, "Libre"],
    [11, 6, "Libre"],
    [12, 7, "PS-Mouse"],
    [13, 8, "Co-Procesador Matemático"],
    [14, 9, "Canal IDE Primario"],
    [15, 10, "Libre (otro adaptadores)"]
]

interrupt_df = pd.DataFrame(interrupt_table, columns=["IRQ", "Prioridad", "Función"])

def display_interrupt_table():
    print(tabulate(interrupt_df, headers='keys', tablefmt='grid'))

def main():
    while True:
        print("\n=== Menu Principal ===")
        print("1. Crear tabla de interrupciones")
        print("2. Salir")
        
        choice = input("Selecciona una opción: ")
        
        if choice == '1':
            iniciar_proceso()
        elif choice == '2':
            break
        else:
            print("Opción no válida, intenta de nuevo.")

def iniciar_proceso():
    tiempo_inicial = int(input("Ingresa el tiempo inicial del programa general: "))
    tiempo_final = int(input("Ingresa el tiempo final del programa general: "))

    interrupciones = []

    while True:
        display_interrupt_table()
        
        segundo = int(input("Ingresa el segundo en el que sucede la interrupción: "))
        codigo_interrupcion = int(input("Ingresa el código de interrupción (IRQ): "))
        duracion = int(input("Ingresa la duración de la interrupción: "))
        
        interrupciones.append([segundo, codigo_interrupcion, duracion])
        
        another = input("¿Deseas añadir otra interrupción? (s/n): ")
        if another.lower() != 's':
            break
    
    timestamps = []

    print("")
    for i in range(6):
        timestamp = int(input(f"Ingresa el timestamp {i+1} para la bitácora: "))
        timestamps.append(timestamp)

    generar_informes(interrupciones, tiempo_inicial, tiempo_final, timestamps)

def generar_informes(interrupciones, tiempo_inicial, tiempo_final, timestamps):
    interrupciones_df = pd.DataFrame(interrupciones, columns=["Segundo", "IRQ", "Duración"])
    
    # Agregar la prioridad y la función al DataFrame de interrupciones
    interrupciones_df = interrupciones_df.merge(interrupt_df[['IRQ', 'Prioridad', 'Función']], on='IRQ')
    
    # Ordenar las interrupciones por segundo y prioridad
    interrupciones_df = interrupciones_df.sort_values(by=['Segundo', 'Prioridad'])
    
    # Generar Tabla de Datos
    print("\n=== Tabla de Datos ===")
    print(tabulate(interrupciones_df, headers='keys', tablefmt='grid'))
    
    # Generar la cola de procesos
    print("\n=== Cola de Procesos ===")
    cola_procesos = []
    for segundo in range(tiempo_inicial, tiempo_final + 1):
        active_irqs = interrupciones_df[(interrupciones_df["Segundo"] <= segundo) & 
                                        (interrupciones_df["Segundo"] + interrupciones_df["Duración"] > segundo)]
        if not active_irqs.empty:
            for _, row in active_irqs.iterrows():
                cola_procesos.append([segundo, row["IRQ"]])
    
    cola_procesos_df = pd.DataFrame(cola_procesos, columns=["Segundo", "IRQ"])
    print(tabulate(cola_procesos_df, headers='keys', tablefmt='grid'))
    
    # Generar la bitácora final
    print("\n=== Bitácora Final ===")
    bitacora_final = []
    
    total_duracion = (tiempo_final - tiempo_inicial) + interrupciones_df["Duración"].sum()
    en_proceso = None
    tiempo_restante = 0
    interrupciones_pendientes = []

    for segundo in range(tiempo_inicial, total_duracion + 1):
        active_irqs = interrupciones_df[(interrupciones_df["Segundo"] == segundo)]
        if not active_irqs.empty:
            # Seleccionar la interrupción de mayor prioridad
            highest_priority_irq = active_irqs.iloc[0]
            if en_proceso is None or highest_priority_irq['Prioridad'] < en_proceso['Prioridad']:
                if en_proceso is not None:
                    interrupciones_pendientes.append((en_proceso, tiempo_restante))
                en_proceso = highest_priority_irq
                tiempo_restante = en_proceso['Duración']
            else:
                tiempo_restante -= 1
                if tiempo_restante <= 0:
                    en_proceso = None
        else:
            if en_proceso is not None:
                tiempo_restante -= 1
                if tiempo_restante <= 0:
                    en_proceso = None
                    if interrupciones_pendientes:
                        en_proceso, tiempo_restante = interrupciones_pendientes.pop()
        
        if segundo in timestamps:
            if en_proceso is None:
                bitacora_final.append([segundo, "Programa", "No", f"{segundo}-{segundo+1}", "N/A"])
            else:
                bitacora_final.append([segundo, en_proceso["Función"], "No", f"{en_proceso['Segundo']}-{en_proceso['Segundo'] + en_proceso['Duración']}", tiempo_restante])
    
    bitacora_final_df = pd.DataFrame(bitacora_final, columns=["Timestamp Monitoreado (s)", "Dispositivo", "Interrupción Afecta", "Rango de Tiempo", "Tiempo Restante de Interrupción"])
    print(tabulate(bitacora_final_df, headers='keys', tablefmt='grid'))

    # Total de duración del proceso
    print(f"\nTotal de duración del proceso: {total_duracion} segundos")

if __name__ == "__main__":
    main()