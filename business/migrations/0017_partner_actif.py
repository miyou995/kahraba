# Generated by Django 3.2.6 on 2021-09-05 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0016_partner_realisation_realisationphotos'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='actif',
            field=models.BooleanField(default=True, verbose_name='actif'),
        ),
    ]