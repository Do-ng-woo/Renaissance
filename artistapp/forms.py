from django.forms import ModelForm
from artistapp.models import Artist


class ArtistCreationForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['title', 'image', 'description']