import django_filters   # type: ignore

from .models import NetworkNode


class NetworkNodeFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(lookup_expr='icontains', label='Страна')

    class Meta:
        model = NetworkNode
        fields = ['country']
