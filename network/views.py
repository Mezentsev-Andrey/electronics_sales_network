from django_filters.rest_framework import DjangoFilterBackend    # type: ignore
from rest_framework import generics, viewsets

from network.filter import NetworkNodeFilter
from network.models import NetworkNode, Product
from network.serializers import NetworkNodeSerializer, ProductSerializer
from users.permissions import IsActiveUser   # type: ignore


class ProductViewSet(viewsets.ModelViewSet):
    """Контроллер для создания, редактирования и удаления продукта, а также
    просмотра всего списка продуктов и просмотра отдельного продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsActiveUser]


class NetworkNodeCreateAPIView(generics.CreateAPIView):
    """Контроллер создания цепочки сети."""

    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]


class NetworkNodeListAPIView(generics.ListAPIView):
    """Контроллер просмотра списка всех цепочек сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter


class NetworkNodeRetrieveView(generics.RetrieveAPIView):
    """Контроллер просмотра одной отдельной цепочки сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]


class NetworkNodeUpdateView(generics.UpdateAPIView):
    """Контроллер редактирования цепочки сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]


class NetworkNodeDestroyView(generics.DestroyAPIView):
    """Контроллер удаления цепочки сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]
