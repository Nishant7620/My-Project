from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Customer,Contact


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.TextInput(attrs={'class':'form-control'}),
        'first_name':forms.TextInput(attrs={'class':'form-control'}),
        }

class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'})) 
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))  

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=  forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 =  forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))      

class UserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name','email', 'date_joined', 'last_login']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                'first_name':forms.TextInput(attrs={'class':'form-control'}), 
                'email':forms.TextInput(attrs={'class':'form-control'}), 
                'date_joined':forms.DateInput(attrs={'class':'form-control','type':'date'}),
                'last_login':forms.DateInput(attrs={'class':'form-control','type':'date'})}


class AdminProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = '__all__'


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['name','email','message']

        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
        'email':forms.TextInput(attrs={'class':'form-control'}),
        'message':forms.Textarea(attrs={'class':'form-control'})}
    
