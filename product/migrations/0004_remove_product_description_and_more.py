# Generated by Django 5.1 on 2024-09-01 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_rename_product_description_product_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_url',
        ),
    ]
