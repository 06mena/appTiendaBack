# Generated by Django 5.0.2 on 2024-09-19 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apishop', '0014_alter_tbl_producto_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tbl_producto',
            name='estado',
        ),
        migrations.AddField(
            model_name='tbl_pedido',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('enviado', 'Enviado'), ('entregado', 'Entregado')], default='pendiente', max_length=20),
        ),
    ]
