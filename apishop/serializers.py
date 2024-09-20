from rest_framework import serializers
from .models import tbl_cliente, tbl_categoria, tbl_producto, tbl_pedido, tbl_producto_por_pedido, tbl_tip

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_cliente
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbl_categoria
        fields = ['id','nombre']

class productoSerializer(serializers.ModelSerializer):
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=tbl_categoria.objects.all(), source='categoria', write_only=True
    )
    categoria = CategoriaSerializer(read_only=True)  # Usar el serializador de categoría
    precio_final = serializers.SerializerMethodField()  # Campo calculado

    class Meta:
        model = tbl_producto
        fields = '__all__'
    
    def get_precio_final(self, obj):
        return obj.precio_final

class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)  # Incluye información detallada del cliente
    productos = serializers.SerializerMethodField()  # Personalizar la inclusión de productos

    class Meta:
        model = tbl_pedido
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()
        return instance

    def get_productos(self, obj):
        productos_pedido = tbl_producto_por_pedido.objects.filter(pedido=obj)
        return ProductoPorPedidoSerializer(productos_pedido, many=True).data


class ProductoPorPedidoSerializer(serializers.ModelSerializer):
    # Solo incluir los IDs en lugar de los serializadores completos
    pedido = serializers.PrimaryKeyRelatedField(queryset=tbl_pedido.objects.all())
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)
    cantidad = serializers.IntegerField()
    precio_unitario = serializers.DecimalField(max_digits=10, decimal_places=2)
    estado = serializers.CharField(max_length=20)

    class Meta:
        model = tbl_producto_por_pedido
        fields = '__all__'

class TipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = tbl_tip
        fields = '__all__'
