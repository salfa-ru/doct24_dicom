from django.contrib import admin

from project.settings import EMPTY_FIELD
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'uid', 'username', 'first_name', 'last_name', 'patronymic',
        'created_at', 'updated_at', 'deleted_at',
        'is_delete')
    list_editable = ('is_delete',)
    list_filter = ('created_at', 'is_delete')
    search_fields = ('username',)
    empty_value_display = EMPTY_FIELD
