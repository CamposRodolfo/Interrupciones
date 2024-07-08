# Instalar PrettyTable
# python -m pip install -U prettytable

from prettytable import PrettyTable

# Tabla de Prioridades de Dispositivos
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

# Tabla de Datos
TablaDatos = PrettyTable()
TablaDatos.field_names = ["Interrupción", "Dispositivo", "Duración"]

# Cola de Procesos
TablaColaProcesos = PrettyTable()
TablaColaProcesos.field_names = ["Dispositivo", "TP1", "TP2", "TP3", "TP4"]

# Diagrama de Control de Procesos
TablaDiagramaControlProcesos = PrettyTable()

# Bitácora de Interrupciones
TablaBitacoraInterrupciones = PrettyTable()
TablaBitacoraInterrupciones.field_names = ["Tiempo Real", "Área de Dispositivo", "Interrupción Aceptada", "Rango de Tiempo en Dispositivo", "Tiempo Faltante"]

#Tabla Auditoria
TablaAuditoria = PrettyTable()
TablaAuditoria.field_names = ["Tiempo", "Dispositivo" , "Interrumpido", "Rango inicial", "Rango final" "Tiempo faltante"]

# Función para ingresar un número entero
def EntradaNumero():
    NumeroInvalido = True
    while NumeroInvalido:
        try:
            numero = int(input("Introduzca un número entero: "))
            return numero
        except ValueError:
            print("Entrada Incorrecta. Por favor introduzca un número válido.")
            print("Vuelve a intentarlo.")

# Función para ingresar el tiempo
def EntradaTiempo():
    NumeroInvalido = True
    while NumeroInvalido:
        tiempo = EntradaNumero()
        if tiempo >= 0:
            print("El número del tiempo seleccionado fue: ", tiempo)
            NumeroInvalido = False
            return tiempo
        else:
            print("Entrada Incorrecta. Por favor introduzca un número válido.")
            print("Vuelva a intentarlo.")

# Función para seleccionar el dispositivo
def EntradaDispositivo():
    NumeroInvalido = True
    while NumeroInvalido:
        print(TablaPrioridad)
        print("Ingrese el número del dispositivo de la Interrupción")
        NumeroDispositivo = EntradaNumero()
        if NumeroDispositivo > 0 and NumeroDispositivo <= 22:
            print("El número del dispositivo seleccionado fue: ", NumeroDispositivo)
            NumeroInvalido = False
            data = TablaPrioridad._rows
            Dispositivo = None
            for fila in data:
                if fila[0] == NumeroDispositivo:
                    Dispositivo = fila[3]
            print("El dispositivo seleccionado fue: ", Dispositivo)
            return Dispositivo
        else:
            print("Entrada Incorrecta. Por favor introduzca un número válido.")
            print("Vuelva a intentarlo.")

# Función para insertar datos en la tabla de datos
def InsertarTablaDeDatos():
    MasInterrupciones = True
    while MasInterrupciones:
        print("Ingrese el tiempo de la Interrupción: ")
        TiempoInterrupcion = EntradaTiempo()
        Dispositivo = EntradaDispositivo()
        print("Ingrese la duración de la Interrupción: ")
        TiempoDuracion = EntradaTiempo()
        TablaDatos.add_row([TiempoInterrupcion, Dispositivo, TiempoDuracion])
        while True:
            print("Desea agregar más interrupciones?")
            print('Introduzca "1" para introducir más interrupciones, "0" para no introducir más.')
            seleccion = EntradaNumero()
            if seleccion == 0:
                MasInterrupciones = False
                break
            elif seleccion == 1:
                MasInterrupciones = True
                break
            else:
                print("Seleccione un número válido.")

