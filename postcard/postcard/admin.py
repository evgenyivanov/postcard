from django.contrib import admin
from models import *

#class CapchaAdmin(admin.ModelAdmin):
#    list_display = ('ip',  'capcha')


admin.site.register(Body)
admin.site.register(Send)