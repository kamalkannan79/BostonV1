from django.contrib import admin

# Register your models here.
from BostonV1_app.models import Server_Data,CPU_Data,RAM_Data,Disk_Data

admin.site.register(Server_Data)
admin.site.register(CPU_Data)
admin.site.register(RAM_Data)
admin.site.register(Disk_Data)
