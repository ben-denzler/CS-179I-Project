import psutil
import csv
from time import time
from tqdm import tqdm

"""
This script tracks CPU and memory utilization as percentages over time.
The results are output as a CSV file to performance_data.csv.
"""

duration = 10   # Seconds to collect data for, in seconds
interval = 0.5  # How often to collect data, in seconds
filename = "./data/performance_data.csv"  # Results stored here

times = []
cpu_percentages = []
memory_percentages = []
start_time = time()

# Collect CPU and memory utilization every 0.5 second for "duration" seconds
print(f"Collecting data every {interval} seconds for {duration} seconds...\n")
for _ in tqdm(range(duration)):
    curr_time = time() - start_time
    times.append(round(curr_time, 3))
    cpu_percent = psutil.cpu_percent(interval=interval)
    cpu_percentages.append(cpu_percent)
    memory_percent = psutil.virtual_memory().percent
    memory_percentages.append(memory_percent)

# Write the data to a CSV file
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Time (s)", "CPU Utilization (%)", "Memory Utilization (%)"])
    for i in range(len(times)):
        writer.writerow([times[i], cpu_percentages[i], memory_percentages[i]])

print(f"\nData saved to {filename} successfully.")