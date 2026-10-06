import os
import psutil
import time


def get_network_stats():


    net1 = psutil.net_io_counters()


    time.sleep(1)

    net2 = psutil.net_io_counters()

    download_bytes = net2.bytes_recv - net1.bytes_recv
    upload_bytes = net2.bytes_sent - net1.bytes_sent

    download_kbps = (download_bytes / 1024)
    upload_kbps = (upload_bytes / 1024)

    packets = net2.packets_recv + net2.packets_sent
    packets_old = net1.packets_recv + net1.packets_sent

    packets_per_sec = packets - packets_old

    connections = psutil.net_connections()

    active_connections = len(connections)

    tcp_connections = 0
    udp_connections = 0

    for conn in connections:

        if conn.type == 1:
            tcp_connections += 1

        elif conn.type == 2:
            udp_connections += 1

    interfaces = psutil.net_if_stats()

    active_interfaces = 0

    for name, stats in interfaces.items():

        if stats.isup:
            active_interfaces += 1

    return {
        "download": round(download_kbps, 2),
        "upload": round(upload_kbps, 2),
        "connections": active_connections,
        "tcp": tcp_connections,
        "udp": udp_connections,
        "interfaces": active_interfaces,
        "packets": packets_per_sec
    }

