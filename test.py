import csv
import time
import psutil
import GPUtil
import threading
import keyboard

exit_event = threading.Event()

def write_metric (name, value):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('metrics.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, name, value])

def monitor_cpu_percent():
    flag = True
    while flag:
        cpu_percent = psutil.cpu_percent()
        write_metric("CPU percent", cpu_percent)
        for i in range(60):
            if exit_event.is_set():
                flag = False
                break
            time.sleep(1)
    print(" monitor_cpu_percent end ", end = "\n")
def monitor_memory():
    flag = True
    while flag:
        ram_percent = psutil.virtual_memory().percent
        write_metric("RAM", ram_percent)
        for i in range(60):
            if exit_event.is_set():
                flag = False
                break
            time.sleep(1)
    print(" monitor_memory end ", end = "\n")

def monitor_gpu_temp():
    flag = True
    while flag:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_name = gpu.name
            gpu_temp = gpu.temperature
        write_metric("".join([gpu_name," percent"]), gpu_temp)
        for i in range(60):
            if exit_event.is_set():
                flag = False
                break
            time.sleep(1)
    print(" monitor_gpu_percent end ", end = "\n")

def monitor_gpu_memory():
    flag = True
    while flag:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_name = gpu.name
            gpu_memory_percent = gpu.memoryUtil * 100
        write_metric("".join([gpu_name," memory"]), gpu_memory_percent)
        for i in range(60):
            if exit_event.is_set():
                flag = False
                break
            time.sleep(1)
    print(" monitor_gpu_memory end ", end = "\n")

print("start, press the SPACE to terminate the program")
cpu_thread = threading.Thread(target=monitor_cpu_percent)
memory_thread = threading.Thread(target=monitor_memory)
gpu_temperature_thread = threading.Thread(target=monitor_gpu_temp)
gpu_memory_thread = threading.Thread(target=monitor_gpu_memory)

cpu_thread.start()
memory_thread.start()
gpu_temperature_thread.start()
gpu_memory_thread.start()

keyboard.add_hotkey('space', lambda: exit_event.set())

cpu_thread.join()
memory_thread.join()
gpu_temperature_thread.join()
gpu_memory_thread.join()
