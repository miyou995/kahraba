# Generated by Django 3.2.6 on 2021-09-01 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210901_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='Atribute Value(maximum of 255 words', max_length=255, verbose_name='Carectéristique')),
                ('value', models.CharField(help_text='Atribute Value(maximum of 255 words', max_length=255, verbose_name='Valeur')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'verbose_name': 'Atribute Value',
                'verbose_name_plural': 'Atribute Values',
            },
        ),
    ]
