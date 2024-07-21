from django.urls import path
from rest_framework.routers import DefaultRouter

from network.apps import NetworkConfig
from network.views import ProductViewSet, NetworkNodeListAPIView, NetworkNodeCreateAPIView, NetworkNodeRetrieveView, \
    NetworkNodeUpdateView, NetworkNodeDestroyView

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('network/list/', NetworkNodeListAPIView.as_view(), name='network_list'),
    path('network/create/', NetworkNodeCreateAPIView.as_view(), name='network_create'),
    path('network/retrieve/<int:pk>', NetworkNodeRetrieveView.as_view(), name='network_retrieve'),
    path('network/update/<int:pk>', NetworkNodeUpdateView.as_view(), name='network_update'),
    path('network/delete/<int:pk>', NetworkNodeDestroyView.as_view(), name='network_delete'),
] + router.urls
