from django import forms
from django.forms import ClearableFileInput
from users.models import Users
from .models import Files_upload, Project_file_List
from users.models import Users

class FileInputForm(forms.ModelForm):
    up_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),     required=True
    )
    user = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.HiddenInput())

    def save(self, *args, **kwargs):
        print(self.cleaned_data['up_file'])
        return super().save(commit=False)

    class Meta:
        model = Files_upload
        fields = ('up_file','user')

class UrlFileInputForm(forms.ModelForm):
    from_url = forms.CharField(
        label='Input Url',
        widget=forms.TextInput(attrs={'placeholder': 'http://www.sample.com/example'})
    )
    user = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.HiddenInput())
    # def save(self, *args, **kwargs):
    #     print(self.cleaned_data['up_file'])
    #     return super().save(commit=False)

    class Meta:
        model = Files_upload
        fields = ('from_url','user')

class RenameForm(forms.Form):
    new_name = forms.CharField(max_length=150, label='New Name')
    class Meta:
        fields = ('new_name',)

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)

class Upload_files_from_alfresco_Form(forms.Form):
    upload1 = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )
    upload2 = forms.FileField(
        widget=forms.ClearableFileInput()
    )

    # def save(self, *args, **kwargs):
    #     print(self.cleaned_data['up_file'])
    #     return super().save(commit=False)
    class Meta:
        model = Files_upload
        # fields = ['files1','files2']
        # widgets = {
        #     'files1': ClearableFileInput(attrs={'multiple': True}),
        #     'files2': ClearableFileInput(attrs={'multiple': True}),
        # }
    # class Meta:
    #     model = Files_upload
    #     fields = ('up_file','user')