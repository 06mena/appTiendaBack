import random
from django.shortcuts import render
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status
from decimal import Decimal, InvalidOperation
from .models import tbl_cliente, tbl_categoria, tbl_producto, tbl_pedido, tbl_producto_por_pedido, tbl_tip
from .serializers import ClienteSerializer, CategoriaSerializer, productoSerializer, PedidoSerializer, ProductoPorPedidoSerializer, TipSerializer

# Aplicar permisos explícitamente en las vistas donde sea necesario
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = tbl_cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [AllowAny]  # Permitir acceso público

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = tbl_categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]  # Permitir acceso público

class productoViewSet(viewsets.ModelViewSet):
    queryset = tbl_producto.objects.all()
    serializer_class = productoSerializer
    permission_classes = [AllowAny]  # Permitir acceso público
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'descripcion']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id is not None:
            queryset = queryset.filter(categoria__id=categoria_id)
        return queryset

    @action(detail=True, methods=['get'])
    def relacionados(self, request, pk=None):
        try:
            producto = tbl_producto.objects.get(id=pk)
        except tbl_producto.DoesNotExist:
            return Response({'detail': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        categoria_id = producto.categoria.id if producto.categoria else None
        productos_relacionados = tbl_producto.objects.filter(categoria_id=categoria_id).exclude(id=pk)

        if not productos_relacionados.exists():
            # Si no hay productos relacionados, seleccionar productos aleatorios
            productos = tbl_producto.objects.exclude(id=pk)
            if productos.exists():
                productos_relacionados = random.sample(list(productos), min(5, productos.count()))
            else:
                productos_relacionados = []

        serializer = productoSerializer(productos_relacionados, many=True)
        return Response(serializer.data)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = tbl_pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [AllowAny]  # Solo para pruebas, ajustar si se necesita autenticación

class ProductoPorPedidoViewSet(viewsets.ModelViewSet):
    queryset = tbl_producto_por_pedido.objects.all()
    serializer_class = ProductoPorPedidoSerializer
    permission_classes = [AllowAny]  # Solo para pruebas, ajustar si se necesita autenticación

class tipViewSet(viewsets.ModelViewSet):  # Si usas minúsculas
    queryset = tbl_tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [AllowAny]

class CrearPedidoView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            cliente_data = request.data.get('cliente', {})
            if not cliente_data.get('nombre') or not cliente_data.get('email'):
                return Response({"error": "Faltan datos del cliente."}, status=status.HTTP_400_BAD_REQUEST)

            # Crear o recuperar cliente
            cliente, created = tbl_cliente.objects.get_or_create(
                nombre=cliente_data.get('nombre'),
                email=cliente_data.get('email'),
                defaults={
                    'direccion': cliente_data.get('direccion'),
                    'telefono': cliente_data.get('celular')
                }
            )

            # Crear pedido
            pedido = tbl_pedido.objects.create(
                cliente=cliente,
                direccion_entrega=request.data.get('direccion'),
                total=request.data.get('total')
            )

            # Agregar productos al pedido
            productos_data = request.data.get('productos', [])
            if not productos_data:
                return Response({"error": "No hay productos en el pedido."}, status=status.HTTP_400_BAD_REQUEST)

            for producto_data in productos_data:
                producto_id = producto_data.get('producto')
                cantidad = producto_data.get('cantidad')
                precio_unitario = producto_data.get('precio_unitario')
                estado = producto_data.get('estado', 'pendiente')

                # Verifica que la cantidad no sea nula
                if cantidad is None:
                    return Response({"error": "La cantidad no puede ser nula."}, status=status.HTTP_400_BAD_REQUEST)
                if not isinstance(cantidad, (int, float)) or cantidad <= 0:
                    return Response({"error": "La cantidad debe ser un número positivo."}, status=status.HTTP_400_BAD_REQUEST)

                if precio_unitario is None:
                    return Response({"error": "El precio unitario no puede ser nulo."}, status=status.HTTP_400_BAD_REQUEST)
                if not isinstance(precio_unitario, (int, float)) or precio_unitario <= 0:
                    return Response({"error": "El precio unitario debe ser un número positivo."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    producto = tbl_producto.objects.get(id=producto_id)
                    tbl_producto_por_pedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,  # Asegúrate de que `cantidad` no sea nulo
                        precio_unitario=precio_unitario,
                        estado=estado
                    )
                except tbl_producto.DoesNotExist:
                    return Response({"error": f"Producto con id {producto_id} no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Pedido creado exitosamente"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProductoRelacionadosView(APIView):
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def get(self, request, pk=None):
        try:
            producto = tbl_producto.objects.get(id=pk)
        except tbl_producto.DoesNotExist:
            return Response({'detail': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        categoria_id = producto.categoria.id if producto.categoria else None
        if categoria_id is not None:
            productos_relacionados = tbl_producto.objects.filter(categoria_id=categoria_id).exclude(id=pk)
        else:
            productos_relacionados = tbl_producto.objects.none()  # No hay categoría asociada

        serializer = productoSerializer(productos_relacionados, many=True)
        return Response(serializer.data)

class CalificarProductoView(APIView):
    permission_classes = [AllowAny]  # Permite acceso sin autenticación

    def post(self, request, pk):
        try:
            producto = tbl_producto.objects.get(id=pk)
        except tbl_producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        calificacion = request.data.get('calificacion')

        try:
            calificacion = Decimal(calificacion)
        except (ValueError, InvalidOperation):
            return Response({'error': 'Calificación inválida. Debe ser un número válido.'}, status=status.HTTP_400_BAD_REQUEST)

        if not (1 <= calificacion <= 5):
            return Response({'error': 'Calificación inválida. Debe ser entre 1 y 5.'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualiza la calificación promedio
        producto.numero_de_calificaciones += 1
        total_calificaciones = Decimal(producto.calificacion_promedio) * (producto.numero_de_calificaciones - 1)
        producto.calificacion_promedio = (total_calificaciones + calificacion) / producto.numero_de_calificaciones
        producto.save()

        return Response({'message': 'Calificación añadida con éxito', 'calificacion_promedio': str(producto.calificacion_promedio)}, status=status.HTTP_200_OK)
    
class ProductosEnOfertaView(APIView):
    permission_classes = [AllowAny]  # Permitir acceso público

    def get(self, request):
        productos_en_oferta = tbl_producto.objects.filter(en_oferta=True)
        serializer = productoSerializer(productos_en_oferta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PedidoDetailView(APIView):
    def get(self, request, pk, format=None):
        # Utiliza get_object_or_404 para manejar el error 404
        pedido = get_object_or_404(tbl_pedido, pk=pk)
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pedido = get_object_or_404(tbl_pedido, pk=pk)
        serializer = PedidoSerializer(pedido, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)