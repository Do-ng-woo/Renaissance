from django.forms import ModelForm
from articleapp.models import Article
from projectapp.models import Project
from artistapp.models import Artist
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'

class ArticleCreationForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'editable text-start','style':'height:auto'}))
    
    project = forms.ModelChoiceField(queryset=Project.objects.all(),required=False)
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(),required=False)
    class Meta:
        model = Article
        fields = ['title', 'image', 'project','artist','content','date']
        widgets = {
            'date' : DateInput(), 
            'time' : TimeInput()
        }