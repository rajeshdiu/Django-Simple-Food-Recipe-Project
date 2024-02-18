from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myApp.models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Custom_User
        fields = UserCreationForm.Meta.fields + ('display_name', 'email','city','user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = Custom_User  
        fields = ['username', 'password']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['user']  

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user'] 
        
class RecipeCategoryForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = ['name', 'description']  # Adjust based on your model fields

