import heapq
import pandas as pd

# Definimos las prioridades de interrupciones por dispositivo
interruptions = {
    0: {'prioridad': 1, 'funcion': 'Reloj del sistema'},
    1: {'prioridad': 2, 'funcion': 'Teclado'},
    2: {'prioridad': 0, 'funcion': 'Reservada al controlador PIC'},
    3: {'prioridad': 11, 'funcion': 'COM 2 y COM4'},
    4: {'prioridad': 12, 'funcion': 'COM 1 y COM3'},
    5: {'prioridad': 13, 'funcion': 'Libre'},
    6: {'prioridad': 14, 'funcion': 'Controlador Floppy - Diskette'},
    7: {'prioridad': 15, 'funcion': 'Puerto Paralelo - Impresora'},
    8: {'prioridad': 3, 'funcion': 'Reloj (tics) en tiempo real CMOS'},
    9: {'prioridad': 4, 'funcion': 'Libre para tarjeta de red, sonido, puerto SCSI'},
    10: {'prioridad': 5, 'funcion': 'Libre (igual que el anterior)'},
    11: {'prioridad': 6, 'funcion': 'Libre (igual que el anterior)'},
    12: {'prioridad': 7, 'funcion': 'PS-mouse'},
    13: {'prioridad': 8, 'funcion': 'Co-procesador matemático'},
    14: {'prioridad': 9, 'funcion': 'Canal IDE primario'},
    15: {'prioridad': 10, 'funcion': 'Libre (otros adaptadores)'}
}

# Simulamos el manejo de interrupciones
class InterruptHandler:
    def __init__(self, interruptions):
        self.interruptions = interruptions
        self.queue = []
        self.current_time = 0
        self.history = []

    def add_interrupt(self, irq, duration):
        priority = self.interruptions[irq]['prioridad']
        heapq.heappush(self.queue, (priority, self.current_time, irq, duration))

    def process_interrupts(self):
        while self.queue:
            priority, start_time, irq, duration = heapq.heappop(self.queue)
            end_time = self.current_time + duration
            self.history.append({
                'irq': irq,
                'start_time': self.current_time,
                'end_time': end_time,
                'duration': duration,
                'priority': priority
            })
            self.current_time = end_time

    def display_history(self):
        for entry in self.history:
            print(f"IRQ: {entry['irq']} - Start: {entry['start_time']} - End: {entry['end_time']} - Duration: {entry['duration']} - Priority: {entry['priority']}")

handler = InterruptHandler(interruptions)

# Agregamos interrupciones simuladas
handler.add_interrupt(1, 5)  # Teclado
handler.add_interrupt(0, 3)  # Reloj del sistema
handler.add_interrupt(8, 2)  # Reloj CMOS

handler.process_interrupts()
handler.display_history()

# Generación del diagrama de control de procesos
def generate_process_control_diagram(history):
    data = {
        'Time': [],
        'Program': [],
        'Devices': []
    }
    
    for entry in history:
        data['Time'].append(entry['start_time'])
        data['Program'].append('Interrupción' if entry['priority'] > 1 else 'Proceso principal')
        data['Devices'].append(f"IRQ {entry['irq']} - {interruptions[entry['irq']]['funcion']}")
    
    df = pd.DataFrame(data)
    return df

control_diagram = generate_process_control_diagram(handler.history)
print(control_diagram)

# Generación de un diagrama de cola de procesos
def generate_queue_diagram(history):
    queue_data = {
        'IRQ': [],
        'Remaining Time': []
    }
    
    for entry in history:
        if entry['priority'] > 1:  # Si fue interrumpido por otro de mayor prioridad
            queue_data['IRQ'].append(entry['irq'])
            queue_data['Remaining Time'].append(entry['duration'])
    
    queue_df = pd.DataFrame(queue_data)
    return queue_df

queue_diagram = generate_queue_diagram(handler.history)
print(queue_diagram)

# Generación del diagrama de bitácora de interrupciones
def generate_interrupt_log(handler, monitor_time):
    log_data = {
        'Device Area': [],
        'Interruption Accepted': [],
        'Time Range': [],
        'Remaining Time to Complete': []
    }

    for entry in handler.history:
        if entry['start_time'] <= monitor_time <= entry['end_time']:
            log_data['Device Area'].append(f"IRQ {entry['irq']} - {interruptions[entry['irq']]['funcion']}")
            log_data['Interruption Accepted'].append("SI")
            log_data['Time Range'].append(f"{entry['start_time']} - {entry['end_time']}")
            remaining_time = entry['end_time'] - monitor_time
            log_data['Remaining Time to Complete'].append(remaining_time if remaining_time > 0 else 0)
        else:
            log_data['Device Area'].append(f"IRQ {entry['irq']} - {interruptions[entry['irq']]['funcion']}")
            log_data['Interruption Accepted'].append("NO")
            log_data['Time Range'].append(f"{entry['start_time']} - {entry['end_time']}")
            log_data['Remaining Time to Complete'].append(0)
    
    log_df = pd.DataFrame(log_data)
    return log_df

interrupt_log = generate_interrupt_log(handler, 4)
print(interrupt_log)
