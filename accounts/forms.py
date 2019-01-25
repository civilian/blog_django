from django import forms

PASSWORD_DONT_MATCH = "The passwords don't match"

class RegisterUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        retype_password = self.cleaned_data.get('retype_password')
        if password == None or retype_password == None:
            pass
        elif password != retype_password:
            self._errors['retype_password'] = [PASSWORD_DONT_MATCH]
        return self.cleaned_data