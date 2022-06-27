from django.shortcuts import render,redirect
from getsize import get_size
from getsize1 import get_size1
from check_internet import have_internet
import psutil
from sys import platform
from datetime import datetime
import GPUtil
import subprocess
from django.http import HttpResponse
#from get_size1 import get_size1
import time
import math
import os
import socket
import cpuinfo
import uuid
import re
from BostonV1_app.models import Server_Data,CPU_Data,RAM_Data,Disk_Data

# Create your views here.
def index(request):
    #System Details
    import platform
    uname = platform.uname()
    system = uname.system
    Node_Name =  uname.node
    Release = uname.release
    Version = uname.version
    Machine = uname.machine
    Processor = cpuinfo.get_cpu_info()['brand_raw']
    # Host Name and ip
    hname = socket.gethostname()
    hip = socket.gethostbyname(hname)
    Server_data = Server_Data(System = system,Hostname = Node_Name,Host_IP=hip,Processor=Processor,Machine =Machine,Version=Version)
    Server_data.save()

    #CPU information
    Total_cores = os.cpu_count()
    Physical_cores = psutil.cpu_count(logical=False)
    ## CPU frequencies
    cpufreq = psutil.cpu_freq()
    Max_Frequency = cpufreq.max
    Min_Frequency = cpufreq.min
    Current_Frequency = round(cpufreq.current)
    ## CPU usage
    cpu_usage = psutil.cpu_percent(percpu=True, interval=1)
    Total_CPU_Usage = psutil.cpu_percent()

    CPU_data = CPU_Data(Physical_cores = Physical_cores,Total_cores = Total_cores,Total_CPU_Usage = Total_CPU_Usage,Turbo_Min = Min_Frequency,Turbo_Max = Max_Frequency,Turbo_Current = Current_Frequency)
    CPU_data.save()

    # RAM Usage
    svmem = psutil.virtual_memory()
    Total = get_size(svmem.total)
    Available = get_size(svmem.available)
    Used = get_size(svmem.used)
    Percentage = svmem.percent
    Free = get_size(svmem.free)
    RAM_data = RAM_Data(Total_RAM = Total,Available_RAM = Available,Used_RAM=Used,Used_Percentage = Percentage)
    RAM_data.save()

    s = psutil.disk_partitions()
    # Find a disk
    disk = []
    for i in range(0,len(s)):
        disk.append(s[i][0])
    disk_count = len(disk)

    #Network and LAN
    LAN = have_internet()

    #Disk 2
    total = int()
    used  = int()
    free  = int()

    for disk in psutil.disk_partitions():
        if disk.fstype:
            total += int(psutil.disk_usage(disk.mountpoint).total)
            used  += int(psutil.disk_usage(disk.mountpoint).used)
            free  += int(psutil.disk_usage(disk.mountpoint).free)
    Total_disk_space = get_size(total)
    USED_DISK_SPACE = get_size(used)
    FREE_DISK_SPACE = get_size(free)
    Disk_data =Disk_Data(Total_Partitions = disk_count,Total_Available = Total_disk_space,Total_Usage = USED_DISK_SPACE,Total_Free = FREE_DISK_SPACE)
    Disk_data.save()




    sys_info_dict = {'system':system,'Node_Name':Node_Name,'Release':Release,
    'Version':Version,'Machine':Machine,'Processor':Processor,'Total_cores':Total_cores,'Physical_cores':Physical_cores,'Max_Frequency':Max_Frequency,
    'Min_Frequency':Min_Frequency,'Current_Frequency':Current_Frequency,'Total_CPU_Usage':Total_CPU_Usage,'Total':Total,'Available':Available,'Used':Used,
    'Percentage':Percentage,'Free':Free,'disk':disk,'hname':hname,'hip':hip,
        'disk_count':disk_count,
        'LAN':LAN,
        'Total_disk_space': Total_disk_space,
        'USED_DISK_SPACE': USED_DISK_SPACE,
        'FREE_DISK_SPACE': FREE_DISK_SPACE}

    return render(request,'BostonV1_app/test.html',context = sys_info_dict)

