from django.shortcuts import render
from django.db.models import Q

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.views.generic.list import MultipleObjectMixin
from personapp.decorators import person_ownership_required


from personapp.forms import PersonCreationForm, PersonUpdateForm
from personapp.models import Person,Subtitle,Description
from articleapp.models import Article
from subscribeapp.models import Per_Subscription

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class PersonCreateView(CreateView):
    model = Person
    form_class = PersonCreationForm
    template_name = 'person/create.html'
    
    def form_valid(self, form):
        temp_person = form.save(commit=False)
        temp_person.writer = self.request.user
        temp_person.save()

        descriptions = {}
        for key, value in self.request.POST.items():
            if 'detailed_descriptions' in key:
                index = key.split('[')[1].split(']')[0]
                field_type = key.split('[')[2].split(']')[0]

                if index not in descriptions:
                    descriptions[index] = {'name': '', 'text': ''}
                
                if field_type == 'name':
                    descriptions[index]['name'] = value
                elif field_type == 'value':
                    descriptions[index]['text'] = value

        for desc in descriptions.values():
            Description.objects.create(person=temp_person, name=desc['name'], text=desc['text'])

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('personapp:detail', kwargs={'pk':self.object.pk})

class PersonDetailView(DetailView, MultipleObjectMixin):
    model = Person
    context_object_name = 'target_person'
    template_name ='personapp/detail.html'
    
    paginate_by=25
    
    def get_context_data(self, **kwargs):
        person = self.object
        user = self.request.user
        
        if user.is_authenticated:
            subscription = Per_Subscription.objects.filter(user=user, person=person)
        else:
            subscription = None
        object_list = Article.objects.filter(person=self.get_object(), hide=False)
        return super(PersonDetailView,self).get_context_data(object_list=object_list, subscription=subscription,**kwargs)
    
class PersonListView(ListView):
    model = Person
    context_object_name = 'person_list'
    template_name = 'personapp/list.html'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Person.objects.filter(hide=False)

        # 검색어가 있는 경우, 제목에서 검색
        search_keyword = self.request.GET.get('search_keyword', None)

        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

        return queryset
    
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class PersonDeleteView(DeleteView):
    model = Person
    context_object_name='target_person'
    success_url = reverse_lazy('personapp:list')
    template_name = 'personapp/delete.html' 
    
@method_decorator(person_ownership_required, 'get')
@method_decorator(person_ownership_required, 'post')
class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonUpdateForm
    context_object_name = 'target_person'
    template_name = 'personapp/update.html'
    
    def get(self, request, *args, **kwargs): #subtitle 기존에 입력된것 나타나게 하기
        self.object = self.get_object()
        form = self.get_form()

        # 여기서 기존 데이터를 폼에 채워 넣음
        form.fields['sub_titles_input'].initial = ', '.join(self.object.sub_titles.values_list('name', flat=True))

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(PersonUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['detailed_descriptions'] = self.request.POST.getlist('detailed_descriptions')
        else:
            context['detailed_descriptions'] = [desc.text for desc in self.object.detailed_descriptions.all()]
        return context

    def form_valid(self, form):
        temp_person = form.save(commit=False)
        temp_person.save()

        # 기존 설명 업데이트
        existing_descriptions = {desc.id: desc for desc in temp_person.detailed_descriptions.all()}
        descriptions_data = {}
        for key, value in self.request.POST.items():
            if 'detailed_descriptions' in key:
                index = key.split('[')[1].split(']')[0]
                field_type = key.split('[')[2].split(']')[0]

                # 데이터 구조 준비
                if index not in descriptions_data:
                    descriptions_data[index] = {'id': None, 'name': '', 'text': ''}

                # 데이터 추출
                if field_type == 'id':
                    descriptions_data[index]['id'] = value
                elif field_type == 'name':
                    descriptions_data[index]['name'] = value
                elif field_type == 'value':
                    descriptions_data[index]['text'] = value

        # 데이터 저장 및 업데이트
        for desc in descriptions_data.values():
            description_id = desc.get('id')
            if description_id and int(description_id) in existing_descriptions:
                # 기존 설명 업데이트
                existing_description = existing_descriptions[int(description_id)]
                existing_description.name = desc['name']
                existing_description.text = desc['text']
                existing_description.save()
                del existing_descriptions[int(description_id)]
            else:
                # 새로운 설명 추가
                Description.objects.create(person=temp_person, name=desc['name'], text=desc['text'])

        # 삭제되지 않은 기존 설명 삭제
        for remaining_desc in existing_descriptions.values():
            remaining_desc.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('personapp:detail', kwargs={'pk': self.object.pk})
    
@login_required
@require_POST
def delete_description(request):
    description_id = request.POST.get('id')
    try:
        description = Description.objects.get(id=description_id)
        if description.person.writer == request.user:  # 작성자 확인
            description.delete()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'}, status=403)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': '설명이 존재하지 않습니다.'}, status=404)
    



