# Generated by Django 5.0.1 on 2024-03-13 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_products_discounted_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='discounted_price',
            field=models.IntegerField(default=0),
        ),
    ]
