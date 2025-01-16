from django.db import models
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError

class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name

def has_permission(user, permission_name):
    """Check if the user has the specified permission."""
    if user.is_authenticated:
        return user.userprofile.role.permissions.filter(codename=permission_name).exists()
    return False

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)  # Active or inactive status

    def __str__(self):
        return self.user.username

class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='subcategories',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)  # Enforce unique URLs
    status = models.BooleanField(default=True)

    def clean(self):
        # Validate uniqueness of name within the same parent
        if Category.objects.filter(name=self.name, parent=self.parent).exclude(id=self.id).exists():
            raise ValidationError(f"A category with the name '{self.name}' already exists under the same parent.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call clean() to validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
