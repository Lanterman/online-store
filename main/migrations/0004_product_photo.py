# Generated by Django 3.2.9 on 2021-11-03 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211101_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Фото'),
        ),
    ]
