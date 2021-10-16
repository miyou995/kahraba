import django_filters
from django_filters import filters
from .models import Product



class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    ordering = filters.OrderingFilter(
                fields=(
            ('price', 'price'),
            ('name', 'name'),
            ('brand', 'gamme__brand'),
        ),
)
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', 'category', 'new', 'price', 'gamme', 'gamme__brand', 'reference']

