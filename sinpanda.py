class InterruptHandler:
    def __init__(self):
        self.interrupts = {
            0: ("Reloj del sistema", 1),
            1: ("Teclado", 2),
            3: ("COM 2 y COM4", 11),
            4: ("COM 1 y COM3", 12),
            5: ("Libre", 13),
            6: ("Controlador Floppy - Diskette", 14),
            7: ("Puerto Paralelo - Impresora", 15),
            8: ("Reloj (tics) en tiempo real CMOS", 3),
            9: ("Libre para tarjeta de red, sonido, puerto SCSI", 4),
            10: ("Libre (igual que el anterior)", 5),
            11: ("Libre (igual que el anterior)", 6),
            12: ("PS-mouse", 7),
            13: ("Co-procesador matemático", 8),
            14: ("Canal IDE primario", 9),
            15: ("Libre (otros adaptadores)", 10)
        }
        self.program_priority = float('inf')
        self.queue = []
        self.log = []

    def handle_interrupt(self, irq, duration):
        name, priority = self.interrupts.get(irq, ("Desconocido", float('inf')))
        self.log.append(f"Interrupción recibida: {name} (IRQ {irq}), duración: {duration}, prioridad: {priority}")
        if priority < self.program_priority:
            self.log.append(f"Interrupción aceptada: {name} (IRQ {irq})")
            if self.queue:
                remaining_time, queued_irq = self.queue.pop(0)
                self.log.append(f"Guardando tiempo restante: {remaining_time} para {self.interrupts[queued_irq][0]} (IRQ {queued_irq}) en la cola de procesos")
            self.program_priority = priority
            self.queue.append((duration, irq))
        else:
            self.log.append(f"Interrupción rechazada: {name} (IRQ {irq})")
            self.queue.append((duration, irq))

    def print_process_control(self):
        print("\nDiagrama de Control de Procesos")
        print("Tiempo | Programa | Dispositivo")
        time = 0
        for duration, irq in self.queue:
            for t in range(duration):
                print(f"{time} | Ejecutando | {self.interrupts[irq][0]} (IRQ {irq})")
                time += 1

    def print_process_queue(self):
        print("\nCola de Procesos")
        for remaining_time, irq in self.queue:
            print(f"{self.interrupts[irq][0]} (IRQ {irq}) - Tiempo restante: {remaining_time}")

    def print_interrupt_log(self):
        print("\nBitácora de Interrupciones")
        for entry in self.log:
            print(entry)

if __name__ == "__main__":
    handler = InterruptHandler()
    # Ejemplo de interrupciones
    handler.handle_interrupt(0, 5)
    handler.handle_interrupt(1, 3)
    handler.handle_interrupt(8, 4)
    handler.handle_interrupt(4, 2)

    handler.print_process_control()
    handler.print_process_queue()
    handler.print_interrupt_log()
