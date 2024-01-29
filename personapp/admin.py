from django.contrib import admin

# Register your models here.
from personapp.models import Person
from personapp.models import Subtitle

class PersonAdmin(admin.ModelAdmin):
    
    actions = ['make_hidden', 'make_not_hidden']

    def make_hidden(self, request, queryset):
        queryset.update(hide=True)
    make_hidden.short_description = "Mark selected articles as hidden"

    def make_not_hidden(self, request, queryset):
        queryset.update(hide=False)
    make_not_hidden.short_description = "Mark selected articles as not hidden"

admin.site.register(Person, PersonAdmin)

class SubtitleAdmin(admin.ModelAdmin):
    actions = ['delete_selected_subtitles']

    def delete_selected_subtitles(self, request, queryset):
        queryset.delete()
    delete_selected_subtitles.short_description = "Delete selected subtitles"

admin.site.register(Subtitle, SubtitleAdmin)
