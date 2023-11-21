from artistapp.views import ArtistListView, ArtistCreateView, ArtistDetailView
from django.urls import path, include

app_name = 'artistapp'

urlpatterns = [
    path('list/', ArtistListView.as_view(template_name='artistapp/list.html'), name='list'),
    path('create/', ArtistCreateView.as_view(template_name='artistapp/create.html'), name='create'),
    path('detail/<int:pk>', ArtistDetailView.as_view(template_name='artistapp/detail.html'), name='detail'),
    
]