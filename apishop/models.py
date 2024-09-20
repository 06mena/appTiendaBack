from django.db import models
from decimal import Decimal

# Tabla Cliente
class tbl_cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

# Tabla Categoría
class tbl_categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Tabla Producto
class tbl_producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(default="Sin descripción")
    precio = models.IntegerField(default=1000)
    estado = models.CharField(max_length=20, default='Activo')
    stock = models.IntegerField(default=0)
    imagen_url = models.URLField(null=True)
    categoria = models.ForeignKey(tbl_categoria, on_delete=models.SET_NULL, null=True)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('0.0'))
    numero_de_calificaciones = models.IntegerField(default=0)

     # Campos para gestionar ofertas
    en_oferta = models.BooleanField(default=False)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00')) 

    def __str__(self):
        return self.nombre
    
    @property
    def precio_final(self):
        """Calcula el precio con descuento si el producto está en oferta."""
        if self.en_oferta:
            return self.precio * (1 - (self.porcentaje_descuento / Decimal('100')))
        return self.precio

# Tabla Pedido
class tbl_pedido(models.Model):
    cliente = models.ForeignKey(tbl_cliente, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    direccion_entrega = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Pedido {self.id} - Cliente {self.cliente.nombre}"

# Tabla Producto por Pedido (Detalle del pedido)
class tbl_producto_por_pedido(models.Model):
    pedido = models.ForeignKey(tbl_pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(tbl_producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, default="pendiente")  # Estado llenado por admin

    def __str__(self):
        return f"{self.producto.nombre} en Pedido {self.pedido.id}"

class tbl_tip(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen_url = models.URLField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.titulo