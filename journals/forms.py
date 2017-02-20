from django import forms
from articles.models import Section, Article, Copyright, ArticleFile, ArticleAuthor, ArticleFile
from journals.models import Journal, JMSTemplate, Announcement, JMSMessage
from issues.models import Issue

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

'''added section choice fields in article forms, to import section in articles'''
class IssueChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.title)

'''added section choice fields in article forms, to import section in articles'''
class SectionChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.cat_name)

'''added copyright choice fields in article forms, to import copyright in articles'''
class CopyrightChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.cr_name)

'''added journal choice fields in article forms, to import journal in articles'''
class JournalChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.title)

class JMSTemplateForm(forms.Form):
	# likes = models.IntegerField(default=0)
	TEMP_TYPE = (
		('EMAIL', 'E'),
		('NOTIFICATION', 'N'),
	)

	temp_type = forms.ChoiceField(required=False, 
		choices = TEMP_TYPE,
		widget=forms.Select(attrs={
			'class' : 'form-control',
			'required': 'True',
		}),
	)

	title = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Title',
				'class'       : 'form-control',
				'id'		  : 'title',
			}
		),
	)

	content = forms.CharField(
		widget = forms.Textarea(
			attrs = {
				'placeholder' : 'Write your abstract here...',
				'class'       : 'form-control',
				'id' 		 : 'abstract',
			})
	)
#  consultation fee choice field
class IssueSelectionForm(forms.Form):
	
	issue_select = IssueChoiceField(queryset = Issue.objects.order_by('title').filter(is_published=True),
		widget = forms.Select(attrs = {
					'class':'form-control input-md',
					'required': 'True',
					'id' : 'issue_select'
				})
	)

	# def __init__(self, eventUser, *args, **kwargs):
	# 	super(ConsultationFeeSelectionForm, self).__init__(*args, **kwargs)
	# 	self.fields['doc_consultation_fee'].queryset = ConsultationFee.objects.order_by('description').filter(professional_id = eventUser )
