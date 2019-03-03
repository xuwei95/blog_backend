import psutil
import os
import time
import re
from blog.settings import log_path

def getCPUstate(interval=1):
    return psutil.cpu_percent(interval)


def getMemorystate():
    phymem = psutil.virtual_memory()
    precent = phymem.percent
    return precent


def disk_stat():
    disk = os.statvfs('/usr')
    percent = (disk.f_blocks - disk.f_bfree) * 100 / (disk.f_blocks - disk.f_bfree + disk.f_bavail) + 1
    return '%.1f' % percent


def network():
    network_sent = int(psutil.net_io_counters()[0]/1024)
    network_recv = int(psutil.net_io_counters()[1]/1024)
    time.sleep(1)
    network_sent2 = int(psutil.net_io_counters()[0]/1024)
    network_recv2 = int(psutil.net_io_counters()[1]/1024)
    sent = network_sent2 - network_sent
    recv = network_recv2 - network_recv
    return sent, recv


def count_user():
    f = open('%s/all.log' % log_path)
    text = f.read()
    ip_list = re.findall('ip:(.*?)]\n', text)
    return len(set(ip_list))


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""

    return {
        'code': 20000,
        'data': {'token': token}
    }

count_user()
