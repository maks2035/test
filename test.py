import csv
import time
import psutil
import GPUtil

def monitor_system():
    i = 0
    a = 1
    while i < a:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent

        gpus = GPUtil.getGPUs()

        for gpu in gpus:
            gpu_name = gpu.name
            gpu_temp = gpu.temperature
            gpu_memory_percent = gpu.memoryUtil * 100

        with open('metrics.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows([(current_time, "CPU temp", cpu_percent)])
            writer.writerows([(current_time, "RAM", ram_percent)])
            writer.writerows([(current_time, "".join([gpu_name," temp"]), gpu_temp)])
            writer.writerows([(current_time, "".join([gpu_name," memory"]), gpu_memory_percent)])

        i += 1

        if(i < a):
            time.sleep(60)


if __name__ == "__main__":
    monitor_system()
