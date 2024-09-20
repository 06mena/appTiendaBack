from django.urls import path, include #funciones para las urls 
from rest_framework.routers import DefaultRouter #rutas basada en viewset 
# from .views import ClienteViewSet, CategoriaViewSet, productoViewSet, PedidoViewSet, ProductoPorPedidoViewSet, CrearPedido
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import productoViewSet, CrearPedidoView, ProductoRelacionadosView, CalificarProductoView, ProductosEnOfertaView, tipViewSet, ClienteViewSet, CategoriaViewSet, PedidoViewSet, ProductoPorPedidoViewSet

router = DefaultRouter() #genera auntomaticamente las rutas 
router.register(r'productos', productoViewSet, basename='producto')
router.register(r'tips', tipViewSet) 
router.register(r'clientes', ClienteViewSet)
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'pedidos', PedidoViewSet)
router.register(r'productos-por-pedido', ProductoPorPedidoViewSet)

# incluyen las rutas generadas por la línea de código arriba
urlpatterns = [
    path('', include(router.urls)),
    path('crear-pedido/', CrearPedidoView.as_view(), name='crear-pedido'), 
    path('productos/<int:pk>/relacionados/', ProductoRelacionadosView.as_view(), name='productos-relacionados'), 
    path('productos/<int:pk>/calificar/', CalificarProductoView.as_view(), name='calificar_producto'),
    path('productos-oferta/', ProductosEnOfertaView.as_view(), name='productos_en_oferta'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Ruta para obtener el token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Ruta para refrescar el token JWT
]
