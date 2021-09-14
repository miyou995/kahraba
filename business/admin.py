from django.contrib import admin
from .models import Business, Slide, ThreePhotos, Counter, LargeBanner ,DualBanner, Realisation, Partner, RealisationPhotos, ClientService
from django.utils.html import format_html

# Register your models here.
@admin.register(LargeBanner)
class LargeBannerAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.photo.url))
    list_display = ('id', 'title', 'sub_title', 'url', 'photo',image_tag)
    list_display_links = ('id',)
    list_editable = ['title', 'sub_title','photo', 'url']

    
    # def has_add_permission(self, request):
    #     return False

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.photo.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    list_display = ('id', 'photo', image_tag,'title', 'sub_title', 'url')
    list_display_links = ('id', )
    list_editable = ['title', 'photo', 'sub_title', 'url']
    
    # def has_add_permission(self, request):
    #     return False
@admin.register(ThreePhotos)
class ThreePhotosAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.photo.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    list_display = ('id', image_tag, 'url')
    list_display_links = ('id', image_tag)
    list_editable = ['url']
    

@admin.register(DualBanner)
class DualBannerAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.photo.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    list_display = ('id', image_tag, 'url')
    list_display_links = ('id', image_tag)
    list_editable = ['url']
    # def has_add_permission(self, request):
    #     return False

@admin.register(Business)
class BusinesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    def has_add_permission(self, request):
        return False


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    list_display = ('name','number')
    list_editable = ['number']

@admin.register(ClientService)
class ClientServiceAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150" />'.format(self.icon.url))
    list_display = ('name','sub_title', image_tag)
    list_display_links = ('name',)
    list_editable = ['sub_title']



class PhotosLinesAdmin(admin.TabularInline):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.image.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    model = RealisationPhotos
    readonly_fields= (image_tag,)
    extra = 1
    # readonly_fields = ('photo',)


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ('title','actif')
    list_editable = ['actif']
    inlines = [PhotosLinesAdmin]# a comenter pour KAHRABACENTER.com

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.logo.url))
    list_display = ('id','siteweb', image_tag, 'actif')
    list_editable = ['siteweb', 'actif']
    