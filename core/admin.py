from django.contrib import admin
from .models import ProductType, Product, Category, ContactForm, PhotoProduct , Atribute, AtributesValue, ProductDetail, ProductDocument, Brand, Gamme
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django_mptt_admin.admin import DjangoMpttAdmin
admin.autodiscover()
admin.site.enable_nav_sidebar = False
admin.site.unregister(Group)
from django.db.models import Count
from django.db import models
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget
from django.contrib.admin import SimpleListFilter

from compressor.filters import CompilerFilter
class PostCSSFilter(CompilerFilter):
    command = 'postcss'





class AtributesInline(admin.TabularInline):
    model = Atribute

class GammesInline(admin.TabularInline):
    model = Gamme

class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument

class AtributesValueInline(admin.TabularInline):
    model = AtributesValue

class ProductDetailInline(admin.TabularInline):
    model = ProductDetail

class PhotosLinesAdmin(admin.TabularInline):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.fichier.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    model = PhotoProduct
    readonly_fields= (image_tag,)
    extra = 1
    # readonly_fields = ('photo',)

# a comenter pour KAHRABACENTER.com
# class ProductTypeAdmin(admin.ModelAdmin):
#     inlines = [AtributesInline]

# class ProductTypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',  'is_active')
#     list_display_links = ('id','name' )
#     list_per_page = 40
#     list_editable = [ 'is_active']
#     search_fields = ('name',)
#     inlines = [AtributesInline]


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',  'actif')
    list_display_links = ('id','name' )
    list_per_page = 40
    list_editable = [ 'actif']
    search_fields = ('name',)
    inlines = [GammesInline]


class CategoryAdmin(DjangoMpttAdmin):
    # def get_queryset(self, request):
    #     qs = super(CategoryAdmin, self).get_queryset(request)
    #     qs = qs.annotate(total_products=Product.objects.all(category__in=models.get_descendants(include_self=True)).count())
    #     return qs
    def count_products(self):
        return Product.objects.filter(category__in=self.get_descendants(include_self=True)).count()
    list_display = ('id', 'name', count_products, 'actif')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id','name' )
    list_per_page = 50
    list_editable = [ 'actif']
    search_fields = ('name',)
    exlude = ['slug']


class HasImages(SimpleListFilter):
    title = "Photos" 
    parameter_name ="pic"
        # return Product.objects.filter(photos=True)
    def lookups(self, request, model_admin):
        return (
            ('true', 'Avec Photos'),
            ('false', 'Sans Photos')
        )
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'true':
            return Product.objects.filter(photos__isnull=False)
        elif self.value().lower() == 'false':
            return Product.objects.filter(photos__isnull=True)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        # exclude = ('confirmer', )
        # widget = ManyToManyWidget(Country, field='name')
        fields = ('id', 'name', 'price', 'reference','category','text','old_price','gamme','specifications')
        export_product = ('id', 'name', 'price', 'reference','category','text','old_price','gamme','specifications')


class ProductAdmin(ExportMixin, admin.ModelAdmin):

    list_display = ('id', 'name', 'category', 'old_price',  'price', 'new', 'top', 'actif', 'stock','status')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id','name' )
    list_per_page = 40
    list_filter = ('gamme',HasImages ,'new')
    list_editable = ['category', 'price', 'new', 'top', 'actif', 'old_price', 'stock','status']
    search_fields = ('name','reference')
    exlude = ['slug']
    inlines = [ProductDetailInline, ProductDocumentInline, PhotosLinesAdmin]# a comenter pour KAHRABACENTER.com
    save_as= True
    resource_class = ProductResource
    

# Contact
# class GammeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     list_display_links = ('id','name')
#     list_per_page = 40
#     search_fields = ('id', 'name')

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)
    list_per_page = 40
    list_filter = ('name', 'phone', 'email',)
    search_fields = ('id', 'phone', 'email')


class PhotosAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150"/>'.format(self.big_slide.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    list_display = ('id', image_tag, 'actif', 'is_big', 'is_small', 'big_slide')
    list_editable = ['actif', 'is_big', 'is_small', 'big_slide']
    list_display_links = ('id',image_tag)
    list_per_page = 40


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ContactForm, ContactFormAdmin)
# admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Brand, BrandAdmin)


