# Generated by Django 3.2.6 on 2021-10-04 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0024_alter_partner_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realisationphotos',
            name='realisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='business.realisation', verbose_name='Projet / Réalisation'),
        ),
    ]
