from django.contrib.auth.forms import UserCreationForm
from .models import Chapter, Code, CustomUser
from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import SplitPhoneNumberField
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model


class UserLoginForm(AuthenticationForm):
    captcha = CaptchaField()
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone = SplitPhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email
    
class VerifyForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    grad_year = forms.CharField(required=True, max_length=4, widget=forms.TextInput(attrs={'class':'form-control'}))
    chapter = forms.ChoiceField(choices=(), required=True, widget=forms.Select(attrs={'class':'form-control'}))
    
    def __init__(self, chap_choices, *args, **kwargs):
        super(VerifyForm, self).__init__(*args, **kwargs)
        self.fields['chapter'].choices = chap_choices

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text='Enter SMS verification code.')

    class Meta:
        model = Code
        fields = ('number',)

    def __init__(self, *args, **kwargs):
        super(CodeForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['class'] = 'form-control'


   