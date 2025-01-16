from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Role

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    status = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        
        # Create a UserProfile for the newly created user
        UserProfile.objects.create(user=user, role=self.cleaned_data['role'], status=self.cleaned_data['status'])
        return user
