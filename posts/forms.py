from django import forms
from .models import Post, PostImage

class PostForm(forms.ModelForm):
    # 'virtual' field to handle the comma-separated string
    tags_str = forms.CharField(
        required=False,
        label="Tags (separated by commas)",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'berlin, python, coding'})
    )

    class Meta:
        model = Post
        fields = ['caption', 'tags_str']
        widgets = {
            'caption': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3,
                       'placeholder': 'Write a caption...'}),
        }

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }