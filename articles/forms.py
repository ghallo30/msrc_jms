import re
from django import forms
from .models import Section, Article, Copyright, ArticleFile, ArticleAuthor
from journals.models import Journal
from issues.models import Issue,IssueGroup,IssueEditorialBoard

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

'''added Section choice fields in article forms, to import Section in articles'''
class SectionChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.cat_name)

'''added Issue choice fields in article forms, to import issues in articles'''
class IssueChoiceField(forms.ModelChoiceField):
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

class ArticleForm(forms.Form):
	# likes = models.IntegerField(default=0)

	section = SectionChoiceField(required=False, queryset = Section.objects.order_by('id') ,
			widget = forms.Select(attrs = {
					'class':'form-control input-md',
					'id' : 'section'
				})
	)

	abstract = forms.CharField(
		widget = forms.Textarea(
			attrs = {
				'placeholder' : 'Write your abstract here...',
				'class'       : 'ckeditor',
				'id' 		 : 'abstract',
			})
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

	subtitle   = forms.CharField(required=False,
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Subtitle',
				'class'       : 'form-control',
				'id'		  : 'subtitle',
			}
		),
	)

	# cover_letter = 				models.CharField(max_length=500, null = True)
	references =  forms.CharField(required=False,
		widget = forms.Textarea(
			attrs = {
				'placeholder' : 'References',
				'class'       : 'form-control',
				'id' 		 : 'references'
			}
		),
	)

	keywords = forms.CharField(required=False,
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'keywords',
				'class'       : 'form-control',
				'id'		  : 'keywords',
				'required'    : 'True',
				'type'		  : 'text',
			}
		),
	)

	journal = JournalChoiceField(required=False, queryset = Journal.objects.order_by('title') ,
			widget = forms.Select(attrs = {
					'class':'form-control input-md',
					# 'required': 'True',
					'id' : 'journal'
				})
	)

	copyright   = CopyrightChoiceField(required=False, queryset = Copyright.objects.order_by('cr_name') ,
			widget = forms.Select(attrs = {
					'class':'form-control input-md',
					'required': 'False',
					'id' : 'copyright'
				})
	)

	main_file  = forms.FileField(required=False)

	# # is_featured =				models.BooleanField(default=False)
	# editor_comment = forms.CharField(required=False,
	# 	widget = forms.Textarea(
	# 	attrs = {
	# 		'placeholder' : 'Editor comment here...',
	# 		'class'       : 'form-control',
	# 		'id' 		 : 'editor_comment',
	# 		'style': 'height: 180px; width: 455px; max-height: 180px;min-width: 455px; max-width: 455px'
	# 	})
	# )

	# article_version =			models.CharField(max_length=300, null = True)
	def clean(self):
		cleaned_data = self.cleaned_data
		references = cleaned_data.get('references')
		references = re.sub(' +', ' ', references)
		# references = re.sub('\n+', '\n', references)
		cleaned_data['references'] = references



class IssueForm(forms.Form):

	title = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Title',
				'class'       : 'form-control',
				'id' 		 : 'title',
			})
	)
	
	description = forms.CharField(required=False,
		widget = forms.Textarea(
			attrs = {
				'placeholder' : 'Issue description',
				'class'       : 'ckeditor',
				'id'		  : 'description',
			}
		),
	)

	issue_volume   = forms.CharField(required=False,
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Volume',
				'class'       : 'form-control',
				'id'		  : 'issue_volume',
			}
		),
	)

	issue_year   = forms.CharField(required=False,
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Year',
				'class'       : 'form-control',
				'id'		  : 'issue_year',
			}
		),
	)

	issue_number =  forms.CharField(required=False,
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Number',
				'class'       : 'form-control',
				'id' 		 : 'issue_number'
			}
		),
	)

	printIssn =  forms.CharField(required=False,
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'ISSn',
				'class'       : 'form-control',
				'id' 		 : 'printIssn'
			}
		),
	)

	cover_photo  = forms.FileField(required=False)
	
	# cover_photo_desc = forms.CharField(required=False,
	# 	widget = forms.Textarea(
	# 		attrs = {
	# 			'placeholder' : 'Cover Photo description',
	# 			'class'       : 'ckeditor',
	# 			'id'		  : 'cover_photo_desc',
	# 		}
	# 	),
	# )

    # special_issue =     models.BooleanField(default = False)

	# cover_letter = 				models.CharField(max_length=500, null = True)
	

	def clean(self):
		cleaned_data = self.cleaned_data
		description = cleaned_data.get('description')
		description = re.sub(' +', ' ', description)
		cleaned_data['description'] = description
