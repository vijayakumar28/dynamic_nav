from django.urls import path
from .views import category_view

urlpatterns = [
    path('', category_view, name='homepage'),  # Homepage view
    path('admin-panel/', category_view, name='admin_panel'),  # Admin panel view
    path('<slug:slug>/', category_view, name='category_detail'),  # Dynamic category URLs
]
