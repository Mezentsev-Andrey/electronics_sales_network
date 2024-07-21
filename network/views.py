from rest_framework import viewsets, generics

from network.models import Product, NetworkNode
from network.serializers import ProductSerializer, NetworkNodeSerializer
from users.permissions import IsActiveUser


class ProductViewSet(viewsets.ModelViewSet):
    """ Контроллер для создания, редактирования и удаления продукта, а также
        просмотра всего списка продуктов и просмотра отдельного продукта."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsActiveUser]


class NetworkNodeCreateAPIView(generics.CreateAPIView):
    """ Контроллер создания цепочки сети."""

    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]


class NetworkNodeListAPIView(generics.ListAPIView):
    """ Контроллер просмотра списка всех цепочек сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]
    filterset_fields = ['country', ]


class NetworkNodeRetrieveView(generics.RetrieveAPIView):
    """ Контроллер просмотра одной отдельной цепочки сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]


class NetworkNodeUpdateView(generics.UpdateAPIView):
    """ Контроллер редактирования цепочки сети."""

    serializer_class = NetworkNodeSerializer
    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]


class NetworkNodeDestroyView(generics.DestroyAPIView):
    """ Контроллер удаления цепочки сети."""

    queryset = NetworkNode.objects.all()
    permission_classes = [IsActiveUser]