# Función para calcular el diagrama de control de procesos
def CalcularDiagramaControlProcesos(T0, Tf):
    dispositivos = [f"{fila[1]}" for fila in TablaDatos._rows]
    TablaDiagramaControlProcesos.field_names = ["Programa"] + dispositivos
    for tiempo in range(T0, Tf + 1):
        fila = [tiempo, "Ejecutando programa principal"]
        for dispositivo in dispositivos:
            interrupcion = "No"
            for row in TablaDatos:
                if row[0] == tiempo and dispositivo.endswith(str(TablaPrioridad._rows[dispositivo - 1][2])):
                    interrupcion = "Sí"
            fila.append(interrupcion)
        TablaDiagramaControlProcesos.add_row(fila)


# Función para calcular la bitácora de interrupciones
def CalcularBitacoraInterrupciones(T0, Tf):
    for tiempo in range(T0, Tf + 1):
        for row in TablaDatos:
            if row[0] == tiempo:
                dispositivo = row[1]
                duracion = row[2]
                TablaBitacoraInterrupciones.add_row([tiempo, dispositivo, "Sí", f"{tiempo}-{tiempo + duracion}", duracion])

# Sección Declarativa
continuar = True
print("Introduzca el tiempo Inicial para el programa")
T0 = EntradaTiempo()
print("Introduzca el tiempo final para el programa")
Tf = EntradaTiempo()

# Mostrar Tabla de Datos Inicial
print("+--------------+-------------+----------+")
print("|              Tabla De Datos           |")
print("+---------------------------------------+")
print("|   Programa:      T0:", T0, "      Tf:", Tf, "  |")
print("+--------------+-------------+----------+\n")
print(TablaDatos)

# Insertar Datos en la Tabla de Datos
InsertarTablaDeDatos()

# Calcular Diagramas
CalcularDiagramaControlProcesos(T0, Tf)
CalcularBitacoraInterrupciones(T0, Tf)

# Mostrar Tablas Finales
print("+--------------+-------------+----------+")
print("|              Tabla De Datos           |")
print("+---------------------------------------+")
print("|   Programa:      T0:", T0, "      Tf:", Tf, "  |")
print("+--------------+-------------+----------+\n")
print(TablaDatos)

print("+------------------------------+")
print("|     Diagrama de Procesos     |")
print("+------------------------------+")
print(TablaDiagramaControlProcesos)

print("+------------------------------+")
print("|     Bitácora de Interrupciones     |")
print("+------------------------------+")
print(TablaBitacoraInterrupciones)












def ColaDeProceso(T0, tf):
    
    while
    
    
    
while ColaDeProcesoPrograma > 0
    TablaColaProcesos= programa, EntradaTiempo
    tiempoTotal = 0
    tiempoPrograma = 0
    if hayinterrupcion:
        tablaColaProcesos= agregar dispositivo, tiempo
        ColaDeProceso= ColaDeProceso - 1
    if maximaPrioridad = prioridadComparada
        maximaprioriada = seguir trabajando
        ColaDeProceso= ColaDeProceso - 1
    elif maxima priodad > prioridadComparda
        maximaprioridad = trabajar
        prioridadcomprada = pausa
        ColaDeProceso= ColaDeProceso - 1
    else:
        programa = continuar
    
    tiempototal = tiempototal + 1
    















def BitacoraProcesos ():
    tiempoAuditoria = input

    verificar NombreTiempoDispositivo en TablaAuditoria con tiempoAuditoria
   
    while Nombretiempodispositivo == TablaAuditoria
        busquedaTiempo = busquedaTiempo - 1
        guardar tiempo
    while nombretiempodispositivo == TablaAuditoria
        busquedaTiempo = busquedaTirmpo + 1
        guardar tiempo    

    if procesodispositivo = completo:
        NO interrunpido en TablaBitacoraInterrupciones
        tiempoPrograma = tiempoPrograma - tiempointerrumpido
    elif procesodispositivo = incompleto
        Si interrumoido en TablaBitacoraInterrupciones

    rango = [tiempofinal, tiempo inicial]
        

