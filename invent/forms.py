from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


class SearchForm(forms.Form):
    query = forms.CharField()


class InvForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = {
            'name',
            'tech_id',
            'invent_id',
            'room',
            'description',
            'comment',
            'department'
        }


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = {
            'inv_id',
            'completed',
            'comment'
        }


class DepForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = {
            'name'
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = {
            'room',
            'comment',
            'department'
        }
