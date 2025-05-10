from django import forms
from .models import About, Blog, Photo

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


class UpdateBlogForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control",
            }
        ),
        required=False,
        help_text="Hold Ctrl (Windows) or Cmd (Mac) to select multiple tags.",
    )

    class Meta:
        model = Blog
        fields = ["title", "content", "image", "tags"]


class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["title", "image", "category"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5})
    )


class SubscribeForm(forms.Form):
    email = forms.EmailField(label="example@love.com", required=True)
