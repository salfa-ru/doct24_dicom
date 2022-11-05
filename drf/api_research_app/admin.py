from django.contrib import admin

from project.settings import EMPTY_FIELD
from .models import Research


@admin.register(Research)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'patient_code', 'media_file', 'owner', 'created_at', 'updated_at'
        )
    # list_editable = ('patient_code',)
    list_filter = ('patient_code', 'owner', 'created_at', 'updated_at')
    search_fields = ('patient_code', 'owner', 'created_at', 'updated_at')
    empty_value_display = EMPTY_FIELD
