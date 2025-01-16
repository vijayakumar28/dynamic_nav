from django.urls import path
from .views import add_user_view, category_view

urlpatterns = [
    path('', category_view, name='homepage'),  # Homepage view
    path('admin-panel/', add_user_view, name='admin_panel'),  # Admin panel for adding users
    path('manage-users/', category_view, name='manage_users'),  # Manage users view
    path('<slug:slug>/', category_view, name='category_detail'),  # Dynamic category URLs
]
