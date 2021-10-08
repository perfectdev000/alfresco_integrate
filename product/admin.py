from django.contrib import admin
from .models import Files_upload

# Register your models here.
class Files_uploadAdmin(admin.ModelAdmin):
    list_display = ('up_file', 'user', 'data_type')
    list_per_page = 20

admin.site.register(Files_upload, Files_uploadAdmin)
