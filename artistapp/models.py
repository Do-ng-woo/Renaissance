from django.db import models
from personapp.models import Person
from django.contrib.auth.models import User

class Subtitle(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.name
    
class CustomArtistManager(models.Manager):
    def get_or_create_artist_by_subtitles(self, title, subtitles, defaults=None, **extra_fields):
        defaults = defaults or {}
        defaults.update(extra_fields)

        normalized_subtitles = set(subtitle.strip().lower() for subtitle in subtitles)

        all_subtitles = []
        for subtitle_name in normalized_subtitles:
            subtitle, created = Subtitle.objects.get_or_create(name=subtitle_name)
            all_subtitles.append(subtitle)

        artist = self.filter(title__iexact=title.strip()).first()
        if not artist:
            artist = self.filter(sub_titles__name__in=normalized_subtitles).distinct().first()

        if artist:
            return artist, False

        artist = self.create(title=title.strip(), **defaults)
        artist.sub_titles.set(all_subtitles)
        return artist, True

class Artist(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='artist', null=True)
    title = models.CharField(max_length=20, null=False)
    sub_titles = models.ManyToManyField('Subtitle', related_name='artists', blank=True)
    image = models.ImageField(upload_to='artist/', null=False)
    description = models.CharField(max_length=200, null=True)
    person = models.ManyToManyField(Person, related_name='artist', blank=True)
    text_person = models.JSONField(default=list)  # JSON 필드로 변경

    created_at = models.DateField(auto_now_add=True, null=True)
    hide = models.BooleanField(default=True)  # 임시저장 여부를 나타내는 필드
    objects = CustomArtistManager()
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['title']
        
        
class Description(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='detailed_descriptions')
    name = models.CharField(max_length=100, default="정보")  # 정보의 이름을 위한 필드
    text = models.TextField()

    def __str__(self):
        return f"{self.name}: {self.text}"