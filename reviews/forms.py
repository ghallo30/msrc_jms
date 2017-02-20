
from django import forms

from articles.models import Section, Article, Copyright, ArticleFile, ArticleAuthor, ArticleFile

from .models import ReviewDetails, ReviewerElement, ReviewerResponse, ReviewForm

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

'''added Section choice fields in article forms, to import Section in articles'''
class SectionChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.cat_name)

'''added copyright choice fields in article forms, to import copyright in articles'''
class CopyrightChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return smart_text(obj.cr_name)


class Review_Submission_Form(forms.Form):
	# likes = models.IntegerField(default=0)
	RECOMMENDATION=(
				('A', 'Accept Submission'),
				('RV', 'Revision Required'),
				('D', 'Reject Submission'),
    )
	
	Q_CHOICES=(
				('Y', 'Yes'),
				('N', 'No'),
				('P', 'Partly'),
	)

	REV_CHOICES=(
				('E', 'Excellent'),
				('G', 'Good'),
				('F', 'Fair'),
				('P', 'Poor'),
	)

	AB_CHOICES=(
				('A', 'Adequate and Relevant'),
				('I', 'Inadequate and/or Irrelevant'),
	)

	comments_for_editor      = forms.CharField(
		widget = forms.Textarea(
			attrs = {
				'placeholder' : 'Write your comment for the editor here...',
				'class'       : 'ckeditor',
				'id' 		 : 'comments_for_editor',
			})
	)

	comments_for_author         = forms.CharField(
		widget = forms.Textarea(
			attrs = {
				'placeholder' : 'Write your comment for the author here...',
				'class'       : 'ckeditor',
				'id' 		 : 'comments_for_author',
			})
	)

		# form for selection boxes
	recommendation = forms.ChoiceField(required =False,choices = RECOMMENDATION,
		widget=forms.Select(attrs={
			'class' : 'input-lg',
	
		}),
    )

    
	acceptability = forms.ChoiceField(choices = Q_CHOICES,
		widget=forms.Select(attrs={
			'class' : 'input-lg',
			'required': 'True',
		}),
    )
    
	quality = forms.ChoiceField(choices = REV_CHOICES,
		widget=forms.Select(attrs={
			'class' : 'input-lg',
		}),
	)

	clarity = forms.ChoiceField(choices = REV_CHOICES,
		widget=forms.Select(attrs={
			'class' : 'input-lg',
		}),
	)

	abstract_review = forms.ChoiceField(choices = AB_CHOICES,
		widget=forms.Select(attrs={
			'class' : 'input-lg',
		}),
	)

	
	
