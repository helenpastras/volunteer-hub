from django.contrib import admin

# Register your models here
from .models import Opportunity, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'location', 'get_tags', 'get_creator')  

    def get_creator(self, obj):
        return obj.created_by.username
    get_creator.short_description = 'Created By'

    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    get_tags.short_description = 'Tags'