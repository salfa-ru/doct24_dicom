# import django_filters
#
#
#
# class DoctorMultipleFilterBackend(django_filters.FilterSet):
#
#     seniority_min = django_filters.filters.NumberFilter(
#         field_name='seniority', lookup_expr='gte')
#
#     """ список id специализаций  """
#     spec_ids = django_filters.filters.BaseInFilter(
#         field_name='specialization__id',
#         lookup_expr='in'
#     )
#
#     category_ids = django_filters.filters.BaseInFilter(
#         field_name='category',
#         lookup_expr='in'
#     )
#
#     rank_ids = django_filters.filters.BaseInFilter(
#         field_name='rank',
#         lookup_expr='in'
#     )
#
#     scientific_degree_ids = django_filters.filters.BaseInFilter(
#         field_name='scientific_degree',
#         lookup_expr='in'
#     )
#
#     gender_ids = django_filters.filters.BaseInFilter(
#         field_name='user__gender',
#         lookup_expr='in'
#     )
#
#     class Meta:
#         model = Doctor
#         fields = ('spec_ids', 'category_ids', 'rank_ids',
#                   'scientific_degree_ids', 'gender_ids', 'seniority_min')
