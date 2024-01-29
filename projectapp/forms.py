from django import forms
from django.forms import ModelForm, Textarea
from projectapp.models import Project


class ProjectCreationForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description','address','hide']
        
class ProjectUpdateForm(ModelForm):
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'hidden': True}), required=False, label='설명')
    
    class Meta:            
        model = Project
        fields = ['title', 'image', 'address', 'hide']
    