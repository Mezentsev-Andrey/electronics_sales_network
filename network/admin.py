from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network.models import Product, NetworkNode


@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(self, request, queryset, ):
    queryset.update(debt=0)
    self.message_user(request, "Задолженность перед поставщиком успешно очищена у выбранных объектов.")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'release_date')
    list_filter = ('title', 'model')
    search_fields = ('title', 'model')


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'supplier', 'debt')
    list_filter = ('city', 'supplier')
    search_fields = ('city',)
    actions = [clear_debt]

    # def supplier_link(self, obj):
    #     if obj.supplier:
    #         url = reverse('admin:network_link_change', args=[obj.supplier.id])
    #         return format_html('<a href="{}">{}</a>', url, obj.supplier.email)
    #     return "-"
    #
    # supplier_link.short_description = 'Поставщик'  # type: ignore
