from django.contrib import admin
from django import forms
from django.forms import TextInput

from modules.core.mixins import TrackUserMixin
from modules.core.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {"name": TextInput(attrs={"size": 70})}


@admin.register(Category)
class CategoryAdmin(TrackUserMixin, admin.ModelAdmin):
    form = CategoryForm
