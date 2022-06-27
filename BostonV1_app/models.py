from django.db import models
import datetime

# Create your models here.
class Server_Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    Time = models.DateTimeField (default = datetime.datetime.now, blank = True)
    System = models.CharField(max_length=25)
    Hostname = models.CharField(max_length=50)
    Host_IP = models.CharField(max_length=50)
    Processor = models.CharField(max_length=100)
    Machine = models.CharField(max_length=25)
    Version = models.CharField(max_length=100)

class CPU_Data(models.Model):
    Physical_cores = models.IntegerField()
    Total_cores = models.IntegerField()
    Total_CPU_Usage = models.IntegerField()
    Turbo_Min = models.IntegerField()
    Turbo_Max = models.IntegerField()
    Turbo_Current = models.IntegerField()

class RAM_Data(models.Model):
    Total_RAM = models.CharField(max_length=20)
    Available_RAM = models.CharField(max_length = 20)
    Used_RAM = models.CharField(max_length = 20)
    Used_Percentage = models.IntegerField()

class Disk_Data(models.Model):
    Total_Partitions = models.IntegerField()
    Total_Available = models.CharField(max_length=20)
    Total_Usage = models.CharField(max_length = 20)
    Total_Free = models.CharField(max_length=20)
