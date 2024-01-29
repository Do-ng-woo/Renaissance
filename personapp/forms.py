# forms.py
from django import forms
from django.forms import ModelForm, Textarea
from personapp.models import Person, Subtitle

class PersonCreationForm(ModelForm):
    class Meta:
        model = Person
        fields = ['title', 'image','position','hide']
        
class PersonCreationForm(forms.ModelForm):
    sub_titles_input = forms.CharField(max_length=100, required=False, label='부제목(쉼표로 구분)')

    class Meta:
        model = Person
        fields = ['title', 'image','position','hide']

    def clean_sub_titles_input(self):
        sub_titles_input = self.cleaned_data.get('sub_titles_input')
        if sub_titles_input:
            sub_titles_list = [sub_title.strip() for sub_title in sub_titles_input.split(',')]
            return sub_titles_list
        else:
            return []

    def save(self, commit=True):
        person = super().save(commit=False)

        # Many-to-Many 필드를 처리하기 전에 먼저 Person 인스턴스를 저장합니다.
        person.save()

        # sub_titles_input 처리
        if self.cleaned_data.get('sub_titles_input'):
            sub_titles_list = self.cleaned_data['sub_titles_input']
            person.sub_titles.clear()  # 기존 부제목 클리어
            for sub_title_name in sub_titles_list:
                subtitle, created = Subtitle.objects.get_or_create(name=sub_title_name)
                person.sub_titles.add(subtitle)

        return person

class PersonUpdateForm(ModelForm):
    sub_titles_input = forms.CharField(max_length=100, required=False, label='부제목 (쉼표로 구분)')
    descriptions = forms.CharField(widget=forms.Textarea(attrs={'hidden': True}), required=False, label='설명')

    class Meta:            
        model = Person
        fields = ['title', 'image','position', 'hide']

    def clean_sub_titles_input(self):
        sub_titles_input = self.cleaned_data.get('sub_titles_input')
        if sub_titles_input:
            sub_titles_list = [sub_title.strip() for sub_title in sub_titles_input.split(',')]
            return sub_titles_list
        else:
            return []

    def save(self, commit=True):
        person = super().save(commit=False)

        # 기존 부제목을 클리어하고 새로운 부제목을 추가합니다.
        if self.cleaned_data.get('sub_titles_input', None):
            person.sub_titles.clear()
            for sub_title_name in self.cleaned_data.get('sub_titles_input', []):
                subtitle, created = Subtitle.objects.get_or_create(name=sub_title_name)
                person.sub_titles.add(subtitle)

        
        if commit:
            person.save()

        return person
