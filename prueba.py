## Intalar Antes
## PrettyTable
## python -m pip install -U prettytable

from prettytable import PrettyTable

TablaPriodidad = PrettyTable()
TablaPriodidad.field_names = ["#", "IRQ", "Prioridad", "Dispositivo"]
TablaPriodidad.add_rows(
    [
        [1, 0, 1, "Reloj del sistema"],
        [2, 1, 2, "Teclado"],
        [3, 2, 15, 'Reservada al controlador PIC ("Programmable Interrupt Controller").'],
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
        [15, 9, 4, "sonido"],
        [16, 9, 4, "puerto SCSI"],
        [17, 10, 5, "Libre (igual que el anterior)"],
        [18, 11, 6, "Libre (igual que el anterior)"],
        [19, 12, 7, "PS-mouse"],
        [20, 13, 8, "Co-procesador matemático"],
        [21, 14, 9, "Canal IDE primario"],
        [22, 15, 10, "Libre (otros adaptadores)"]
    ]
)

TablaDatos = PrettyTable()
TablaDatos.field_names = ["Interrupcion", "Dispositivo", "Duración"]

ColaProcesos = PrettyTable()
ColaProcesos.field_names = ["Dispositivo", "TP1", "TP2", "TP3", "TP4"]

DiagramaControlProcesos = PrettyTable()
DiagramaControlProcesos.field_names = ["",]


def EntradaNumero():
    NumeroInvalido = True
    while NumeroInvalido:
        try:
            numero = int(input("Introduzca un número entero: "))
            return numero
        except ValueError:
            print("Entrada Incorrecta. Porfavor Introduzca un número valido.")
            print("Vuelve a intentarlo.")
            
            
def EntradaTiempo():
    NumeroInvalido = True
    while NumeroInvalido:
        tiempo = EntradaNumero()
        if tiempo>=0:
            print("El número del tiempo seleccionado fue: ", tiempo)
            NumeroInvalido = False
            return tiempo
            break
        else:
            print("Entrada Incorrecta. Porfavor Introduzca un número valido.")
            print("Vuelva a intentarlo.")
            

def EntradaDispositivo():
    NumeroInvalido = True
    while NumeroInvalido:
        print(TablaPriodidad)
        print("Ingrese el número del dispositivo de la Interrupción")
        NumeroDispositivo = EntradaNumero()
        if NumeroDispositivo>0 and NumeroDispositivo<=22:
            print("El número del dispositivo seleccionado fue: ", NumeroDispositivo)
            NumeroInvalido = False
            data = TablaPriodidad._rows
            
            Dispositivo = None
            for fila in data:
                if fila[0] == NumeroDispositivo:
                    Dispositivo = fila[3]
            
            print("El dispositivo seleccionado fue: ", Dispositivo)
            return Dispositivo
            break
        else:
            print("Entrada Incorrecta. Porfavor Introduzca un número valido.")
            print("Vuelva a intentarlo.")



def InsertarTablaDeDatos():
    MasInterrupciones = True
    
    while MasInterrupciones:
        print("Ingrese el tiempo de la Interrupción: ")
        TiempoInterrupcion = EntradaTiempo()
        
        Dispositivo = EntradaDispositivo()
        
        print("Ingrese la duración de la Interrupción: ")
        TiempoDuracion = EntradaTiempo()
        
        TablaDatos.add_row([TiempoInterrupcion,Dispositivo,TiempoDuracion])
        
        while True:
            print("Desea agregar más interrupciones?")
            print('Introduzca "1" para intoducir más interruciones, "0" para no introducir más.')
            seleccion = EntradaNumero()
            if seleccion==0:
                MasInterrupciones = False
                break
            elif seleccion==1:
                MasInterrupciones = True
                break
            else:
                print("Slececiones un numero valido.")
    
    
# def AnchoColaProcesos():
#     a


# def AnchoDiagramaControlProcesos():
#     a
    


# Seccion Decalarativa
continuar = True
print("Introduzca un del tiempo Inicial para el programa")
T0 = EntradaTiempo()
print("Introduzca un del tiempo final para el programa")
Tf = EntradaTiempo()

print("+--------------+-------------+----------+")
print("|              Tabla De Datos           |")
print("+---------------------------------------+")
print("|   Programa:      T0:", T0, "      Tf:", Tf, "  |")
print("+--------------+-------------+----------+\n")

print(TablaDatos)

InsertarTablaDeDatos()


print("+--------------+-------------+----------+")
print("|              Tabla De Datos           |")
print("+---------------------------------------+")
print("|   Programa:      T0:", T0, "      Tf:", Tf, "  |")
print("+--------------+-------------+----------+\n")
print(TablaDatos)
    
    # Seccion de Procesos
    
# print(TablaPriodidad)
    # while continuar:
    #     AgregarDispositivo()
        
        
    # Seccion de Try Catch