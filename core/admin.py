from django.contrib import admin
from .models import ProductType, Product, Category, ContactForm, PhotoProduct , Atributes, AtributesValue, ProductDetail, ProductDocument, Brand
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from django_mptt_admin.admin import DjangoMpttAdmin
admin.autodiscover()
admin.site.enable_nav_sidebar = False
admin.site.unregister(Group)


 
# class AtributesInline(admin.TabularInline):
#     model = Atributes

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

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',  'actif')
    list_display_links = ('id','name' )
    list_per_page = 40
    list_editable = [ 'actif']
    search_fields = ('name',)


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ('id', 'name',  'actif')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id','name' )
    list_per_page = 40
    list_editable = [ 'actif']
    search_fields = ('name',)
    exlude = ['slug']
    


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'old_price',  'price', 'new', 'top', 'actif', 'status')
    prepopulated_fields = {"slug": ("name",)}
    list_display_links = ('id','name' )
    list_per_page = 40
    list_filter = ('brand', 'category','new')
    list_editable = ['category', 'price', 'new', 'top', 'actif', 'old_price', 'status']
    search_fields = ('name',)
    exlude = ['slug']
    inlines = [ProductDetailInline, ProductDocumentInline, PhotosLinesAdmin]# a comenter pour KAHRABACENTER.com
    save_as= True
    

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
        return format_html('<img src="{}" height="150"  />'.format(self.big_slide.url))
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


