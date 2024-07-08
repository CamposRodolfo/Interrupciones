import os
from prettytable import PrettyTable

# Declaración de las Tablas

# Tabla de IRQ (Tabla de Prioridades)
TablaPrioridad = PrettyTable()
TablaPrioridad.field_names = ["#", "IRQ", "Prioridad", "Dispositivo"]
TablaPrioridad.add_rows(
    [
        [1, 0, 1, "Reloj del sistema"],
        [2, 1, 2, "Teclado"],
        [3, 2, 15, 'Reservada al controlador PIC ("Programmable Interrupt Controller")'],
        [4, 3, 11, "COM 2"],
        [5, 3, 11, "COM 4"],
        [6, 4, 12, "COM 1"],
        [7, 4, 12, "COM 3"],
        [8, 5, 13, "Libre"],
        [9, 6, 14, "Controlador Floppy"],
        [10, 6, 14, "Diskette"],
        [11, 7, 15, "Puerto Paralelo"],
        [12, 7, 15, "Impresora"],
        [13, 8, 3, "Reloj (tics) en tiempo real CMOS"],
        [14, 9, 4, "Libre para tarjeta de red"],
        [15, 9, 4, "Sonido"],
        [16, 9, 4, "Puerto SCSI"],
        [17, 10, 5, "Libre (igual que el anterior)"],
        [18, 11, 6, "Libre (igual que el anterior)"],
        [19, 12, 7, "PS-mouse"],
        [20, 13, 8, "Co-procesador matemático"],
        [21, 14, 9, "Canal IDE primario"],
        [22, 15, 10, "Libre (otros adaptadores)"]
    ]
)

# Tabla de Programa Principal
TablaPrograma = PrettyTable()
TablaPrograma.field_names = ["Tiempo Inicial", "Tiempo Final"]
TablaPrograma.add_row([0, 0])

# Tabla de Datos
TablaDatos = PrettyTable()
TablaDatos.field_names = ["Interrupción", "Dispositivo", "Duración"]

# Tabla de Diagrama de Cola de Procesos
TablaColaProcesos = PrettyTable()

# Tabla de Diagrama de Control de Procesos
TablaControlProcesos = PrettyTable()

# Tabla de Bitácora
TablaBitacoraInterrupciones = PrettyTable()
TablaBitacoraInterrupciones.field_names = ["Tiempo Real", "Área de Dispositivo", "¿Fue Interrumpido?", "Rango de Tiempo en Dispositivo", "Tiempo Faltante"]

# Declaración de Funciones

# Ingresar Número Entero
def EntradaNumero(mensaje):
    NumeroInvalido = True
    while NumeroInvalido:
        try:
            numero = int(input(mensaje))
            return numero
        except ValueError:
            print("\nEntrada Incorrecta. Por favor introduzca un número válido.")
            print("Vuelve a intentarlo.\n")

# Función para ingresar el tiempo
def EntradaTiempo(mensaje):
    NumeroInvalido = True
    while NumeroInvalido:
        tiempo = EntradaNumero(mensaje)
        if tiempo >= 0:
            print("\nEl número del tiempo seleccionado fue: ", tiempo)
            NumeroInvalido = False
            return tiempo
        else:
            print("\nEntrada Incorrecta. Por favor introduzca un número válido.")
            print("Vuelva a intentarlo.\n")

# Función para seleccionar el dispositivo
def EntradaDispositivo(mensaje):
    limpiar_pantalla()
    while True:
        print(TablaPrioridad)
        NumeroDispositivo = EntradaNumero(mensaje)
        if NumeroDispositivo > 0 and NumeroDispositivo <= 22:
            print("\nEl número del dispositivo seleccionado fue: ", NumeroDispositivo)
            data = TablaPrioridad._rows
            Dispositivo = None
            for fila in data:
                if fila[0] == NumeroDispositivo:
                    Dispositivo = fila[3]
            print("\nEl dispositivo seleccionado fue: ", Dispositivo)
            return Dispositivo
        else:
            print("\nEntrada Incorrecta. Por favor introduzca un número válido.")
            print("Vuelva a intentarlo.\n")

# Declarar Tabla de Datos
def InicializarTablaDeDatos():
    TablaPrograma.rows[0][0] = EntradaTiempo("\nIntroduzca el tiempo inicial para el programa:\n>>> ")
    TablaPrograma.rows[0][1] = EntradaTiempo("\nIntroduzca el tiempo final para el programa:\n>>> ")

    ImprimirTablaPrograma()

    MasInterrupciones = True
    while MasInterrupciones:
        Dispositivo = EntradaDispositivo("\nIngrese el número del dispositivo de la Interrupción:\n>>> ")
        TiempoInterrupcion = EntradaTiempo("\nIngrese el tiempo donde se dió la Interrupción:\n>>> ")
        TiempoDuracion = EntradaTiempo("\nIngrese la duración de la Interrupción:\n>>> ")
        TablaDatos.add_row([TiempoInterrupcion, Dispositivo, TiempoDuracion])
        while True:
            seleccion = EntradaNumero('\n\nDesea agregar más interrupciones?\nIntroduzca "1" para introducir más interrupciones, "0" para no introducir más.\n>>> ')
            if seleccion == 0:
                MasInterrupciones = False
                break
            elif seleccion == 1:
                MasInterrupciones = True
                break
            else:
                print("\nSeleccione un número válido.\n")

    ImprimirTablaPrograma()