def server_details(request):
    #System Details
    import platform
    uname = platform.uname()
    system = uname.system
    Node_Name =  uname.node
    Release = uname.release
    Version = uname.version
    Machine = uname.machine
    Processor = cpuinfo.get_cpu_info()['brand_raw']
    MAC_Address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    # Reboot server_details
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)

    #CPU information
    Total_cores = psutil.cpu_count(logical=True)
    Physical_cores = psutil.cpu_count(logical=False)
    ## CPU frequencies
    cpufreq = psutil.cpu_freq()
    Max_Frequency = cpufreq.max
    Min_Frequency = cpufreq.min
    Current_Frequency = cpufreq.current
    ## CPU usage
    cpu_usage = psutil.cpu_percent(percpu=True, interval=1)
    Total_CPU_Usage = psutil.cpu_percent
    stat = psutil.cpu_stats()
    ctx = get_size(stat.ctx_switches)
    interrupts = get_size(stat.interrupts)
    syscalls = get_size(stat.syscalls)

    server_info_dict = {'system':system,'Node_Name':Node_Name,'Release':Release,
    'Version':Version,'Machine':Machine,'Processor':Processor,'bt':bt,'Total_cores':Total_cores,'Physical_cores':Physical_cores,'Max_Frequency':Max_Frequency,
    'Min_Frequency':Min_Frequency,'Current_Frequency':Current_Frequency,'cpu_usage':cpu_usage,'Total_CPU_Usage':Total_CPU_Usage,
    'ctx':ctx,'syscalls':syscalls,'interrupts':interrupts,'MAC_Address':MAC_Address}
    return render(request,'BostonV1_app/server_details.html',server_info_dict)

def cpu_details(request):
    ## CPU usage
    cpu_usage = psutil.cpu_percent(percpu=True, interval=1)
    Total_CPU_Usage = psutil.cpu_percent

    cpu_details_dict = {
    'cpu_usage':cpu_usage,
    'Total_CPU_Usage':Total_CPU_Usage
    }

    return render(request,'BostonV1_app/cpu_details.html',cpu_details_dict)

def ram_details(request):
    svmem = psutil.virtual_memory()
    Total = get_size(svmem.total)
    Available = get_size(svmem.available)
    Used = get_size(svmem.used)
    Percentage = svmem.percent
    Free = get_size(svmem.free)

    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    Total_swap =  get_size(swap.total)
    Free_swap = get_size(swap.free)
    Used_swap = get_size(swap.used)
    Percentage_swap = swap.percent
    mem_dict = {'Total':Total,'Available':Available,'Used':Used,'Percentage':Percentage,'Free':Free,'Total_swap':Total_swap,'Free_swap': Free_swap,
    'Used_swap':Used_swap,'Percentage_swap':Percentage_swap}

    return render(request,'BostonV1_app/ram_details.html',context = mem_dict)

def disk_details(request):
    s = psutil.disk_partitions()
    # Find a disk
    disk = []
    for i in range(0,len(s)):
        disk.append(s[i][0])
    #find a disk total storage
    disk_total_storage = []
    for i in range(0,len(disk)):
        disk_total_storage.append(get_size(psutil.disk_usage(disk[i][:2])[0]))
        #disk_total = sum(disk_free_storage)
    #Find the disk Free storage
    disk_free_storage = []
    for i in range(0,len(disk)):
        disk_free_storage.append(get_size(psutil.disk_usage(disk[i][:2])[1]))
    #Find the disk Used storage
    disk_used_storage = []
    for i in range(0,len(disk)):
        disk_used_storage.append(get_size(psutil.disk_usage(disk[i][:2])[2]))
    #Find the disk Used Percentage storage
    disk_storage_percent = []
    for i in range(0,len(disk)):
        disk_storage_percent.append(psutil.disk_usage(disk[i][:2])[3])

    disk_details_dict = {
    'disk':disk,
    'disk_total_storage':disk_total_storage,
    'disk_free_storage':disk_free_storage,
    'disk_used_storage':disk_used_storage,
    'disk_storage_percent':disk_storage_percent
    }
    return render(request,'BostonV1_app/disk_details.html',disk_details_dict)

def network_details(request):
    hname = socket.gethostname()
    hip = socket.gethostbyname(hname)
    LAN = have_internet()
    network_dict = {'hname':hname,'hip':hip,'LAN':LAN}
    return render(request,'BostonV1_app/network_details.html',network_dict)
