# Generated by Django 5.0.2 on 2024-09-19 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apishop', '0015_remove_tbl_producto_estado_tbl_pedido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbl_producto',
            name='estado',
            field=models.CharField(default='Activo', max_length=20),
        ),
    ]
