# Generated by Django 5.0.2 on 2024-09-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apishop', '0010_alter_tbl_producto_precio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
