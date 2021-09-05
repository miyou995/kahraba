from django.contrib import admin

from .models import Wilaya, Commune


from import_export.admin import ImportExportModelAdmin
# from import_export.widgets import ForeignKeyWidget
# from import_export import resources, fields

# Register your models here.
@admin.register(Wilaya)
class WilayaAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name','price' ,'active']
    list_display_links =('id', 'name')
    list_filter = ['active']
    list_editable = ['price']
    list_per_page = 30


@admin.register(Commune)
class CommuneAdmin(ImportExportModelAdmin):
    # resource_class = CommuneResource  
    pass