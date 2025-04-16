from django import forms
from .models import UserRegister, Profile, Recommendation

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = UserRegister
        fields = ['username', 'email', 'password', 'role', 'location', 'climate', 'soil_type']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),  # Hides password input with form-control class
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'climate': forms.TextInput(attrs={'class': 'form-control'}),
            'soil_type': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # Updating Profile instead of UserRegister
        fields = ['profile_picture', 'full_name', 'bio', 'gardening_preferences']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'gardening_preferences': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['watering_schedule', 'fertilization_plan', 'pest_control_measures']
        widgets = {
            'watering_schedule': forms.TextInput(attrs={'class': 'form-control'}),
            'fertilization_plan': forms.TextInput(attrs={'class': 'form-control'}),
            'pest_control_measures': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import GardeningGroup

class GardeningGroupForm(forms.ModelForm):
    class Meta:
        model = GardeningGroup
        fields = ['name', 'description', 'location', 'social_media_link']

    def __init__(self, *args, **kwargs):
        super(GardeningGroupForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
