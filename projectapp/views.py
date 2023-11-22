from django.shortcuts import render

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.views.generic.list import MultipleObjectMixin


from projectapp.forms import ProjectCreationForm
from projectapp.models import Project
from articleapp.models import Article
from subscribeapp.models import P_Subscription


# Create your views here.
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'projectapp/create.html'
    
    def get_success_url(self):
        return reverse('projectapp:detail', kwargs={'pk':self.object.pk})

class ProjectDetailView(DetailView, MultipleObjectMixin):
    model = Project
    context_object_name = 'target_project'
    template_name ='projectapp/detail.html'
    
    paginate_by=25
    
    def get_context_data(self, **kwargs):
        project = self.object
        user = self.request.user
        
        if user.is_authenticated:
            subscription = P_Subscription.objects.filter(user=user, project=project)
        else:
            subscription = None
        object_list = Article.objects.filter(project=self.get_object())
        return super(ProjectDetailView,self).get_context_data(object_list=object_list, subscription=subscription,**kwargs)
    
class ProjectListView(ListView):
    model= Project
    context_object_name = 'project_list'
    template_name = 'projectapp/list.html'
    paginate_by = 25
    
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ProjectDeleteView(DeleteView):
    model = Project
    context_object_name='target_project'
    success_url = reverse_lazy('projectapp:list')
    template_name = 'projectapp/delete.html' 