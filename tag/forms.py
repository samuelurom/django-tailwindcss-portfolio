from django import forms
from .models import Tag, TaggedItem


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"
