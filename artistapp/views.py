from django.shortcuts import render
from django.db.models import Q

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.views.generic.list import MultipleObjectMixin
from artistapp.decorators import artist_ownership_required


from artistapp.forms import ArtistCreationForm, ArtistUpdateForm
from artistapp.models import Artist,Subtitle,Description
from articleapp.models import Article
from personapp.models import Person

from subscribeapp.models import A_Subscription

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import json
from django.core.serializers import serialize
from django.db import transaction
import uuid


# Create your views here.
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistCreationForm
    template_name = 'artistapp/create.html'
    
    def form_valid(self, form):
        temp_artist = form.save(commit=False)
        temp_artist.writer = self.request.user
        temp_artist.save()

        self._save_descriptions(temp_artist)
        self._save_persons(temp_artist)
        self._save_text_persons(temp_artist)  # 직접 입력한 멤버 정보 저장

        return super().form_valid(form)

    def _save_descriptions(self, artist):
        descriptions_data = {}
        for key, value in self.request.POST.items():
            if 'detailed_descriptions' in key:
                index = key.split('[')[1].split(']')[0]
                field_type = key.split('[')[2].split(']')[0]

                if index not in descriptions_data:
                    descriptions_data[index] = {'name': '', 'text': ''}

                if field_type == 'name':
                    descriptions_data[index]['name'] = value
                elif field_type == 'value':
                    descriptions_data[index]['text'] = value

        for desc in descriptions_data.values():
            Description.objects.create(artist=artist, name=desc['name'], text=desc['text'])

    def _save_persons(self, artist):
        memberCounter = 0
        while True:
            selection_method_key = f'selection_method_{memberCounter}'
            if selection_method_key not in self.request.POST:
                break

            selection_method = self.request.POST[selection_method_key]
            if selection_method == 'load':
                person_id = self.request.POST.get(f'person_id_{memberCounter}', '')
                if person_id:
                    person = Person.objects.get(id=person_id)
                    artist.person.add(person)
            # 여기서 "직접 입력하기"에 대한 추가적인 처리를 할 수 있습니다.
            # 예: 직접 입력된 데이터를 다른 필드나 모델에 저장
            memberCounter += 1
    
    def _save_text_persons(self, artist):
        text_person_data = []
        memberCounter = 0
        while True:
            selection_method_key = f'selection_method_{memberCounter}'
            if selection_method_key not in self.request.POST:
                break

            selection_method = self.request.POST[selection_method_key]
            if selection_method == 'manual_entry':
                name = self.request.POST.get(f'manual_name_{memberCounter}', '')
                position = self.request.POST.get(f'manual_position_{memberCounter}', '')
                if name and position:
                    member_info = f'{position}: {name}'  # 문자열로 포맷
                    text_person_data.append(member_info)
            memberCounter += 1

        if text_person_data:
            artist.text_person = text_person_data  # 리스트를 저장
            artist.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persons'] = Person.objects.all()
        context['positions'] = Person.POSITION_CHOICES
        return context

    def get_success_url(self):
        return reverse('artistapp:detail', kwargs={'pk': self.object.pk})

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
        object_list = Article.objects.filter(artist=self.get_object(), hide=False)
        return super(ArtistDetailView,self).get_context_data(object_list=object_list, subscription=subscription,**kwargs)
    
class ArtistListView(ListView):
    model = Artist
    context_object_name = 'artist_list'
    template_name = 'artistapp/list.html'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Artist.objects.filter(hide=False)

        # 검색어가 있는 경우, 제목에서 검색
        search_keyword = self.request.GET.get('search_keyword', None)

        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

        return queryset
    
@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArtistDeleteView(DeleteView):
    model = Artist
    context_object_name='target_artist'
    success_url = reverse_lazy('artistapp:list')
    template_name = 'artistapp/delete.html' 
    
    
