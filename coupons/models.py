from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver

# translation
from django.utils.translation import gettext_lazy as _

class Coupon(models.Model):
    '''
    DESCRIPTION:
    Code: The code that users have to enter in order to apply the coupon to their
    purchase
    valid_from: datetime value - when coupon becomes valid
    valid_to: datetime value - when coupon becomes invalid
    discount: discount rate to apply, minimum is 0, maximum is 100
    active: indicates whether the coupon is active
    stock: indicates left quantity
    '''
    code                = models.CharField(max_length=40, unique=True, verbose_name="Code coupon")
    valid_from          = models.DateTimeField(verbose_name='Valide à partir de')
    valid_to            = models.DateTimeField(verbose_name='Valide jusqu\'à')
    discount_amount     = models.IntegerField(verbose_name='Montant' , validators= [MinValueValidator(0)], default= 0)
    discount_percentage = models.IntegerField(verbose_name= 'Pourcentage',  validators= [MinValueValidator(0), MaxValueValidator(100)], default=0)
    active              = models.BooleanField(verbose_name='Actif', default=True)
    stock               = models.IntegerField(verbose_name = 'Coupons restant', default= 1)
    used                = models.IntegerField(verbose_name = 'Utilisé', default= 0)
    
    created = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)
    # In the admin side this method will check if the values are 0 together or both set
    
    def clean(self):
        if (self.discount_amount == 0) & (self.discount_percentage == 0):
                raise ValidationError("Le pourcentage ou le montant doivent être différents de 0, pas les deux en même temps")
        if (self.discount_amount > 0) & (self.discount_percentage > 0):
                raise ValidationError('Le pourcentage ou le montant doivent être différents de 0, pas les deux en même temps')
    
    # def get_ordering(self, request):
    #    return ['valid-from']
    

    def __str__(self):
        return self.code
    
    
   