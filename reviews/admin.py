from django.contrib import admin

from articles.models import Section,Article, ArticleFile, Copyright, ArticleAuthor
from employee.models import User
from journals.models import Journal, JMSTemplate, JMSMessage
from .models import ReviewDetails, ReviewerElement, ReviewerResponse, ReviewForm, EditorDecision
# Register your models here.



class ReviewDetailsAdmin(admin.ModelAdmin):
    
    list_display = ('reviewer', 'article', 'date_ended', 'date_submitted')

class EditorDecisionAdmin(admin.ModelAdmin):
    
    list_display = ('editor', 'article', 'date_decided', 'decision')





admin.site.register(ReviewDetails, ReviewDetailsAdmin)

admin.site.register(EditorDecision, EditorDecisionAdmin)
