from prettytable import PrettyTable

# Declaración de las Tablas
TablaPrioridad = PrettyTable()
TablaPrioridad.field_names = ["#", "IRQ", "Prioridad", "Dispositivo"]
TablaPrioridad.add_rows(
    [
        [1, 0, 1, "Reloj del sistema"],
        [2, 1, 2, "Teclado"],
        [3, 2, 16, 'Reservada al controlador PIC ("Programmable Interrupt Controller")'],
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

TablaPrograma = PrettyTable()
TablaPrograma.field_names = ["Tiempo Inicial", "Tiempo Final"]
TablaPrograma.add_row([0, 0])

TablaDatos = PrettyTable()
TablaDatos.field_names = ["Interrupción", "Dispositivo", "Duración"]

TablaColaProcesos = PrettyTable()

TablaControlProcesos = PrettyTable()

TablaAuditoria = PrettyTable()
TablaAuditoria.field_names = ["Tiempo Real", "Área de Dispositivo", "¿Fue Interrumpido?", "Rango inicial", "Rango final", "Tiempo faltante"]

TablaBitacoraInterrupciones = PrettyTable()
TablaBitacoraInterrupciones.field_names = ["Tiempo Real", "Área de Dispositivo", "¿Fue Interrumpido?", "Rango de Tiempo en Dispositivo", "Tiempo Faltante"]

# Declaración de Funciones

def EntradaNumero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("\nEntrada Incorrecta. Por favor introduzca un número válido.\n")

def EntradaTiempo(mensaje):
    while True:
        tiempo = EntradaNumero(mensaje)
        if tiempo >= 0:
            print("\nEl número del tiempo seleccionado fue: ", tiempo)
            return tiempo
        else:
            print("\nEntrada Incorrecta. Por favor introduzca un número válido.\n")

def EntradaDispositivo(mensaje):
    while True:
        print(TablaPrioridad)
        NumeroDispositivo = EntradaNumero(mensaje)
        if 0 < NumeroDispositivo <= 22:
            print("\nEl número del dispositivo seleccionado fue: ", NumeroDispositivo)
            data = TablaPrioridad._rows
            Dispositivo = None
            for fila in data:
                if fila[0] == NumeroDispositivo:
                    Dispositivo = fila[3]
            print("\nEl dispositivo seleccionado fue: ", Dispositivo)
            return Dispositivo
        else:
            print("\nEntrada Incorrecta. Por favor introduzca un número válido.\n")

def obtener_prioridad(dispositivo):
    for fila in TablaPrioridad._rows:
        if fila[3] == dispositivo:
            return fila[2]
    return float('inf')  # Retorna un valor muy alto si el dispositivo no se encuentra en la tabla

def InicializarTablaDeDatos():
    TablaPrograma.rows[0][0] = EntradaTiempo("\nIntroduzca el tiempo inicial para el programa:\n>>> ")
    TablaPrograma.rows[0][1] = EntradaTiempo("\nIntroduzca el tiempo final para el programa:\n>>> ")
    
    ImprimirTablaPrograma()
    
    while True:
        Dispositivo = EntradaDispositivo("\nIngrese el número del dispositivo de la Interrupción:\n>>> ")
        TiempoInterrupcion = EntradaTiempo("\nIngrese el tiempo donde se dió la Interrupción:\n>>> ")
        TiempoDuracion = EntradaTiempo("\nIngrese la duración de la Interrupción:\n>>> ")
        TablaDatos.add_row([TiempoInterrupcion, Dispositivo, TiempoDuracion])
        
        seleccion = EntradaNumero('\n\nDesea agregar más interrupciones?\nIntroduzca "1" para introducir más interrupciones, "0" para no introducir más.\n>>> ')
        if seleccion == 0:
            break

    ImprimirTablaPrograma()

def InicializarColaProcesos():
    print("Diagrama De Cola de Procesos")
    dispositivos = [fila[1] for fila in TablaDatos._rows]
    tiempos_iniciales = [f"T={fila[2]}" for fila in TablaDatos._rows]
    TablaColaProcesos.add_column("Dispositivo", dispositivos)
    TablaColaProcesos.add_column("TP1", tiempos_iniciales)

def AgregarColaProcesos(dispositivo, tiempo):
    for fila in TablaColaProcesos._rows:
        if fila[0] == dispositivo:
            for i in range(1, len(fila)):
                if not fila[i]:
                    fila[i] = tiempo
                    break
            else:
                nueva_columna = f"TP{len(TablaColaProcesos.field_names)}"
                TablaColaProcesos.field_names.append(nueva_columna)
                TablaColaProcesos._align[nueva_columna] = 'c'
                TablaColaProcesos._valign[nueva_columna] = 't'
                for f in TablaColaProcesos._rows:
                    f.append("-")
                fila[-1] = tiempo
                break
    print(TablaColaProcesos)

def obtener_siguiente_interrupcion(tiempo_real, interrupciones_pendientes):
    interrupciones = [(fila[0], fila[1], fila[2]) for fila in interrupciones_pendientes if fila[0] >= tiempo_real]
    if interrupciones:
        return min(interrupciones, key=lambda x: (x[0], obtener_prioridad(x[1])))
    return None

def ControlProcesos():
    print("Inicializar Control de Procesos")
    tiempo_real = 0
    dispositivos = list(set([fila[1] for fila in TablaDatos._rows]))
    TablaControlProcesos.field_names = ["Tiempo", "Detalle", "Programa"] + dispositivos
    tiempos_iniciales = [""] * len(dispositivos)
    TablaControlProcesos.add_row([tiempo_real, "Inicio Programa", f"T={tiempo_real}"] + tiempos_iniciales)
    
    interrupciones_pendientes = [list(fila) for fila in TablaDatos._rows]
    programa_tiempo_restante = TablaPrograma.rows[0][1] - TablaPrograma.rows[0][0]
    programa_interrumpido = False

    while interrupciones_pendientes or programa_tiempo_restante > 0:
        siguiente_interrupcion = obtener_siguiente_interrupcion(tiempo_real, interrupciones_pendientes)
        if siguiente_interrupcion:
            tiempo_interrupcion, dispositivo, duracion = siguiente_interrupcion
            if tiempo_interrupcion > tiempo_real:
                # Procesar el tiempo restante del programa hasta la siguiente interrupción
                tiempo_avance = min(tiempo_interrupcion - tiempo_real, programa_tiempo_restante)
                if tiempo_avance > 0:
                    nueva_fila = [tiempo_real, "En ejecución", f"T={tiempo_real}"] + [""] * len(dispositivos)
                    TablaControlProcesos.add_row(nueva_fila)
                    tiempo_real += tiempo_avance
                    programa_tiempo_restante -= tiempo_avance
                    nueva_fila = [tiempo_real, "Programa interrumpido", f"T={tiempo_real}(Dur. {tiempo_avance}s)"] + [""] * len(dispositivos)
                    TablaControlProcesos.add_row(nueva_fila)

            # Procesar la interrupción
            if programa_interrumpido and programa_tiempo_restante > 0:
                nueva_fila = [tiempo_real, "Reanudación del programa", f"T={tiempo_real}"] + [""] * len(dispositivos)
                TablaControlProcesos.add_row(nueva_fila)
                programa_interrumpido = False
            
            tiempo_real = tiempo_interrupcion
            nueva_fila = [tiempo_real, f"Interrumpido por {dispositivo}", ""] + [""] * len(dispositivos)
            indice_dispositivo = dispositivos.index(dispositivo)
            nueva_fila[indice_dispositivo + 3] = f"T={tiempo_real}"
            TablaControlProcesos.add_row(nueva_fila)
            
            # Verificar interrupciones de mayor prioridad durante la interrupción actual
            while duracion > 0:
                tiempo_real += 1
                duracion -= 1
                siguiente_interrupcion_durante = obtener_siguiente_interrupcion(tiempo_real, interrupciones_pendientes)
                if siguiente_interrupcion_durante and obtener_prioridad(siguiente_interrupcion_durante[1]) < obtener_prioridad(dispositivo):
                    nueva_fila = [tiempo_real, f"Interrumpido por {siguiente_interrupcion_durante[1]}", ""] + [""] * len(dispositivos)
                    indice_dispositivo_nuevo = dispositivos.index(siguiente_interrupcion_durante[1])
                    nueva_fila[indice_dispositivo_nuevo + 3] = f"T={tiempo_real}"
                    TablaControlProcesos.add_row(nueva_fila)
                    interrupciones_pendientes.append((tiempo_real, dispositivo, duracion))
                    dispositivo, duracion = siguiente_interrupcion_durante[1], siguiente_interrupcion_durante[2]
                    interrupciones_pendientes.remove(list(siguiente_interrupcion_durante))
            
            nueva_fila = [tiempo_real, "Fin de interrupción", ""] + [""] * len(dispositivos)
            TablaControlProcesos.add_row(nueva_fila)
            
            tiempo_real += duracion
            nueva_fila = [tiempo_real, "En ejecución", f"T={tiempo_real}(Dur. {duracion}s)"] + [""] * len(dispositivos)
            nueva_fila[indice_dispositivo + 3] = f"T={tiempo_real}(Dur. {duracion}s)"
            TablaControlProcesos.add_row(nueva_fila)
            
            interrupciones_pendientes.remove(list(siguiente_interrupcion))
            programa_interrumpido = True
            
            # Imprimir la tabla de control de procesos en cada iteración
            print(TablaControlProcesos)
        else:
            # Procesar el tiempo restante del programa
            if programa_tiempo_restante > 0:
                nueva_fila = [tiempo_real, "En ejecución", f"T={tiempo_real}"] + [""] * len(dispositivos)
                TablaControlProcesos.add_row(nueva_fila)
                tiempo_real += programa_tiempo_restante
                programa_tiempo_restante = 0
                nueva_fila = [tiempo_real, "Fin del programa", f"T={tiempo_real}(Dur. {tiempo_real - TablaPrograma.rows[0][0]}s)"] + [""] * len(dispositivos)
                TablaControlProcesos.add_row(nueva_fila)
                # Imprimir la tabla de control de procesos al finalizar
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

def ImprimirTablaPrograma():
    print("+--------------+-------------+----------+")
    print("|              Tabla De Datos           |")
    print("+---------------------------------------+")
    print("|   Programa:      Ti:", TablaPrograma.rows[0][0], "      Tf:", TablaPrograma.rows[0][1], "  |")
    print("+--------------+-------------+----------+\n")
    print(TablaDatos)

def main():
    InicializarTablaDeDatos()
    InicializarColaProcesos()
    ControlProcesos()
    DiagramaBitacoraInterrupciones()

if __name__ == "__main__":
    main()
