from django.db import models
from tinymce import models as tinymce_models
from django.utils.html import format_html

from django.core.exceptions import ValidationError
# Create your models here.
from django.db.models.signals import pre_init
class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)

class Business(models.Model):
    name        = models.CharField(verbose_name="Nom de l'entreprise", max_length=100)
    logo        = models.ImageField(upload_to='images/logos', verbose_name='Logo')
    logo_negatif= models.ImageField(upload_to='images/slides', verbose_name="Logo négatif")
    title       = models.CharField(verbose_name="Titre", max_length=50, blank=True)
    adress      = models.CharField(verbose_name="Adresse", max_length=50, blank=True)
    email       = models.EmailField(verbose_name="email de l'entreprise", max_length=50, blank=True)
    phone       = models.CharField(verbose_name="numéro de téléphone de l'entreprise", max_length=50, blank=True)
    about       = tinymce_models.HTMLField(verbose_name='Text a propos', blank=True, null=True)
    about_photo = models.ImageField(verbose_name="Photo A propos 440 X 275 px", upload_to='slides/', blank=True, null=True)
    facebook    = models.URLField(verbose_name="Lien page Facebook", max_length=300, blank=True, null=True)
    insta       = models.URLField(verbose_name="Lien page Instagram", max_length=300, blank=True, null=True)
    twitter     = models.URLField(verbose_name="Lien Compte Twitter", max_length=300, blank=True, null=True)
    google_plus = models.URLField(verbose_name="Lien Compte Google plus", max_length=300, blank=True, null=True)
    youtube     = models.URLField(verbose_name="Lien Chaine Youtube", max_length=300, blank=True, null=True)
    chat_code   = models.TextField(verbose_name="Script messagerie instantané", blank=True, null=True)
    pixel       = models.TextField(verbose_name="Script Facebook pixel", blank=True, null=True)
    analytics   = models.TextField(verbose_name="Script Analytics", blank=True, null=True)
    # actif  = models.BooleanField(verbose_name='Active', default=False)
    # is_big  = models.BooleanField(verbose_name='Grande photo (1920 x 570)', default=False)
    # is_small  = models.BooleanField(verbose_name='Medium photo (720 x 540)', default=False)

    def image_tag(self):
        return format_html('<img src="{}" height="150"  />'.format(self.logo.url))
    image_tag.allow_tags = True
    class Meta:
        verbose_name = '1. Infomation'
        verbose_name_plural = '1. Infomations'

    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and
                self.id != model.objects.get().id):
            raise ValidationError("Vous ne pouvez pas rajouter d'entreprise")

class Slide(models.Model):
    photo      = models.ImageField(verbose_name="Slide 870 X 475 px", upload_to='slides/', )
    title      = models.CharField(verbose_name="Grand titre de la photo", max_length=50, blank=True, null=True) 
    sub_title  = models.CharField(verbose_name="Sous titre de la photo", max_length=50, blank=True, null=True) 
    url        = models.URLField(verbose_name="Lien", max_length=250)
    actif  = models.BooleanField(verbose_name='actif', default=True)
    objects = ActiveManager()

    class Meta:
        verbose_name = '2. Slides haut page d\'accueil'
        verbose_name_plural = '2. Slides haut page d\'accueil'

    def clean(self):
        model = self.__class__
        if (model.objects.count() > 5 and
                self.id != model.objects.get().id):
            raise ValidationError("Vous ne pouvez pas rajouter d'autres Slides")


class ThreePhotos(models.Model):
    photo = models.ImageField(verbose_name="photo 370 X 225 px", upload_to='slides/', )
    url   = models.URLField(verbose_name="lien", max_length=200)
    objects = ActiveManager()

    class Meta:
        verbose_name = '3. Trois Photos Acceuil'
        verbose_name_plural = '3. Trois Photos Acceuil'

    def clean(self):
        model = self.__class__
        if model.objects.count() > 3:
            raise ValidationError("Vous ne pouvez pas rajouter d'autres photos ( la limites des photos dans ce contexte est 3)")
        super(ThreePhotos, self).clean()

class DualBanner(models.Model):
    photo = models.ImageField(verbose_name="photo 570 X 200 px", upload_to='slides/', )
    url   = models.URLField(verbose_name="lien", max_length=200)
    actif  = models.BooleanField(verbose_name='actif', default=True)
    objects = ActiveManager()

    class Meta:
        verbose_name = '3. Petits Banners en duo'
        verbose_name_plural = '3. Petits Banners en duo'

    def clean(self):
        model = self.__class__
        if model.objects.count() > 2:
            raise ValidationError("Vous ne pouvez pas rajouter d'autres photos ( la limites des photos dans ce contexte est 2)")


class LargeBanner(models.Model):
    photo      = models.ImageField(verbose_name="Slide 1170 X 400 px", upload_to='slides/', )
    title      = models.CharField(verbose_name="Grand titre de la photo", max_length=50, blank=True, null=True) 
    sub_title  = models.CharField(verbose_name="Sous titre de la photo", max_length=50, blank=True, null=True) 
    url        = models.URLField(verbose_name="Lien", max_length=250)
    class Meta:
        verbose_name = '3. Grand Banner bas de page d\'accueil'
        verbose_name_plural = '3. Grand Banner bas de d\'accueil'

    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError("Vous ne pouvez pas rajouter d'autres Grand Banners")
        super(LargeBanner, self).clean()

class Counter(models.Model):
    name    = models.CharField(verbose_name="nom de l'acomplissement", max_length=150) 
    before  = models.CharField(verbose_name="avant le chiffre", max_length=50, blank=True, null=True) 
    number  = models.IntegerField(verbose_name="chiffre") 
    icon    = models.ImageField(verbose_name="icon", upload_to='icons/', )
    actif  = models.BooleanField(verbose_name='actif', default=True)
    objects = ActiveManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '5. Accomplissement'
        verbose_name_plural = '5. Accomplissement'

    def clean(self):
        model = self.__class__
        if model.objects.count() > 4:
            raise ValidationError("Vous ne pouvez pas rajouter plus de quatre Accomplissement")



class Realisation(models.Model):
    title    = models.CharField(verbose_name="nom de l'acomplissement", max_length=150) 
    description     = tinymce_models.HTMLField(verbose_name='Déscription du produit', blank=True, null=True)

    actif  = models.BooleanField(verbose_name='actif', default=True)
    created = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)
    objects = ActiveManager()

    def __str__(self):
        return self.title

class RealisationPhotos(models.Model):
    realisation = models.ForeignKey(Realisation, verbose_name="Projet / Réalisation", on_delete=models.CASCADE)
    image    = models.ImageField(verbose_name="icon", upload_to='icons/')
    actif  = models.BooleanField(verbose_name='actif', default=True)

class Partner(models.Model):
    logo    = models.ImageField(verbose_name="icon", upload_to='icons/', )
    siteweb = models.URLField(verbose_name="Lien", max_length=250)
    actif  = models.BooleanField(verbose_name='actif', default=True)
    

# def create_counter_signal(sender, **kwargs):
#     if Counter.objects.count() > 3:
#         print('ouiii je suis init')
#         # raise ValidationError("Vous ne pouvez pas rajouter plus de quatre Accomplissement")
    
# pre_init.connect(create_counter_signal, sender=Counter)
