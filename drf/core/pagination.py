""" Глобальный модуль пагинации """
from rest_framework.pagination import PageNumberPagination

from config.config import settings


class ProjectPagination(PageNumberPagination):
    """ Класс проектной пагинации """
    page_size_query_param = 'page_size'
    max_page_size = settings.REST_FRAMEWORK['MAX_PAGE_SIZE']
