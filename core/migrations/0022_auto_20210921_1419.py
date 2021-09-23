# Generated by Django 3.2.6 on 2021-09-21 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_atributesvalue_specification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_type',
        ),
        migrations.CreateModel(
            name='Gamme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('actif', models.BooleanField(default=True, verbose_name='actif')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gammes', to='core.brand')),
            ],
            options={
                'verbose_name': '- Gamme',
                'verbose_name_plural': '- Gammes',
                'ordering': ('id',),
            },
        ),
        migrations.AddField(
            model_name='product',
            name='gamme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='core.gamme'),
        ),
    ]
