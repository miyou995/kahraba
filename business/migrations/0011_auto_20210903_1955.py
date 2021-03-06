# Generated by Django 3.2.6 on 2021-09-03 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_rename_banner_slide'),
    ]

    operations = [
        migrations.CreateModel(
            name='DualBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='slides/', verbose_name='photo 370 X 225 px')),
                ('url', models.URLField(verbose_name='lien')),
            ],
            options={
                'verbose_name': '3. Trois Photos Acceuil',
                'verbose_name_plural': '3. Trois Photos Acceuil',
            },
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={'verbose_name': "2. Slides haut page d'accueil", 'verbose_name_plural': "2. Slides haut page d'accueil"},
        ),
    ]
