from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem
import csv
import datetime

def export_to_csv(modelAdmin, request, queryset):
    opts = modelAdmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Exporter en CSV'


def order_detail(obj):
    url = reverse('order:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Detail</a>')

def order_pdf(obj):
    url = reverse('order:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model           = OrderItem
    raw_id_fields   = ['product']

@admin.display()
def total_da(obj):
    return ("%s" % obj.get_total_cost())


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name','last_name' ,'phone' ,'email' ,'created' ,'updated' ,total_da,'confirmer', 'paid', order_detail, order_pdf]
    list_display_links =('id', 'first_name', 'last_name')
    list_filter = ['paid','created' ,'updated']
    list_editable = ['confirmer','paid']
    inlines = [OrderItemInline] 
    actions = [export_to_csv]
    list_per_page = 30



