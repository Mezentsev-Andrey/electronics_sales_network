from rest_framework.serializers import ValidationError


class NetworkNodeValidator:
    """
    Валидирует:
    - завод не может ни у кого закупать;
    - завод не может быть должником;
    - дебиторская задолженность не может быть установлена без наличия поставщика.
    """

    def __call__(self, seller):
        if seller.get("type", None) == "factory":
            if seller.get("supplier", None):
                raise ValidationError("Завод не может закупать товары для реализации.")
            if seller.get("debt", None):
                raise ValidationError("Завод не может быть должником по закупкам.")
        else:
            if seller.get("debt", None) and not seller.get("seller", None):
                raise ValidationError(
                    "Задолженность перед поставщиком не может быть изменена через API."
                )
