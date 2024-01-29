from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from articleapp.decorators import article_ownership_required
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.views.generic.edit import FormMixin

from commentapp.forms import CommentCreationForm
from articleapp.forms import ArticleCreationForm
from articleapp.forms import ArticleSearchForm

from articleapp.models import Article
from django.urls import reverse, reverse_lazy

# Create your views here.
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreationForm
    template_name = 'articleapp/create.html'
    
    
    def form_valid(self,form):
        temp_article = form.save(commit=False)
        temp_article.writer = self.request.user
        temp_article.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk':self.object.pk})
    
    

class ArticleDetailView(DetailView, FormMixin):
    model = Article
    form_class = CommentCreationForm
    context_object_name = 'target_article'
    template_name ='articleapp/detail.html'

@method_decorator(article_ownership_required, 'get')
@method_decorator(article_ownership_required, 'post')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleCreationForm
    context_object_name= 'target_article'
    template_name = 'articleapp/update.html'
        
    def get_success_url(self):
        return reverse('articleapp:detail', kwargs={'pk':self.object.pk})

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleDeleteView(DeleteView):
    model = Article
    context_object_name= 'target_article'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'articleapp/delete.html' 

from django.db.models import Q
from datetime import datetime

class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articleapp/list.html'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Article.objects.filter(hide=False)
        search_keyword = self.request.GET.get('search_keyword', '')
        search_field = self.request.GET.get('search_field', '')
        date_range = self.request.GET.get('date_range', '')

        if search_field == 'title' and search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)
        elif search_field == 'date':
            if date_range and ' ~ ' in date_range:
                # 날짜 범위를 '-'로 분리
                start_date_str, end_date_str = date_range.split(' ~ ')
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                # date 및 datetime 필드에서 날짜 범위로 검색
                queryset = queryset.filter(
                    Q(date__range=(start_date, end_date)) |
                    Q(datetime__date__range=(start_date, end_date))
                )
            elif search_keyword:
                # 날짜 검색어가 있을 경우 이전 로직 유지
                queryset = queryset.filter(
                    Q(date__icontains=search_keyword) |
                    Q(datetime__date__icontains=search_keyword)
                )
        elif search_field == 'project' and search_keyword:
            queryset = queryset.filter(project__title__icontains=search_keyword)
        elif search_field == 'artist' and search_keyword:
            queryset = queryset.filter(artist__name__icontains=search_keyword)

        return queryset

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ArticleSearchForm(self.request.GET or None)
        context['search_field'] = self.request.GET.get('search_field', 'title')  # 검색 필드 추가
        return context
    

    
    