def ImprimirTablaPrograma():
    print("\n+------------------+----------------+")
    print("| Tiempo Inicial   | Tiempo Final   |")
    print("+------------------+----------------+")
    print("|", TablaPrograma.rows[0][0], "              |", TablaPrograma.rows[0][1], "               |")
    print("+------------------+----------------+\n")
    print(TablaDatos)

# Trabajar en la Tabla de Cola de Procesos
def InicializarColaProcesos():
    print("Diagrama De Cola de Procesos")
    dispositivos = [f"{fila[1]}" for fila in TablaDatos._rows]
    tiempos_faltantes = [f"{fila[2]}" for fila in TablaDatos._rows]
    TablaColaProcesos.add_column("Dispositivo", dispositivos)
    TablaColaProcesos.add_column("", tiempos_faltantes)
    print(TablaColaProcesos)

# Trabajar en la Tabla de Cola de Procesos
def AgregarColaProcesos(dispositivo, tiempo_faltante):
    # Buscar la fila donde el primer valor coincide con dispositivo
    for fila in TablaColaProcesos._rows:
        if fila[0] == dispositivo:
            fila[1] = tiempo_faltante
            break
    else:
        # Si no se encuentra el dispositivo, agregar una nueva fila
        TablaColaProcesos.add_row([dispositivo, tiempo_faltante])

    print(TablaColaProcesos)

# Diagrama De Control de Procesos
def InicializarControlProcesos():
    print("Inicializar Control de Procesos")
    # Obtener dispositivos únicos
    dispositivos = list(set([fila[1] for fila in TablaDatos._rows]))
    TablaControlProcesos.field_names = ["Tiempo","Detalle", "Programa"] + dispositivos
    tiempos_iniciales = [0 for _ in dispositivos]
    TablaControlProcesos.add_row([0, "En ejecución", "T=0"] + tiempos_iniciales)

    for fila in TablaDatos._rows:
        tiempo, dispositivo, duracion = fila
        nueva_fila = [tiempo, f"Interrumpido por {dispositivo}"]
        for d in dispositivos:
            if d == dispositivo:
                nueva_fila.append(f"T={tiempo}")
            else:
                nueva_fila.append("")
        TablaControlProcesos.add_row(nueva_fila)
        fin_interrupcion = tiempo + duracion
        nueva_fila = [fin_interrupcion, "En ejecución"]
        for d in dispositivos:
            if d == dispositivo:
                nueva_fila.append(f"T={fin_interrupcion}(Dur. {duracion}s)")
            else:
                nueva_fila.append("")
        TablaControlProcesos.add_row(nueva_fila)

    # Ajustar ancho de columnas
    for i, nombre in enumerate(TablaControlProcesos.field_names):
        TablaControlProcesos.align[nombre] = "c"
        if i > 1:  # Ajustar solo columnas de dispositivos
            TablaControlProcesos.max_width[nombre] = 15

    print(TablaControlProcesos)

# Trabajar en la Tabla de Bitácora
def DiagramaBitacoraInterrupciones():
    tiempos_reales = []
    MasTiemposReales = True
    while MasTiemposReales:
        tiempo_real = EntradaTiempo("Introduzca el tiempo real para la bitácora:\n>>> ")
        tiempos_reales.append(tiempo_real)
        while True:
            seleccion = EntradaNumero('\n\nDesea agregar más tiempos reales?\nIntroduzca "1" para agregar más tiempos reales, "0" para no agregar más.\n>>> ')
            if seleccion == 0:
                MasTiemposReales = False
                break
            elif seleccion == 1:
                MasTiemposReales = True
                break
            else:
                print("\nSeleccione un número válido.\n")

    # Obtener dispositivos únicos
    dispositivos = list(set([fila[1] for fila in TablaDatos._rows]))

    for tiempo_real in tiempos_reales:
        area_dispositivo = "En ejecución"
        fue_interrumpido = "No"
        rango_tiempo = "-"
        tiempo_faltante = "-"

        for fila in TablaDatos._rows:
            tiempo, dispositivo, duracion = fila
            if tiempo <= tiempo_real < tiempo + duracion:
                area_dispositivo = dispositivo
                fue_interrumpido = "Sí"
                rango_tiempo = f"{tiempo}-{tiempo + duracion}"
                tiempo_faltante = max(0, (tiempo + duracion) - tiempo_real)
                break

        TablaBitacoraInterrupciones.add_row([tiempo_real, area_dispositivo, fue_interrumpido, rango_tiempo, tiempo_faltante])

    print(TablaBitacoraInterrupciones)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main
if __name__ == "__main__":
    limpiar_pantalla()
    InicializarTablaDeDatos()
    InicializarColaProcesos()
    InicializarControlProcesos()
    DiagramaBitacoraInterrupciones()
