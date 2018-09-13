from django import forms

from posts.models import Post

class PostForm(forms.models.ModelForm):

    class Meta:
        model = Post
        exclude = ['publication_date']
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
            'expiring_date': forms.fields.DateInput(attrs={
                'input_type': 'date',
                'class': 'form-control'
            }),
        }
