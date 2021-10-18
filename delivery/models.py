from django.db import models


class Wilaya(models.Model):

    name = models.CharField(max_length=40, verbose_name="Wilaya")
    mat = models.IntegerField(verbose_name='Matricule', blank=True,null=True)
    price = models.DecimalField( max_digits=10, verbose_name="Prix de Livraison", decimal_places=2)
    active = models.BooleanField(default=True, verbose_name="Livraison Active")
    
    class Meta:
        verbose_name = "Wilaya"
        verbose_name_plural = "1. Wilayas"

    def __str__(self):
        return self.name

class Commune(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, verbose_name="Wilaya")
    name = models.CharField(max_length=30, verbose_name="Commune")
    # active = models.BooleanField(default=True, verbose_name="Livraison Active")
    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "2. Communes"        
        
    def __str__(self):
        return self.name
        