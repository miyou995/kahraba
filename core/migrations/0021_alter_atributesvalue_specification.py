# Generated by Django 3.2.6 on 2021-09-16 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20210916_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atributesvalue',
            name='specification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='values', to='core.atribute'),
        ),
    ]
