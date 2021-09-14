from django.db import models
# Create your models here.


class Tag(models.Model):
    name = models.CharField(verbose_name ="nom", max_length=150)
    # hex_value   = models.CharField(max_length=7, verbose_name="Valeur hexadécimale")
    def __str__(self):
        return self.name