import django_filters

class YourFilter(django_filters.FilterSet):
    # Define your fields here
    name = django_filters.CharFilter(lookup_expr='icontains')
    documentId = django_filters.NumberFilter()