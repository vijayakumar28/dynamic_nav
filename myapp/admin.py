from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from .models import Role, UserProfile, Category
from django.contrib.auth.admin import UserAdmin


class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'permissions_list']
    
    def permissions_list(self, obj):
        return ", ".join([perm.name for perm in obj.permissions.all()])
    permissions_list.short_description = 'Permissions'

admin.site.register(Role, RoleAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    def get_urls(self):
        # Getting the URL patterns from the base
        urls = super().get_urls()
        
        # Add your custom admin URL patterns here
        custom_urls = [
            path('custom_admin/', self.admin_site.admin_view(self.custom_admin_view)),
        ]
        
        return custom_urls + urls

    def custom_admin_view(self, request):
        # Now, we can access the request object and check user profile info
        if request.user.is_authenticated and request.user.userprofile.role.name == "Admin" and request.user.userprofile.status:
            # Your logic for the Admin view
            return HttpResponseRedirect('/somewhere')  # Redirect to some page if user is Admin and active
        else:
            return HttpResponseRedirect('/admin/')  # Redirect back to admin if conditions are not met

admin.site.register(UserProfile, UserProfileAdmin)

# Custom User Admin to include the default fields along with the ones from UserProfile
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ['username', 'email']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'url', 'status']
    search_fields = ['name', 'url']
    list_filter = ['status']

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
