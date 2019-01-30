from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

PASSWORD_DONT_MATCH = "The passwords don't match"
USERNAME_ALREADY_IN_USER = 'Username %s is alreay in use.'

class SignUpUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def save(self):
        return User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password'])


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(USERNAME_ALREADY_IN_USER % username)



    def clean_retype_password(self):
        password = self.cleaned_data.get('password')
        retype_password = self.cleaned_data.get('retype_password')
        if password == None or retype_password == None:
            pass
        elif password != retype_password:
            raise forms.ValidationError(PASSWORD_DONT_MATCH)
        return self.cleaned_data