from django import template
from tools.tools import (
	encrypt_text, 
	hasAssignedEditor, 
	allArticleReviewDone,
	hasAssignedReviewer,
	allArticleCount,
	is_article_author,
	article_decided
)

#, allArticleReviewDone
from django.contrib.auth.models import Group 
from employee.models import User

register = template.Library()


@register.filter(is_safe=True)
def encrypts(value, args):
	if args == 'encrypt':
		encrypted = encrypt_text(str(value))
		return encrypted
	return value

@register.filter(is_safe=True)
def hasArticle_decision(value, args):
	print('--asdasd--checking article decision ')
	return article_decided(value)

@register.filter(is_safe=True)
def is_submission_author(value, args):
	return is_article_author(value,args)

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()

@register.filter(is_safe=True)
def num_submission(value, args):
	return allArticleCount(value, args)

#check if article has assigned editor
@register.filter(is_safe=True)
def hasEditorAssigned(value, args):
	return hasAssignedEditor(value, args)

#check if article has assigned reviewer
@register.filter(is_safe=True)
def hasRevAssigned(value, args):
	return hasAssignedReviewer(value, args)

#check if all reviews is done on a article
@register.filter(is_safe=True)
def allReviewDone(value, args):	
	return allArticleReviewDone(value)
	
# @register.filter(is_safe=True)
# def checkifadmit(value, args):

# 	if args == 'case_number':
# 		return Admission.objects.filter(case_number=value).exists()
# 	elif args == 'patient':
# 		print (args, value, 'jajaja')
# 		print (Admission.objects.filter(patient_id=value, is_discharges=False, patient_type='IP').exists())
# 		return Admission.objects.filter(patient_id=value, is_discharges=False, patient_type='IP').exists()
# 	elif args == 'admission':
# 		return Admission.objects.filter(patient_id=value, is_discharges=False).exists()
# 	elif args == 'admission':
# 		return Admission.objects.filter(patient_id=value, is_discharges=False).exists()
# 	elif args == 'admission_id':
# 		try:
# 			return Admission.objects.get(patient_id=value, is_discharges=False).id
# 		except :
# 			return False