import csv
from kubernetes import client, config
from time import time, sleep

"""
This script tracks the number of active pods for our service over time.
A CSV file is output when you force quit the app with Ctrl + C.
The results are output as pod_data.csv.
"""

kube_namespace = "default"
kube_service_name = "cs179i-project"
filename = "./data/pod_data.csv"  # Results stored here
interval = 0.5  # Seconds to wait between pod count queries

times = []
num_pods = []
start_time = time()

def output_csv(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Num Pods"])
        for i in range(len(times)):
            writer.writerow([times[i], num_pods[i]])

try:
    print("Collecting data... Use Ctrl + C to stop.")
    config.load_kube_config()
    kube_client = client.CoreV1Api()
    while True:
        # Count number of running pods for our service
        pods = kube_client.list_namespaced_pod(kube_namespace, label_selector=f"serving.knative.dev/service={kube_service_name}")
        active_pod_count = len([pod for pod in pods.items if pod.status.phase == "Running"])
        curr_time = time() - start_time
        times.append(round(curr_time, 3))
        num_pods.append(active_pod_count)
        sleep(interval)
except KeyboardInterrupt:
    output_csv(filename)
    print(f"\nData saved to {filename} successfully.")
    exit(1)
except Exception as e:
    print(f"An error occurred: {e}")