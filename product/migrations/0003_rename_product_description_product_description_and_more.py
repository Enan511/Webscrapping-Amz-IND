# Generated by Django 5.1 on 2024-09-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_description',
            new_name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='product_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
