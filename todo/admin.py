from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('title', 'user', 'important', 'created', 'date_compleated',)
    list_filter = ('user',)


admin.site.register(Todo, TodoAdmin)
