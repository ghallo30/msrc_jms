
import random
import string

import json
import time
import os
import re


from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.models import PermissionsMixin, Group

from reviews.models import ReviewDetails, EditorDecision,AssignEditor
from articles.models import  Section, Article, ArticleFile, Copyright, ArticleAuthor


def convert_to_text():
	print('convert_to_text')
	# Open a PDF document.
	# pdf_file = open('d:/project/jms/tools/sample (2).pdf', 'rb')
	# read_pdf = PyPDF2.PdfFileReader(pdf_file)
	# number_of_pages = read_pdf.getNumPages()
	#page = read_pdf.getPage(0)
	# page_content =""

	# page_content = "\n".join(page.extractText().strip() for page in read_pdf.pages)
	# page_content = ' '.join(page_content.split())

	# print (page_content,'--- #page1')
	return True



def hasAssignedEditor(assoc_info, attr):
	if attr=='article':
		return AssignEditor.objects.filter(article=assoc_info, is_accepted=True, is_active=True).exists()
	else:
		return AssignEditor.objects.filter(assoc_editor=assoc_info, is_accepted=True, is_active=True).count()

def is_article_author(art_info, attr):
	print(art_info.id,'-------',attr)
	return ArticleAuthor.objects.filter(article=art_info, author__id=attr).exists()

def hasAssignedReviewer(assoc_info, attr):
	if attr=='article':
		return ReviewDetails.objects.filter(article=assoc_info, is_active=True, is_done=False ).exists()
	elif attr=='no_form':
		return ReviewDetails.objects.filter(article=assoc_info, is_active=True, review_form=None ).exists()
	else:
		#count number of reviewers
		return ReviewDetails.objects.filter(article=assoc_info, is_active=True ).count()

def allArticleCount(art_info, attr):
	revs=0
	if attr=='unassigned':
		revs = Article.objects.filter(is_submitted =True, state='ACC').exclude(id__in= ReviewDetails.objects.filter(is_active=True).values_list('article', flat=True)).count()
	elif attr=='on_review':
		revs=ReviewDetails.objects.filter( is_active= True, is_done = False ).count()
	elif attr=='on_edit':
		revs=Article.objects.filter(state='ED' ).count()
	elif attr=='publish':
		revs=Article.objects.filter(state='PUB' ).count()
	return revs

def allArticleReviewDone(art_info):

	revs=ReviewDetails.objects.filter(article=art_info, is_active=True ).count()
	done_rev=ReviewDetails.objects.filter(article=art_info, is_active=True, is_done=True).count()
	print(revs,'------',done_rev)
	if revs>0 and done_rev>0:
		if revs==done_rev:
			print('samesame')
			return True
	return False

def article_decided(art_info):
	print(EditorDecision.objects.filter(article=art_info, rounds=art_info.current_rounds, decided=True).exists(),' --decided')
	return EditorDecision.objects.filter(article=art_info, rounds=art_info.current_rounds, decided=True).exists()

def hasAccess(user, model_table):
	print (user,'hasAccess', user.groups.filter(name=model_table).exists(), model_table)	
	if user.is_superuser:
		return True
	else:
		return user.groups.filter(name=model_table).exists()

def encrypt_text(text):
	# url_new = EncodeAES(cipher,text)
	# url_new = url_new.decode('utf8')
	# print (quote_plus(url_new),'dawd  scs')
	# url_new = url_new.replace('/','_')
	# print (url_new)
	# return quote_plus(url_new)
	add_str =''
	numbers = {
		'1': 'is2e',
		'2': 'd4we',
		'3': '0d3e',
		'4': '0vhje',
		'5': 'ad3e',
		'6': '7zwe',
		'7': '932se',
		'8': '0dfge',
		'9': '3ffe',
		'0': '000re',
	}
	size = len(text)
	if size == 1:
		add_str = 'l2ase24dfedaw9euiseswqesdfeEaswe'
	elif size == 2:
		add_str = 'lAaae24dfe4K29eJisSswqesdfe'
	elif size == 3:
		add_str = 'lPaDe24Afedaw9euIseOwqe'
	elif size == 4:
		add_str = 'luSse24dFedaw9Vuise'
	elif size == 5:
		add_str = 'lA2asY24sfe2aw9'
	elif size == 6:
		add_str = 'ldfedaw9e' 
	elif size == 7:
		add_str = 'ldEre' 
	new_str = ''
	for x in text:
		new_str = new_str + numbers[str(x)]
	return new_str+add_str

