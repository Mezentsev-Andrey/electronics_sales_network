from django.db import models  # type: ignore
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

NULLABLE = {"blank": True, "null": True}


class SupplierType(models.TextChoices):
    """Тип поставщика."""

    FACTORY = "factory", _("завод")
    RETAIL = "retail", _("розничная сеть")
    SELLER = "seller", _("индивидуальный предприниматель")


class Product(models.Model):
    """Модель продукта."""

    title = models.CharField(max_length=100, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель", **NULLABLE)
    release_date = models.DateField(
        verbose_name="Дата выхода продукта на рынок", **NULLABLE
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = (
            "title",
            "release_date",
        )

    def __str__(self) -> str:
        return f"{self.title} {self.model}"


class NetworkNode(models.Model):
    """Модель звена сети."""

    title = models.CharField(max_length=150, unique=True, verbose_name="Название")
    email = models.EmailField(max_length=50, verbose_name="Почта")
    country = models.CharField(max_length=50, verbose_name="Страна", **NULLABLE)
    city = models.CharField(max_length=50, verbose_name="Город", **NULLABLE)
    street = models.CharField(max_length=70, verbose_name="Улица", **NULLABLE)
    house = models.PositiveSmallIntegerField(verbose_name="Номер дома", **NULLABLE)
    type = models.CharField(
        max_length=7,
        choices=SupplierType.choices,
        default=SupplierType.FACTORY,
        verbose_name="Тип продавца",
    )
    time = models.DateTimeField(default=timezone.now, verbose_name="Время создания")
    supplier = models.ForeignKey(
        "NetworkNode", **NULLABLE, on_delete=models.SET_NULL, verbose_name="Поставщик"
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Задолженность перед поставщиком",
    )
    products = models.ManyToManyField(Product, blank=True, verbose_name="Продукты")

    class Meta:
        verbose_name = "Сетевое звено"
        verbose_name_plural = "Сетевые звенья"
        ordering = ("title", "type")

    def __str__(self) -> str:
        return f"{self.title} {self.debt}"
