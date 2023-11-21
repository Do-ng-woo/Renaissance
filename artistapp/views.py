from django.shortcuts import render

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.list import MultipleObjectMixin


from artistapp.forms import ArtistCreationForm
from artistapp.models import Artist
from articleapp.models import Article
from subscribeapp.models import A_Subscription


# Create your views here.
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistCreationForm
    template_name = 'artist/create.html'
    
    def get_success_url(self):
        return reverse('artistapp:detail', kwargs={'pk':self.object.pk})

class ArtistDetailView(DetailView, MultipleObjectMixin):
    model = Artist
    context_object_name = 'target_artist'
    template_name ='artistapp/detail.html'
    
    paginate_by=25
    
    def get_context_data(self, **kwargs):
        artist = self.object
        user = self.request.user
        
        if user.is_authenticated:
            subscription = A_Subscription.objects.filter(user=user, artist=artist)
        else:
            subscription = None
        object_list = Article.objects.filter(artist=self.get_object())
        return super(ArtistDetailView,self).get_context_data(object_list=object_list, subscription=subscription,**kwargs)
    
class ArtistListView(ListView):
    model= Artist
    context_object_name = 'artist_list'
    template_name = 'artistapp/list.html'
    paginate_by = 25