def decrypt_text(text):
	numbers = {
		'is2': '1',
		'd4w' :'2',
		 '0d3':'3',
		'0vhj':'4',
		'ad3': '5',
		'7zw': '6' ,
		'932s': '7',
		'0dfg': '8',
		'3ff': '9',
		'000r': '0'
	}
	text=text.split('l')[0]
	size = (len(text.split('e')))
	new_str = ''
	count = 0
	for x in text.split('e'):
		count = count + 1
		if count == size:
			return new_str
		if numbers[x]!="" or  numbers[x]!='"':
			new_str = new_str + numbers[x]

	return new_str

def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])

# def check_casenumber_ifexist(casenumber):
# 	data={}
# 	pasyente=None
# 	# pasyente = get_patients(_id)
# 	if  Admission.objects.filter(case_number=casenumber,is_discharges=True).exists():
# 		add = Admission.objects.get(case_number=casenumber,is_discharges=True)
# 		data={
# 			'exist':'is_discharges',
# 			'date_discharges':add.date_discharge.strftime('%B')+" "+add.date_discharge.strftime('%d')+", "+add.date_discharge.strftime('%Y')+", Time "+add.date_discharge.strftime('%H')+":"+add.date_discharge.strftime('%M'),
# 			'patient_name':"Hospital ID: "+add.patient.patient_hospid+"    Name:"+str(add.patient.firstname+' '+add.patient.middlename+' '+add.patient.lastname).title()
# 		}
# 	else:
# 		try:
# 			pasyente = Admission.objects.filter(case_number=casenumber,is_discharges=False).exists()
			
# 		except Patient.DoesNotExist or Patient:
# 			pasyente = None

# 		if not pasyente:

# 			data={'exist':'no'}

# 		else:
# 			data={'exist':'yes'}
# 	if Admission.objects.filter(case_number=casenumber).exists():
# 			ad = Admission.objects.get(case_number=casenumber)
# 			data['patient_name']="Hospital ID: "+ad.patient.patient_hospid+"    Name: "+str(ad.patient.firstname+' '+ad.patient.middlename+' '+ad.patient.lastname).title()
	

	

# 	json_response = json.dumps(data)
# 	return HttpResponse(json_response, content_type="application/json")

# def check_name_ifexist(fname, lname, mname):
# 	data={}
# 	pasyente=None
# 	print (fname,lname,mname)
# 	try:
# 		pasyente = Patient.objects.filter(firstname__iexact=fname,lastname__iexact=lname,middlename__iexact=mname).exists()
		
# 	except Patient.DoesNotExist or Patient:
# 		pasyente = None
# 	if pasyente:
# 		data={'exist':'yes'}
# 	else:
# 		data={'exist':'no'}
	
	
# 	print (data)
# 	json_response = json.dumps(data)
# 	return HttpResponse(json_response, content_type="application/json")

def genSubmissionNumber():
	count =Articles.objects.filter(is_submitted=True).count()
	case_id = time.strftime("%y") +"-"+time.strftime("%m")+"-" + '%s' %str(count+400)
	return case_id

# def genHospitalId():
#     id = time.strftime("%Y") + '%s' %str(random.randint(1000, 9999))
#     return id

def genEmpUsername():
    id = time.strftime("%y") + '%s' %str(random.randint(1000, 9999))
    return id