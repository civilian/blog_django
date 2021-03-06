import datetime

from django import forms
from django.core.exceptions import ValidationError

from posts.models import Post

EXPIRATION_DATE_IS_WRONG = 'The expiring date needs to be after the publication date.'

class PostForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Post
        exclude = []
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'image': forms.fields.FileInput(attrs={
                'class': 'form-control'
            }),
            'publication_date': forms.fields.DateInput(attrs={
                'input_type': 'date',
                'class': 'form-control'
            }),
            'expiring_date': forms.fields.DateInput(attrs={
                'input_type': 'date',
                'class': 'form-control'
            }),
        }

    def clean(self):
        expiring_date = self.cleaned_data.get('expiring_date')
        publication_date = self.cleaned_data.get('publication_date')
        if publication_date == None or expiring_date == None:
            pass
        elif publication_date > expiring_date:
            self._errors['expiring_date'] = [EXPIRATION_DATE_IS_WRONG]
        return self.cleaned_data
