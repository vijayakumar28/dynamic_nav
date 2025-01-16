from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'url', 'status']
    search_fields = ['name', 'url']  # Enable search in admin panel
    list_filter = ['status']        # Add filtering options

    def save_model(self, request, obj, form, change):
        # Validate uniqueness for name and parent combination
        if Category.objects.filter(name=obj.name, parent=obj.parent).exclude(id=obj.id).exists():
            raise ValidationError(f"A category with the name '{obj.name}' already exists under the same parent.")
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter the parent field to show only main categories
        form.base_fields['parent'].queryset = Category.objects.filter(parent=None)
        return form

admin.site.register(Category, CategoryAdmin)
