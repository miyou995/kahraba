# Generated by Django 3.2.6 on 2021-09-03 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_rename_slide_threephotos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Banner',
            new_name='Slide',
        ),
    ]