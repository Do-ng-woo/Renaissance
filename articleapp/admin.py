from django.contrib import admin

from articleapp.models import Article
# Register your models here.
# admin.py

class ArticleAdmin(admin.ModelAdmin):
    
    actions = ['make_hidden', 'make_not_hidden']

    def make_hidden(self, request, queryset):
        queryset.update(hide=True)
    make_hidden.short_description = "Mark selected articles as hidden"

    def make_not_hidden(self, request, queryset):
        queryset.update(hide=False)
    make_not_hidden.short_description = "Mark selected articles as not hidden"

admin.site.register(Article, ArticleAdmin)
