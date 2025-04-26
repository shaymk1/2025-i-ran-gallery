from django import forms
from .models import About, Blog


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "image",
            "date_created",
            "last_updated",
            "slug",
            "categories",
            "tags",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'tags',
            'data-role': 'tagsinput',
        })
