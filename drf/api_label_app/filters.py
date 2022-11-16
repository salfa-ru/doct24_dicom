import django_filters

from api_label_app.models import Label


class LabelFilterBackend(django_filters.FilterSet):

    research_id = django_filters.filters.BaseInFilter(
        field_name='research', lookup_expr='in'
    )

    class Meta:
        model = Label
        fields = ('research_id', )
