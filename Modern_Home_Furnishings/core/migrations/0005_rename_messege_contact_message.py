# Generated by Django 5.0.1 on 2024-03-05 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='messege',
            new_name='message',
        ),
    ]
