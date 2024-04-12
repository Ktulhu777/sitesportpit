import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('time_create', 'time_create'),
        )
    )

    class Meta:
        model = Product
        fields = []
