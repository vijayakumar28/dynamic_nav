from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Role, UserProfile, Category


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'categories_list']

    def categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    categories_list.short_description = 'Categories'


admin.site.register(Role, RoleAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'status']


admin.site.register(UserProfile, UserProfileAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ['username', 'email']


# Unregister the default User model and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'url', 'status']
    search_fields = ['name', 'url']
    list_filter = ['status']

    def save_model(self, request, obj, form, change):
        try:
            # Validate uniqueness for name and parent combination
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            self.message_user(request, f"Error: {e.message}", level='error')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter the parent field to show only main categories
        form.base_fields['parent'].queryset = Category.objects.filter(parent=None)
        return form


admin.site.register(Category, CategoryAdmin)
