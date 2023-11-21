from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, ListView
from django.shortcuts import get_object_or_404

from subscribeapp.models import P_Subscription, A_Subscription
from projectapp.models import Project
from artistapp.models import Artist
from articleapp.models import Article



@method_decorator(login_required,'get')
class P_SubscriptionView(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('projectapp:detail', kwargs={'pk':self.request.GET.get('project_pk')})
    
    def get(self,request,*args,**kwargs):
        project = get_object_or_404(Project, pk=self.request.GET.get('project_pk'))
        user = self.request.user
        subscription = P_Subscription.objects.filter(user=user, project=project)
        
        if subscription.exists():
            subscription.delete()
        else:
            P_Subscription(user=user,project=project).save()
        return super(P_SubscriptionView,self).get(request, *args, **kwargs)

@method_decorator(login_required,'get')
class P_SubscriptionListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'subscribeapp/P_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        projects = P_Subscription.objects.filter(user=self.request.user).values_list('project')
        article_list = Article.objects.filter(project__in=projects)
        return article_list
    

@method_decorator(login_required,'get')
class A_SubscriptionView(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('artistapp:detail', kwargs={'pk':self.request.GET.get('artist_pk')})
    
    def get(self,request,*args,**kwargs):
        artist = get_object_or_404(Artist, pk=self.request.GET.get('artist_pk'))
        user = self.request.user
        subscription = A_Subscription.objects.filter(user=user, artist=artist)
        
        if subscription.exists():
            subscription.delete()
        else:
            A_Subscription(user=user,artist=artist).save()
        return super(A_SubscriptionView,self).get(request, *args, **kwargs)

@method_decorator(login_required,'get')
class A_SubscriptionListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'subscribeapp/A_list.html'
    paginate_by = 5
    
    def get_queryset(self):
        artists = A_Subscription.objects.filter(user=self.request.user).values_list('artist')
        article_list = Article.objects.filter(artist__in=artists)
        return article_list