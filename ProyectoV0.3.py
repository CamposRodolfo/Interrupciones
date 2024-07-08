#Importación

import os

# Instalar PrettyTable
# python -m pip install -U prettytable
from prettytable import PrettyTable




#Declaración de las Tablas

#Tabla de IRQ (Tabla de Prioridades)
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


#Tabla de Programa Principal
TablaPrograma = PrettyTable()
TablaPrograma.field_names = ["Tiempo Inicial", "Tiempo Final"]
TablaPrograma.add_row([0,0])


#Tabla de Datos
TablaDatos = PrettyTable()
TablaDatos.field_names = ["Interrupción", "Dispositivo", "Duración"]


#Tabla de Diagrama de Cola de Procesos
TablaColaProcesos = PrettyTable()


#Tabla de Diagrama de Control de Procesos
TablaControlProcesos = PrettyTable()


#Tabla de Auditoría
TablaAuditoria = PrettyTable()
TablaAuditoria.field_names = ["Tiempo Real", "Área de Dispositivo" , "¿Fue Interrumpido?", "Rango inicial", "Rango final" "Tiempo faltante"]


#Tabla de Bitácora
TablaBitacoraInterrupciones = PrettyTable()
TablaBitacoraInterrupciones.field_names = ["Tiempo Real", "Área de Dispositivo", "¿Fue Interrumpido?", "Rango de Tiempo en Dispositivo", "Tiempo Faltante"]





#Declaración de Funciones

#Ingresar Número Entero
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


#Declarar Tabla de Datos
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


#Trabajar en la Tabla de Cola de Procesos
def InicializarColaProcesos():
    print("Diagrama De Cola de Procesos")
    dispositivos = [f"{fila[1]}" for fila in TablaDatos._rows]
    TablaColaProcesos.add_column("Dispositivo", dispositivos)
    

#Trabajar en la Tabla de Cola de Procesos
def AgregarColaProcesos(dispositivo, tiempo):
    # Buscar la fila donde el primer valor coincide con valor_buscar
    for fila in TablaColaProcesos._rows:
        if fila[0] == dispositivo:
            # Recorrer las columnas de la fila para encontrar una celda vacía
            for i in range(1, len(fila)):
                if fila[i] is None or fila[i] == "" or fila[i] == "-":
                    fila[i] = tiempo
                    break
            else:
                # Si no se encuentra una celda vacía, agregar una nueva columna
                nueva_columna = f"TP{len(TablaColaProcesos.field_names)}"
                TablaColaProcesos.field_names.append(nueva_columna)
                TablaColaProcesos._align[nueva_columna] = 'c'  # Establecer alineación horizontal para la nueva columna
                TablaColaProcesos._valign[nueva_columna] = 't'  # Establecer alineación vertical para la nueva columna
                for f in TablaColaProcesos._rows:
                    f.append("-")
                fila[-1] = tiempo
                break
                
    print(TablaColaProcesos)
    


#Diagrama De Control de Procesos
def InicializarControlProcesos():
    print("Inicializar Control de Procesos")
    dispositivos = [f"{fila[1]}" for fila in TablaDatos._rows]
    TablaControlProcesos.field_names = ["Programa"] + dispositivos
    TablaControlProcesos.add_row([0] + [f"-" for fila in TablaDatos._rows])
    print(TablaControlProcesos)
    

#Diagrama De Control de Procesos
def AgregarControlProcesos():
    print("Agregaar Control de Procesos")
    


#Trabajar en la Tabla de Bitácora
def DiagramaBitacoraInterrupciones():
    print("Diagrama de Bitacora de Interrupciones")




#Funcion de Impresión de Tablas

# Función para limpiar la pantalla
def limpiar_pantalla():
    # Verificar el sistema operativo
    sistema_operativo = os.name
    if sistema_operativo == 'nt':  # Windows
        _ = os.system('cls')
    else:  # Unix/Linux/MacOS
        _ = os.system('clear')


#Impresión de tabla de de Datos
def ImprimirTablaPrograma():
    print("+--------------+-------------+----------+")
    print("|              Tabla De Datos           |")
    print("+---------------------------------------+")
    print("|   Programa:      Ti:", TablaPrograma.rows[0][0], "      Tf:", TablaPrograma.rows[0][1], "  |")
    print("+--------------+-------------+----------+\n")
    print(TablaDatos)
    


#Declaración de Main
def main():
    limpiar_pantalla()
    InicializarTablaDeDatos()
    
    input("Presiona Enter para continuar...")
    limpiar_pantalla()
    InicializarColaProcesos()
    limpiar_pantalla()
    # AgregarColaProcesos()
    limpiar_pantalla()
    InicializarControlProcesos()
    limpiar_pantalla()
    DiagramaBitacoraInterrupciones()
    
if __name__ == "__main__":
    main()