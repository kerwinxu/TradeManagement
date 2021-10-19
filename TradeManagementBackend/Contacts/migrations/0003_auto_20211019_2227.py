# Generated by Django 3.2.5 on 2021-10-19 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contacts', '0002_auto_20211019_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='webside',
            field=models.URLField(blank=True, max_length=100, null=True, verbose_name='网站'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
    ]
