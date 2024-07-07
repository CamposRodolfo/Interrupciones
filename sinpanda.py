class InterruptHandler:
    def __init__(self):
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
        self.program_priority = float('inf')
        self.queue = []
        self.log = []

    def handle_interrupt(self, device, duration):
        irq = self.interrupts.get(device, -1)
        if irq == -1:
            self.log.append(f"Error: Dispositivo '{device}' no encontrado en la lista de interrupciones.")
            return
        
        name, priority = device, irq  # Prioridad basada en el IRQ
        self.log.append(f"Interrupción recibida: {name} (IRQ {irq}), duración: {duration}, prioridad: {priority}")
        
        if priority < self.program_priority:
            self.log.append(f"Interrupción aceptada: {name} (IRQ {irq})")
            if self.queue:
                remaining_time, queued_irq = self.queue.pop(0)
                self.log.append(f"Guardando tiempo restante: {remaining_time} para {self.interrupts[queued_irq]} (IRQ {queued_irq}) en la cola de procesos")
            self.program_priority = priority
            self.queue.append((duration, irq))
        else:
            self.log.append(f"Interrupción rechazada: {name} (IRQ {irq})")
            self.queue.append((duration, irq))

    def parse_duration(self, duration_str):
        try:
            duration_value = int(duration_str.split()[0])
            return duration_value
        except ValueError:
            print("Error: La duración debe ser un número seguido de 's' (por ejemplo, 8s)")
            return None

    def print_device_list(self):
        print("\nListado de Dispositivos (ordenados por IRQ)")
        print(f"{'IRQ':<5} {'Dispositivo':<40} {'Prioridad':<10}")
        sorted_interrupts = sorted(self.interrupts.items(), key=lambda x: x[1])
        for device, irq in sorted_interrupts:
            print(f"{irq:<5} {device:<40} {irq:<10}")

    def print_process_control(self):
        print("\nTabla de datos")
        print(f"{'Dispositivos':<30} {'Interrupción':<15} {'Duración':<10}")
        if self.queue:
            duration, irq = self.queue[0]
            device = [dev for dev, val in self.interrupts.items() if val == irq][0]
            print(f"{device:<30} {irq:<15} {duration:<10}")

    def print_process_queue(self):
        print("\nCola de Procesos")
        headers = ["Dispositivos", "TP1", "TP2", "TP3"]
        print(" | ".join(headers))
        for i, (duration, irq) in enumerate(self.queue):
            if i == 0:
                device = [dev for dev, val in self.interrupts.items() if val == irq][0]
                row = [device] + ["" for _ in range(len(headers) - 1)]
                row[i + 1] = str(duration)
                print(" | ".join(row))

    def print_interrupt_log(self):
        print("\nBitácora de Interrupciones")
        for entry in self.log:
            print(entry)


if __name__ == "__main__":
    handler = InterruptHandler()

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
            interrupt = handler.interrupts[device_name]
            duration = input(f"Ingrese la duración para {device_name} (por ejemplo, 8s): ")

            duration_value = handler.parse_duration(duration)
            if duration_value is not None:
                handler.handle_interrupt(device_name, duration_value)

                handler.print_process_control()
                handler.print_process_queue()
                handler.print_interrupt_log()

        except ValueError:
            print("Error: Ingrese un número entero válido para seleccionar el dispositivo.")
