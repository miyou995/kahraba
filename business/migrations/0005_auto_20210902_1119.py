# Generated by Django 3.2.6 on 2021-09-02 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_alter_business_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name="nom de l'acomplissement")),
                ('number', models.CharField(max_length=50, verbose_name='chiffre')),
                ('icon', models.ImageField(height_field=870, upload_to='icons/', verbose_name='icon', width_field=475)),
            ],
            options={
                'verbose_name': '2. Accomplissement',
                'verbose_name_plural': '2. Accomplissement',
            },
        ),
        migrations.CreateModel(
            name='LargeBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(height_field=870, upload_to='slides/', verbose_name='Slide 870 X 475 px', width_field=475)),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Grand titre de la photo')),
                ('sub_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sous titre de la photo')),
                ('url', models.URLField(max_length=250, verbose_name='Lien')),
            ],
            options={
                'verbose_name': "2. Banners page d'accueil",
                'verbose_name_plural': "2. Banners page d'accueil",
            },
        ),
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': "2. Banners page d'accueil", 'verbose_name_plural': "2. Banners page d'accueil"},
        ),
        migrations.AlterModelOptions(
            name='slide',
            options={'verbose_name': '3. Trois Photos Acceuil', 'verbose_name_plural': '3. Trois Photos Acceuil'},
        ),
        migrations.AddField(
            model_name='business',
            name='about_photo',
            field=models.ImageField(blank=True, height_field=440, null=True, upload_to='slides/', verbose_name='Photo A propos 440 X 275 px', width_field=275),
        ),
        migrations.AddField(
            model_name='business',
            name='analytics',
            field=models.TextField(blank=True, null=True, verbose_name='Script Analytics'),
        ),
        migrations.AddField(
            model_name='business',
            name='chat_code',
            field=models.TextField(blank=True, null=True, verbose_name='Script messagerie instantané'),
        ),
        migrations.AddField(
            model_name='business',
            name='google_plus',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='Lien Compte Google plus'),
        ),
        migrations.AddField(
            model_name='business',
            name='pixel',
            field=models.TextField(blank=True, null=True, verbose_name='Script Facebook pixel'),
        ),
        migrations.AddField(
            model_name='business',
            name='twitter',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='Lien Compte Twitter'),
        ),
        migrations.AddField(
            model_name='business',
            name='youtube',
            field=models.URLField(blank=True, max_length=300, null=True, verbose_name='Lien Chaine Youtube'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='photo',
            field=models.ImageField(height_field=870, upload_to='slides/', verbose_name='Slide 870 X 475 px', width_field=475),
        ),
        migrations.AlterField(
            model_name='slide',
            name='photo',
            field=models.ImageField(height_field=225, upload_to='slides/', verbose_name='photo 370 X 225 px', width_field=370),
        ),
    ]