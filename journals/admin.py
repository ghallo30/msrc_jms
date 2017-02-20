from django.contrib import admin

from employee.models import User
from .models import Journal, JMSTemplate, JMSMessage
# Register your models here.


class JMSTemplateAdmin(admin.ModelAdmin):
    
    list_display = ('template_title','date_created', 'creator')

admin.site.register(JMSTemplate, JMSTemplateAdmin)
admin.site.register(JMSMessage)