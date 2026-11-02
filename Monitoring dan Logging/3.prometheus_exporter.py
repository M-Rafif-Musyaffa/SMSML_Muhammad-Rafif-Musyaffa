from prometheus_client import start_http_server, Gauge
import psutil
import time

# 5 Metrik Sistem
cpu_usage = Gauge('sys_cpu_percent', 'Penggunaan CPU')
mem_usage = Gauge('sys_memory_percent', 'Penggunaan RAM')
disk_usage = Gauge('sys_disk_percent', 'Penggunaan Disk')
net_sent = Gauge('sys_network_sent_bytes', 'Byte Jaringan Terkirim')
net_recv = Gauge('sys_network_recv_bytes', 'Byte Jaringan Diterima')

def collect_metrics():
    while True:
        cpu_usage.set(psutil.cpu_percent(interval=1))
        mem_usage.set(psutil.virtual_memory().percent)
        disk_usage.set(psutil.disk_usage('/').percent)
        net_io = psutil.net_io_counters()
        net_sent.set(net_io.bytes_sent)
        net_recv.set(net_io.bytes_recv)
        time.sleep(2)

if __name__ == '__main__':
    print("Memulai Prometheus Exporter (Sistem) di port 8000...")
    start_http_server(8000)
    collect_metrics()