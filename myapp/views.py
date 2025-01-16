from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Category
from .forms import CategoryForm

def category_view(request, slug=None):
    # Fetch main categories for the navbar
    main_categories = Category.objects.filter(parent=None)

    # If the request is to access the admin panel
    if request.path.startswith('/admin-panel/'):
        # Handle form submission for adding a new category
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_panel')  # Redirect to admin panel after submission
        else:
            form = CategoryForm()

        # Fetch all categories for admin panel
        categories = Category.objects.all()

        return render(request, 'admin_panel.html', {
            'categories': categories,
            'form': form,
            'main_categories': main_categories,
        })

    # If a slug is provided, fetch the corresponding category
    if slug:
        category = get_object_or_404(Category, url=slug)
        # Handle subcategories if applicable
        subcategories = Category.objects.filter(parent=category)

        return render(request, 'category.html', {
            'category': category,
            'subcategories': subcategories,
            'main_categories': main_categories,
        })

    # Default behavior: render homepage
    return render(request, 'navbar.html', {'main_categories': main_categories})
