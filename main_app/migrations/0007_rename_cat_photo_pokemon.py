# Generated by Django 4.2.4 on 2023-08-16 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='cat',
            new_name='pokemon',
        ),
    ]
