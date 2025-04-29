from django import forms
from .models import About, Blog
# from taggit.forms import TagField
from taggit.models import Tag


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
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control",
                "data-role": "tagsinput",
            }
        ),
        required=False,
        help_text="Hold Ctrl (Windows) or Cmd (Mac) to select multiple tags.",
    )

    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "image",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "tags",
                "data-role": "tagsinput",
            }
        )
