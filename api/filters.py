from django_filters import rest_framework as filters
from .models import Titles, Genre, Category


class TitlesFilter(filters.FilterSet):
    genre = filters.ModelMultipleChoiceFilter(
        field_name='genre__slug', to_field_name='slug', queryset=Genre.objects.all())
    category = filters.ModelMultipleChoiceFilter(
        field_name='category__slug', to_field_name='slug', queryset=Category.objects.all())
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
