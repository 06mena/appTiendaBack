# Generated by Django 5.0.2 on 2024-09-19 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apishop', '0009_tbl_tip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_producto',
            name='precio',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
    ]
