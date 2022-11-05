from django.contrib import admin

from project.settings import EMPTY_FIELD
from .models import Label


"""
    'research', 'owner', 'labels', 'created_at'
"""

@admin.register(Label)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'research', 'owner', 'labels', 'created_at'
        )
    # list_editable = ('patient_code',)
    list_filter = ('research', 'owner', 'labels', 'created_at')
    search_fields = ('research', 'owner', 'created_at')
    empty_value_display = EMPTY_FIELD
