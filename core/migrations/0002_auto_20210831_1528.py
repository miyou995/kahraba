# Generated by Django 3.2.6 on 2021-08-31 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('id',), 'verbose_name': 'Catégorie', 'verbose_name_plural': '- Catégories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('id',), 'verbose_name': 'Produit', 'verbose_name_plural': '- Produits'},
        ),
    ]