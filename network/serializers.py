from rest_framework import serializers    # type: ignore

from network.models import NetworkNode, Product
from network.validators import NetworkNodeValidator


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        if "debt" in validated_data:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "Задолженность перед поставщиком не может быть изменена через API."
                }
            )
        return super().update(instance, validated_data)

    class Meta:
        model = NetworkNode
        fields = "__all__"
        validators = [NetworkNodeValidator()]
