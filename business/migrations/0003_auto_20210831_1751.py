# Generated by Django 3.2.6 on 2021-08-31 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20210831_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': '2. Banner', 'verbose_name_plural': '2. Banner'},
        ),
        migrations.AlterModelOptions(
            name='business',
            options={'verbose_name': '1. Infomation', 'verbose_name_plural': '1. Infomation'},
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={'verbose_name': '3. Photos Acceuil', 'verbose_name_plural': '3. Photos Acceuil'},
        ),
    ]
