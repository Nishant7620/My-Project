# Generated by Django 5.0.1 on 2024-02-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='pet_image',
        ),
        migrations.AddField(
            model_name='products',
            name='product_image',
            field=models.ImageField(default='none', upload_to='product_images'),
        ),
    ]
