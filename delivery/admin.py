from django.contrib import admin

from .models import Wilaya, Commune
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export import widgets

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





class CommuneResource(resources.ModelResource):
    # wilaya_id = fields.Field(column_name='wilaya_id',attribute='wilaya_id',widget=ForeignKeyWidget(Wilaya, 'mat')) 
    class Meta:
        model = Commune
        fields = ('wilaya_id','name')
        exclude = ('id',)
        # import_id_fields = ('id',)


@admin.register(Commune)
class CommuneAdmin(ImportExportModelAdmin):
    list_display = ('name','wilaya_id')
    resource_class = CommuneResource
    # list_display_links =('id', 'name')
    # search_fields = ('name',)
    # list_per_page = 40



