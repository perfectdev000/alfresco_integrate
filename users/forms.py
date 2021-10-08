from django import forms
from .models import Users
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Users
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', max_length=8, min_length=6,
                                                        help_text='The password must be between 6 and 8 characters',
                                                        widget=forms.PasswordInput(attrs={
                                                        'placeholder': 'Password',
                                                    }))
    password2 = forms.CharField(label='Password confirmation', max_length=8, min_length=6,
                                                                widget=forms.PasswordInput(attrs={
                                                                'placeholder': 'Retype Password',

                                                                }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
                                                        'placeholder': 'email',
                                            }))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={
                                                            'placeholder': 'Full Name',
                                                    }))

    class Meta:
        model = Users
        fields = ('full_name', 'email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        print("user:forms.save->", user)
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                            'placeholder': 'Email Address'
                            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                'placeholder': 'Password'
                            }))
    class Meta:
        fields = ('email', 'password')

class ResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                            'placeholder': 'Email Address'
    }))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user =  Users.objects.get(email=email)
        except:
            raise forms.ValidationError('There is no account with this email address')


    class Meta:
        fields = ('email',)
