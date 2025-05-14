from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'id': 'floatingEmail'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'floatingUsername'
        })
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'floatingPhone'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'id': 'floatingPassword1'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'id': 'floatingPassword2'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("The phone number should only contains digit numbers!")
        if len(phone) != 11 and len(phone) != 12:
            raise forms.ValidationError("The phone number should be 11 or 12 number!")
        if not (phone.startswith('09') or phone.startswith('98')):
            raise forms.ValidationError('The phone number should start with 09 or 98!')
        return phone

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.filter(user=user).update(phone=self.cleaned_data['phone'])
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    

class UpdateUserForm(UserChangeForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
            })
    )
    email = forms.CharField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
            })
    )
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['phone'].initial = self.instance.profile.phone

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("The phone number should only contains digit numbers!")
        if len(phone) != 11 and len(phone) != 12:
            raise forms.ValidationError("The phone number should be 11 or 12 number!")
        if not (phone.startswith('09') or phone.startswith('98')):
            raise forms.ValidationError('The phone number should start with 09 or 98!')
        return phone

    def save(self, commit=True):
        user = self.instance
        if commit:
            Profile.objects.filter(user=user).update(phone=self.cleaned_data['phone'])
        return user
    

class CustomPasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(
        label="old password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password is incorrect")
        return old_password
    
    def save(self, commit=True): 
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user