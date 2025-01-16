from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    url = models.CharField(
        max_length=100,
        unique=True,
        
        help_text=_("Enter a valid URL for the category."),
    )
    status = models.BooleanField(default=True)

    def clean(self):
        # Validate uniqueness of name within the same parent
        if Category.objects.filter(name=self.name, parent=self.parent).exclude(id=self.id).exists():
            raise ValidationError(
                _(f"A category with the name '{self.name}' already exists under the same parent.")
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() to validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    def get_navbar_items(self):
        """Get the navbar menu items associated with the role's permissions."""
        # Placeholder logic: Adjust according to your permissions model
        return self.categories.all()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  # Active or inactive status

    def __str__(self):
        return self.user.username

    def get_navbar_items(self):
        """Fetch the navbar menu items for the user's role."""
        return self.role.get_navbar_items() if self.status else []
