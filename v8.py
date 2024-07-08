import heapq
import pandas as pd

class Device:
    def __init__(self, name, irq, priority, duration):
        self.name = name
        self.irq = irq
        self.priority = priority
        self.duration = duration
        self.remaining_time = duration

class Process:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority
        self.queue = []
        self.history = []
        self.process_queue = []

    def add_device(self, device, time):
        heapq.heappush(self.queue, (device.priority, time, device))

    def run(self, duration):
        for t in range(duration):
            self.history.append(self.name)
            if self.queue:
                priority, start_time, device = self.queue[0]
                if t >= start_time:
                    heapq.heappop(self.queue)
                    self.handle_device(device, t)

    def handle_device(self, device, start_time):
        for t in range(device.duration):
            self.history.append(device.name)
        remaining_time = device.duration - (len(self.history) - start_time)
        if remaining_time > 0:
            device.remaining_time = remaining_time
            heapq.heappush(self.queue, (device.priority, start_time + device.duration, device))
        self.process_queue.append({
            "Device": device.name,
            "IRQ": device.irq,
            "Duration": device.duration,
            "Remaining Time": remaining_time
        })

# Define devices
devices = [
    Device("Reloj del sistema", 0, 1, 5),
    Device("Teclado", 1, 2, 4),
    Device("Reloj CMOS", 8, 3, 3),
    Device("Tarjeta de red", 9, 4, 6),
    Device("COM2 y COM4", 3, 11, 2),
    Device("COM1 y COM3", 4, 12, 2),
    Device("Floppy Disk", 6, 14, 7),
    Device("Puerto Paralelo", 7, 15, 3),
    # Add more devices as needed
]

# Create an instance of the main process and add devices
main_process = Process("Programa", float('inf'))

# Add devices to the main process (example times)
main_process.add_device(devices[0], 1)
main_process.add_device(devices[1], 2)
main_process.add_device(devices[2], 4)
main_process.add_device(devices[3], 6)

# Execute the main process for a duration of time
main_process.run(20)

def generate_process_control_diagram(process):
    timeline = range(len(process.history))
    data = {"Time": timeline, "Action": process.history}
    df = pd.DataFrame(data)
    print("Diagrama de Control de Proceso:")
    print(df)
    print("\n")

def generate_process_queue(process):
    df = pd.DataFrame(process.process_queue)
    print("Cola de Procesos:")
    print(df)
    print("\n")

def generate_interrupt_log(process, query_time):
    log = []
    for t, action in enumerate(process.history):
        if t == query_time:
            log.append({
                "Time": t,
                "Device": action,
                "Affected": "YES" if action != "Programa" else "NO",
                "Time Range": f"{t} - {t + 1}",
                "Remaining Time": next((d.remaining_time for d in devices if d.name == action), 0)
            })
    df = pd.DataFrame(log)
    print("Bitácora de Interrupciones:")
    print(df)
    print("\n")

# Generate the process control diagram
generate_process_control_diagram(main_process)

# Generate the process queue
generate_process_queue(main_process)

# Request specific time for interrupt log
query_time = int(input("Ingrese el tiempo específico para la bitácora de interrupciones: "))
generate_interrupt_log(main_process, query_time)
