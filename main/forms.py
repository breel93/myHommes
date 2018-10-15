from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, User
from django.contrib.auth import get_user_model



User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None


    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    # save user method
    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']    

        if commit:
            user.save()

        return user 

class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class UpdateCustomerFormTwo(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =(
            'address',
            'city',
            'state',
            'phone_number'
        )

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
