from artistapp.views import ArtistListView, ArtistCreateView, ArtistDetailView, ArtistDeleteView, ArtistUpdateView, delete_description
from django.urls import path, include

app_name = 'artistapp'

urlpatterns = [
    path('list/', ArtistListView.as_view(template_name='artistapp/list.html'), name='list'),
    path('create/', ArtistCreateView.as_view(template_name='artistapp/create.html'), name='create'),
    path('detail/<int:pk>', ArtistDetailView.as_view(template_name='artistapp/detail.html'), name='detail'),
    path('delete/<int:pk>', ArtistDeleteView.as_view(template_name='artistapp/delete.html'), name='delete'),
    path('update/<int:pk>', ArtistUpdateView.as_view(template_name='artistapp/update.html'), name='update'),
    path('delete_description/', delete_description, name='delete_description'),
    
]