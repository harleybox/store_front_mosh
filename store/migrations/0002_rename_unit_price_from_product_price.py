# Generated by Django 4.2.7 on 2023-11-19 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='unit_price',
            new_name='price',
        ),
    ]
