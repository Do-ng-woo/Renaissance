from django.contrib import admin

from projectapp.models import Project
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    
    actions = ['make_hidden', 'make_not_hidden']

    def make_hidden(self, request, queryset):
        queryset.update(hide=True)
    make_hidden.short_description = "Mark selected articles as hidden"

    def make_not_hidden(self, request, queryset):
        queryset.update(hide=False)
    make_not_hidden.short_description = "Mark selected articles as not hidden"

admin.site.register(Project, ProjectAdmin)