@method_decorator(artist_ownership_required, 'get')
@method_decorator(artist_ownership_required, 'post')
class ArtistUpdateView(UpdateView):
    model = Artist
    form_class = ArtistUpdateForm
    context_object_name = 'target_artist'
    template_name = 'artistapp/update.html'
    
    def get(self, request, *args, **kwargs): #subtitle 기존에 입력된것 나타나게 하기
        self.object = self.get_object()
        form = self.get_form()

        # 여기서 기존 데이터를 폼에 채워 넣음
        form.fields['sub_titles_input'].initial = ', '.join(self.object.sub_titles.values_list('name', flat=True))

        return self.render_to_response(self.get_context_data(form=form))


       
    def form_valid(self, form):
        with transaction.atomic():  # 데이터 처리를 트랜잭션으로 묶음
            # Artist 객체 저장
            artist = form.save(commit=False)
            artist.save()

            # 기존 설명 업데이트
            existing_descriptions = {desc.id: desc for desc in artist.detailed_descriptions.all()}
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
                    existing_description = existing_descriptions[int(description_id)]
                    existing_description.name = desc['name']
                    existing_description.text = desc['text']
                    existing_description.save()
                    del existing_descriptions[int(description_id)]
                else:
                    Description.objects.create(artist=artist, name=desc['name'], text=desc['text'])

            # 삭제되지 않은 기존 설명 삭제
            for remaining_desc in existing_descriptions.values():
                remaining_desc.delete()

            # Person 및 TextPerson 데이터 처리
            self.update_persons(artist)

        return super().form_valid(form)
    
    
    def update_persons(self, artist):
        # JSON 문자열을 안전하게 파싱하는 함수
        def safe_json_loads(s):
            try:
                return json.loads(s) if s else []
            except json.JSONDecodeError:
                return []

        final_person_ids = self.request.POST.get('final_persons', '[]')
        if final_person_ids:
            final_person_ids = json.loads(final_person_ids)

        # text_person JSON 데이터 파싱 및 변환
        final_text_persons_str = safe_json_loads(self.request.POST.get('final_text_persons', ''))
        final_text_persons_converted = []

        for item in final_text_persons_str:
            if isinstance(item, str) and ':' in item:
                final_text_persons_converted.append(item.strip())
            else:
                # 형식이 맞지 않는 경우 예외 처리
                # 이 부분은 상황에 따라 적절히 처리해야 합니다.
                pass

        # Person 필드 업데이트
        artist.person.set(final_person_ids)

        # text_person JSON 필드 업데이트
        artist.text_person = final_text_persons_converted
        artist.save()

            
    def get_context_data(self, **kwargs):
        context = super(ArtistUpdateView, self).get_context_data(**kwargs)

        # 기존 context 설정 코드 유지
        if self.request.POST:
            context['detailed_descriptions'] = self.request.POST.getlist('detailed_descriptions')
        else:
            context['detailed_descriptions'] = [desc.text for desc in self.object.detailed_descriptions.all()]
        
        # 이미 입력한 불러오기를 통한 멤버와 포지션 정보 불러오기
        persons_with_positions = [
            {
                'person_id': person.id,
                'position': person.position,
                'name': person.title,  # 또는 다른 필요한 정보
            }
            for person in self.object.person.all()
        ]
        context['persons_with_positions'] = persons_with_positions
        #이미 입력한 직접 입력하기를 통한 멤버와 포지션 정보 불러오기
        # "직접 입력하기" 데이터를 포지션과 이름으로 나누기
        text_persons_data = []
        for text_person in self.object.text_person:  # 가정: text_persons는 문자열 목록
            parts = text_person.split(':')
            if len(parts) == 2:
                text_persons_data.append({'position': parts[0], 'name': parts[1]})
            else:
                text_persons_data.append({'position': '', 'name': text_person})

        context['text_persons_data'] = text_persons_data

        context['persons'] = Person.objects.all()
        context['positions'] = Person.POSITION_CHOICES
                
        return context

    def get_success_url(self):
        return reverse('artistapp:detail', kwargs={'pk': self.object.pk})
    
    
@login_required
@require_POST
def delete_description(request):
    description_id = request.POST.get('id')
    try:
        description = Description.objects.get(id=description_id)
        if description.artist.writer == request.user:  # 작성자 확인
            description.delete()
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'}, status=403)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': '설명이 존재하지 않습니다.'}, status=404)
    



