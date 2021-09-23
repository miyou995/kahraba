# Generated by Django 3.2.6 on 2021-09-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='couleur',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='pointure',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='taille',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='attribute_1',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='spécificité 1'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='attribute_2',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='spécificité 2'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='attribute_3',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='spécificité 3'),
        ),
    ]