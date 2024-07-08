class InterruptHandler:
    def _init_(self):
        self.interrupts = {
            "Reloj del sistema": 0,
            "Teclado": 1,
            "COM 2 y COM4": 3,
            "COM 1 y COM3": 4,
            "Libre": 5,
            "Controlador Floppy - Diskette": 6,
            "Puerto Paralelo - Impresora": 7,
            "Reloj (tics) en tiempo real CMOS": 8,
            "Libre para tarjeta de red, sonido, puerto SCSI": 9,
            "Libre (igual que el anterior)": 10,
            "PS-mouse": 12,
            "Co-procesador matemático": 13,
            "Canal IDE primario": 14,
            "Libre (otros adaptadores)": 15
        }
        self.queue = []
        self.log = []

    def handle_interrupt(self, device, duration):
        irq = self.interrupts.get(device, -1)
        if irq == -1:
            self.log.append(f"Error: Dispositivo '{device}' no encontrado en la lista de interrupciones.")
            return
        
        self.log.append(f"Interrupción recibida: {device} (IRQ {irq}), duración: {duration} segundos")

        self.queue.append((device, duration, irq))

    def print_device_list(self):
        print("\nListado de Dispositivos (ordenados por IRQ)")
        print(f"{'IRQ':<5} {'Dispositivo':<40}")
        sorted_interrupts = sorted(self.interrupts.items(), key=lambda x: x[1])
        for device, irq in sorted_interrupts:
            print(f"{irq:<5} {device:<40}")

    def print_process_control(self):
        print("\nTabla de datos")
        print(f"{'Dispositivo':<30} {'Duración':<15}")
        for device, duration, irq in self.queue:
            print(f"{device:<30} {duration:<15} segundos")

    def print_interrupt_log(self):
        print("\nBitácora de Interrupciones")
        for entry in self.log:
            print(entry)


def parse_duration(duration_str):
    try:
        duration_value = int(duration_str.split()[0])
        return duration_value
    except ValueError:
        print("Error: La duración debe ser un número seguido de 's' (por ejemplo, 8s)")
        return None


if _name_ == "_main_":
    handler = InterruptHandler()

    # Solicitar inicio y fin del programa general
    inicio = input("Ingrese el inicio del programa general: ")
    fin = input("Ingrese el fin del programa general: ")
    print(f"Programa general desde {inicio} hasta {fin}")

    while True:
        handler.print_device_list()  # Mostrar lista de dispositivos ordenados por IRQ
        device = input("Ingrese el número del dispositivo (por ejemplo, 1) o 'fin' para terminar: ")
        if device.lower() == 'fin':
            break
        
        try:
            device_num = int(device)
            if device_num < 1 or device_num > len(handler.interrupts):
                print("Error: Seleccione un número válido de dispositivo.")
                continue

            device_name = list(handler.interrupts.keys())[device_num - 1]
            duration = input(f"Ingrese la duración para {device_name} en segundos (por ejemplo, 8): ")

            duration_value = parse_duration(duration)
            if duration_value is not None:
                handler.handle_interrupt(device_name, duration_value)

                handler.print_process_control()
                handler.print_interrupt_log()

        except ValueError:
            print("Error: Ingrese un número entero válido para seleccionar el dispositivo.")