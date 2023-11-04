import csv
import time
import psutil
import GPUtil
import threading

def write_metric (name, value):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    with open('metrics.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time, name, value])

def monitor_cpu_temp():
    while True:
        cpu_percent = psutil.cpu_percent()
        write_metric("CPU percent", cpu_percent)
        time.sleep(60)

def monitor_memory():
    while True:
        ram_percent = psutil.virtual_memory().percent
        write_metric("RAM", ram_percent)
        time.sleep(60)

def monitor_gpu_temp():
    while True:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_name = gpu.name
            gpu_temp = gpu.temperature
        write_metric("".join([gpu_name," temp"]), gpu_temp)
        time.sleep(60)

def monitor_gpu_memory():
    while True:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_name = gpu.name
            gpu_memory_percent = gpu.memoryUtil * 100
        write_metric("".join([gpu_name," memory"]), gpu_memory_percent)
        time.sleep(60)

cpu_thread = threading.Thread(target=monitor_cpu_temp)
memory_thread = threading.Thread(target=monitor_memory)
gpu_temperature_thread = threading.Thread(target=monitor_gpu_temp)
gpu_memory_thread = threading.Thread(target=monitor_gpu_memory)

cpu_thread.start()
memory_thread.start()
gpu_temperature_thread.start()
gpu_memory_thread.start()

try:
    cpu_thread.join()
    memory_thread.join()
    gpu_temperature_thread.join()
    gpu_memory_thread.join()
except KeyboardInterrupt:
    pass

