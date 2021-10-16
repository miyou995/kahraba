from django.db import models
from django.utils.text import slugify
# Create your models here.
from atributes.models import Tag
from django.urls import reverse
from tinymce import models as tinymce_models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.db.models import Q

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

STATUS_PRODUIT = (
    ('N', _('Normal')),
    ('R', _('Rupture')),
    ('P', _('Promotion')),
)

class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)



class ProductQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(name__icontains=query) |
            Q(reference__icontains=query) |
            Q(gamme__brand__name__icontains=query) |
            # Q(product_type__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(text__icontains=query) & Q(actif=True)
        )
        return self.filter(lookups) 

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nom')
    actif = models.BooleanField(verbose_name='actif', default=True)
    def __str__(self):
        return self.name
    def products_count(self):
        return Product.objects.filter(gamme__brand_id=self.id).count()
    class Meta:
        ordering = ('id',)
        verbose_name = '- Marque'
        verbose_name_plural = '- Marques'

class Gamme(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nom')
    brand = models.ForeignKey(Brand, related_name="gammes", on_delete=models.CASCADE, blank=True, null=True)

    actif = models.BooleanField(verbose_name='actif', default=True)
    objects = ActiveManager()
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = '- Gamme'
        verbose_name_plural = '- Gammes'


class Category(MPTTModel):
    name  = models.CharField( max_length=150, verbose_name='Nom')
    slug  = models.SlugField( max_length=150, unique= True, verbose_name='URL')
    actif = models.BooleanField(verbose_name='actif', default=True)
    icon  = models.ImageField(upload_to='images/categories', null=True, blank=True)
    # tree = models.ForeignKey(Tree, verbose_name="Branche de Catégorie",related_name="sub_categories" ,on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    objects = ActiveManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Catégorie'
        verbose_name_plural = '- Catégories'
    class MPTTMeta:
        order_insertion_by = ["name"]
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name +'-'+str(self.id))
        return super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/produits/?category={self.id}"


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """
    name = models.CharField(verbose_name=_("Type"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = _("- Produits Type")
        verbose_name_plural = _("- Produits Types")
    def __str__(self):
        return self.name

class Atribute(models.Model):
    name = models.CharField(verbose_name=_("Atribut"), help_text=_("Required"), max_length=255)
    product_type = models.ForeignKey(ProductType, related_name="atributes",on_delete=models.CASCADE)
    class Meta:
        verbose_name = _("Produits Specification")
        verbose_name_plural = _("Produits Specifications")
    def __str__(self):
        return self.name


class Product(models.Model):
    name            = models.CharField( max_length=200, verbose_name='Nom')
    reference       = models.CharField( max_length=200, verbose_name='Référence', unique=True)
    slug            = models.SlugField( max_length=150, unique= True, verbose_name='URL')
    category        = TreeForeignKey(Category, verbose_name="Catégorie",related_name="products" ,on_delete=models.CASCADE, blank=True, null=True)
    text            = models.TextField(verbose_name='petit text', blank=True, null=True)
    description     = tinymce_models.HTMLField(verbose_name='Déscription du produit', blank=True, null=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    old_price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ancien prix",blank=True, null=True)
    gamme      = models.ForeignKey(Gamme, blank=True, null=True,related_name="products", on_delete=models.CASCADE)
    actif      = models.BooleanField(verbose_name='actif', default=True)
    new        = models.BooleanField(verbose_name='Nouveau', default=False)
    top        = models.BooleanField(verbose_name='Meilleur vente', default=False)
    status     = models.CharField(choices=STATUS_PRODUIT, max_length=1, default='N', blank=True, null=True, verbose_name='Status')
    stock  =    models.IntegerField( default=1,  verbose_name="Stock initial",blank=True, null=True)
    created = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)
    # product_type    = models.ForeignKey(ProductType, on_delete=models.RESTRICT, blank=True, null=True)

    # tag        = models.ManyToManyField(Tag, blank=True)
    # brand           = models.ForeignKey(Brand, related_name="brand_products", on_delete=models.CASCADE, blank=True, null=True)
    
    objects = ProductManager()
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Produit'
        verbose_name_plural = '- Produits'
    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.name +'-'+str(self.id))
    #         return super(Product, self).save(*args, **kwargs)    
    def promo(self):
        try:
            pourcentage = (self.price / self.old_price) * 100 -100
            return int(pourcentage)
        except:
            return None
    def get_absolute_url(self):
        return reverse("core:productDetail", args=[self.slug])


class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    key =   value = models.CharField(verbose_name=_("Carectéristique"),help_text=_("Atribute Value(maximum of 255 words"),max_length=255,)
    value = models.CharField(
        verbose_name=_("Valeur"),
        help_text=_("Atribute Value(maximum of 255 words"),
        max_length=255,
    )
    class Meta:
        verbose_name = _("Produit Details")
        verbose_name_plural = _("Produit Details")

    def __str__(self):
        return self.value

class AtributesValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(Atribute, related_name='values',on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Atribute Value(maximum of 255 words"),
        max_length=255,
    )
    class Meta:
        verbose_name = _("Atribute Value")
        verbose_name_plural = _("Atribute Values")
    def __str__(self):
        return self.value

class PhotoProduct(models.Model):
    fichier   = models.ImageField(upload_to='images/produits') 
    actif   = models.BooleanField(verbose_name='actif', default=True)
    produit = models.ForeignKey(Product, related_name="photos", on_delete=models.CASCADE)


class ProductDocument(models.Model):
    file    = models.FileField(upload_to='images/produits') 
    name    = models.CharField(verbose_name=_("Nom du document") , max_length=25)
    actif   = models.BooleanField(verbose_name='actif', default=True)
    produit = models.ForeignKey(Product, related_name="documents", on_delete=models.CASCADE)

class ContactForm(models.Model):
    name        = models.CharField(verbose_name=_('Nom complet'), max_length=100)
    phone       = models.CharField(verbose_name=_("Téléphone") , max_length=25)
    email       = models.EmailField(verbose_name=_("Email"), null=True, blank = True)
    subject     = models.CharField(verbose_name=_("Sujet"), max_length=50, blank=True)
    message     = models.TextField(verbose_name=_("Message"), blank=True, null=True)
    date_sent = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('id',)
        verbose_name = 'Formulaire de contact'
        verbose_name_plural = 'Formulaire de contact'