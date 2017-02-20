import os
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_protect,csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,  user_passes_test

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection, transaction

from datetime import *

from tools.tools import decrypt_text, encrypt_text, hasAccess, genEmpUsername, create_random_string, genSubmissionNumber

# database
from django.db import transaction
from django.db.models import Q

# forms
from django.forms.models import model_to_dict
from .forms import ArticleForm
from employee.forms import Registration_Form, Author_Form

# models
from .models import Article, ArticleFile, Copyright, ArticleAuthor
from employee.models import User
from journals.models import Journal, JMSMessage


SYSTEM_NAME = 'MSRC JMS'
# def get_invitation(user):
#     invitation = Invitation.objects.filter(
#         user        = user,
#         is_accepted = False,
#         is_declined = False,
#     ).count()
    
#     return invitation

def get_jmsmessage(user):
    notification = JMSMessage.objects.filter(
        target    = user,
        is_opened = False,
    ).count()
    
    return notification

@login_required(login_url='/sign-in/')
def index(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	user = request.user
	a =  User.objects.get(username=user)
	jms_articles = Article.objects.filter(is_submitted = False, submitting_author=a)
	return render(
		request,
		'articles/index.html',
		{
			'system_name': 'Article List',
			'page_title': 'Submitted Articles',
			'jms_articles':jms_articles,
			'submitted':'active'
		}
	)

@login_required(login_url='/sign-in/')
def my_articles(request, article_list=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	state = article_list
	curr_user = request.user
	# a =  User.objects.get(username=user)
	
	if state =='submitted':
		jms_articles = Article.objects.filter(Q(is_submitted=True ) & Q(submitting_author=curr_user) & (Q(state='ACC') | Q(state='PEN')) )
		system_name = 'Submitted Article'
	elif state =='art_draft':
		jms_articles = Article.objects.filter(is_submitted=False, submitting_author=curr_user)
		system_name = 'Draft'
	elif state =='on_review':
		jms_articles = Article.objects.filter(is_submitted=True, submitting_author=curr_user, state='REV' )
		system_name = 'On Review'
	elif state =='published':
		jms_articles = Article.objects.filter(is_submitted=True, submitting_author=curr_user, state='PUB' )
		system_name = 'Published Article'
	elif state =='archives':
		jms_articles = Article.objects.filter( Q(submitting_author=curr_user) &( Q(state='WITH') | Q(state='DEC')))
		system_name = 'Archived'

	return render(
		request,
		'articles/index.html',
		{
			'system_name': system_name,
			'page_title': 'List of Draft Article',
			'jms_articles':jms_articles,
			state:'active'
		}
	)

@login_required(login_url='/sign-in/')
def del_article_file(request):
	_file_id_ = request.GET.get('file_del')
	# file_id_ = decrypt_text(_file_id_)
	
	success = True
	try:
		instance = ArticleFile.objects.get(id__exact=_file_id_)
		os.unlink( instance.file_path.path )
		instance.delete()
	except ArticleFile.DoesNotExist:
		success = False
	if success:
		return HttpResponse('yes')
	
	return HttpResponse('no')

@login_required(login_url='/sign-in/')
def update_article_author(request, article_det=None, auth_info =None):
	print('not-form')
	if request.method == 'POST':	
		auth_form = Author_Form(request.POST)
		
		art_id_=article_det

		auth_user = User.objects.get(id__exact=auth_info)	
		print('updating')
		if auth_form.is_valid():
			print('valid')
			
			auth_user.contact_no      = auth_form.cleaned_data['contact_no']
			auth_user.address         = auth_form.cleaned_data['address']
			auth_user.email   		= auth_form.cleaned_data['email']
			# curr_user.affiliation     = art_form.cleaned_data['affiliation']
			auth_user.department      = auth_form.cleaned_data['department']
			auth_user.position_title  = auth_form.cleaned_data['position_title']
			auth_user.first_name		= auth_form.cleaned_data['first_name']
			auth_user.last_name		= auth_form.cleaned_data['last_name']
			auth_user.save()
			# User.save()
			# if not is_author_exists(arts,article_auth):
			# class Meta():
			# 	db_table = 'article_author'
			

			direct='/articles/submission/'+art_id_+'/authors'
			# request.session['article_auths'] = art_form.cleaned_data['first_name']+', '+art_form.cleaned_data['last_name']
			return HttpResponseRedirect(direct)

		else:
			print('form-errror')
			print(auth_form.errors)

			request.session['auth_prof_message'] = auth_form.errors
			# "Invalid Data. Please fill the correctly."
			return HttpResponseRedirect('/articles/edit-coauthor/'+article_det+'/'+auth_user.id+'/')

	else:
		print('not-form')
		request.session['auth_prof_message'] = "Error occured.Not saved."
		return HttpResponseRedirect('/articles/edit-coauthor/'+article_det+'/'+auth_info+'/')

	return render(request,'profile_display.html',
        {
            'system_name':request.user,
            'author_form':auth_form,
            'curr_user':auth_user,
        }
    )

def article_author_update_form(request,article_info=None, auth_info =None ):

	art_auths = User.objects.get(id=auth_info)
	arts=decrypt_text(article_info)
	art_info = Article.objects.get(id=arts)

	auth_form = Author_Form(initial=model_to_dict(art_auths))
	# return HttpResponseRedirect('/articles/')
	# iss = Issue.objects.filter(is_published = True)
	message=None
	if 'auth_prof_message' in request.session:
		message = request.session.get('auth_prof_message')
		del request.session['auth_prof_message']

	return render(request,'profile_display.html',
        {
            'system_name':'User - '+request.user.username,
            'author_form':auth_form,
            'curr_user':art_auths,
            'message':message,
            'art_info':art_info,
        }
    )

@login_required(login_url='/sign-in/')
def get_author_info(request):
	author_det = request.GET.get('art_auth')
	art_det = request.GET.get('art_det')
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	message=None
	
	art_auths=None
	outs=None

	try:
		print('getting_infor')
		# art_info = Article.objects.get(id__exact=pk)
		art_auths =  ArticleAuthor.objects.get(id = art_det, author = author_det)
		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
		outs={
			'author_name':art_auths.author.first_name+' '+art_auths.author.last_name,
			'email_add':art_auths.author.email,
			'contact_num':art_auths.author.contact_no,
			'department':art_auths.author.department,
			'position_title':art_auths.author.position_title,
			'success': 'yes'
		}

	except ArticleAuthor.DoesNotExist or ArticleAuthor:
		print(art_det,'--art',author_det,'--auth')
		message='Unable to retrieve author info.'
		
	if outs:
		data=outs
	else:
		data={
			'success':'no',
			'message':message
		}
	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")
	

@login_required(login_url='/sign-in/')
def get_article_info(request, article_name=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	print('article_info')
	message=None
	
	pk = decrypt_text(article_name)
	art_info=None
	art_auths=None
	try:
		art_info = Article.objects.get(id__exact=pk)
		art_auths =  ArticleAuthor.objects.filter(article = art_info)

		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
	except Article.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	
	if 'joumsy_message' in request.session:
		message = request.session.get('joumsy_message')
		del request.session['joumsy_message']

	return render(
		request,
		'articles/article_info.html',
		{
			'system_name': 'Article Info',
			'art_info':art_info,
			'author_list': art_auths,
			'message':message
		}
	)

'''
note limit the display with Submitted only
'''
@login_required(login_url='/sign-in/')
def view_articles(request):

	curr_user=request.user
	arts = Article.objects.filter(is_submitted=False, submitting_author=curr_user)

	return render(
		request,
		'articles/index.html',
		{
			'system_name': 'Article List',
			'page_title': 'Submitted Articles',
			'jms_articles': arts,
		}
	)

@login_required(login_url='/sign-in/')
def article_author_form(request, article_name =None):
	
	# art_form = ArticleForm()
	# print('asdasdas')
	message=None
	art_auths=None
	
	if article_name:
		pk = decrypt_text(article_name)
		try:
			art_info = Article.objects.get(id__exact=pk)
			
			art_auths =  ArticleAuthor.objects.filter(article = art_info)

			# form.fields['patient_hospid'].initial = admitted.patient.patient_hospid
			added = None

			auth_form = Author_Form()

			if 'article_auths' in request.session:
				added = request.session['article_auths']
			return render(
				request,
				'articles/article_submission.html',
				{
					'system_name': 'Article Form - Author',
					'author_form': auth_form,
					'art_auth':'active',
					'art_info':art_info,
					'author_list': art_auths,
					'newly_add':added,
				}
			)

		except Article.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'		
	else:
		message='Invalid Data.<a href="articles/articles-list"> Click here</a> to see article list'

	return HttpResponse(message)


@login_required(login_url='/sign-in/')
def article_file_form(request, article_name):
	# art_form = ArticleForm()
	message=None
	if article_name:
		pk = decrypt_text(article_name)
		try:
			art_info = Article.objects.get(id__exact=pk)
			# art_form = ArticleForm(initial=model_to_dict(art_info))
			art_files=ArticleFile.objects.filter(article=art_info)

			for x in art_files:
				print(x.file_name,'---')

			# form.fields['patient_hospid'].initial = admitted.patient.patient_hospid
			return render(
				request,
				'articles/article_submission.html',
				{
					'system_name': 'Article Form - Files',
					'art_files':'active',
					'art_info':art_info,
					'article_files':art_files,
				}
			)
		except Article.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
	else:
		message='Invalid Data.<a href="articles/articles-list"> Click here</a> to see article list'

	return HttpResponse(message)

@login_required(login_url='/sign-in/')
def upload_article_file(request, article_name=None):
	message=None

	if article_name:
		pk = decrypt_text(article_name)
		dt = datetime.today()
		many_files=request.FILES.getlist('artfiles')
		
	# file_name = 				models.CharField(max_length=100, null= True)
	# file_path = 				models.FileField(upload_to='article_file')
	# date_created  = 			models.DateTimeField(auto_now = True)
	# article =					models.ForeignKey(Article, null=True)
	# uploader =					models.ForeignKey(User, null=True)
		try:
			art_info = Article.objects.get(id__exact=pk)
			creator= request.user

			for x in many_files:

				a_file = ArticleFile(
					file_name=x.name,
					file_path=x,
					article = art_info,
					date_created=dt,
					uploader =creator,
					main=False,
					state ='SUP'
				)

				a_file.save()

			return HttpResponse('Files uploaded! ')

		except Article.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
			return HttpResponse(message)

		# direct='/articles/submission_info/'+encrypt_text(str(art_info.id))

		# return HttpResponseRedirect(direct)

	return HttpResponse(message)


@login_required(login_url='/sign-in/')
def article_metadata_form(request):
	art_form = ArticleForm()
	return render(
		request,
		'articles/article_submission.html',
		{
			'system_name': 'Article Form',
			'meta_form': art_form,
			'art_meta':'active'
		}
	)

@login_required(login_url='/sign-in/')
def article_meta_save(request):
	message = None
	if request.method == 'POST':
		art_form = ArticleForm(request.POST, request.FILES)
		
		if art_form.is_valid():
			
			dt = datetime.today()
			curr=request.user
			article_meta = Article(
				section = 					art_form.cleaned_data['section'],
				title = 					art_form.cleaned_data['title'],
				# subtitle   =				models.CharField(max_length=300, null = True)		
				# cover_letter = 				models.CharField(max_length=500, null = True)
				references   =				art_form.cleaned_data['references'],
				#keywords   =				art_form.cleaned_data['keywords'],
				# journal   =					art_form.cleaned_data['journal']
				# copyright   =				models.ForeignKey(Copyright, null=True)
				is_featured =				False,
				article_version =			0,
				
				published_by_others =		False,
				is_submitted = 				False,
				abstract = 					art_form.cleaned_data['abstract'],
				likes = 					0,
				pub_date = 					None,
				date_created = 				dt,
				require_review = 			True,
				restrict_access_article = 	False,
				date_modified = 			None,
				submitting_author =  		curr,
			)
			article_meta.save()
			# if request.user:
			
			artauth = ArticleAuthor(
				author = 				User.objects.get(username= curr),
				article = 				article_meta,
				date_added  = 			dt,
				main_author =			True,
				)
			artauth.save()

			if 'main_file' in request.FILES:
				# print(request.FILES['image_path'])
				art_file = request.FILES['main_file']
				a_file = ArticleFile(
					file_name=art_file.name,
					file_path=art_file,
					article = article_meta,
					date_created=dt,
					uploader =request.user,
					state= 'AUTH',
					main=True,
					stage=1
				)
				a_file.save()

	return HttpResponseRedirect('/articles/submission/'+encrypt_text(str(article_meta.id))+'/authors/')

@login_required(login_url='/sign-in/')
def update_article_info(request, article_name=None):
	message=None
	main_file=None
	if article_name:
		pk = decrypt_text(article_name)
		try:
			art_info = Article.objects.get(id__exact=pk)
			# request.session['article'] = pk
			# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
			if ArticleFile.objects.filter(article=art_info,main =True).exists():
				main_file = ArticleFile.objects.get(article=art_info,main =True)

		except Article.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
			return HttpResponse(message)
		
		art_form = ArticleForm(initial=model_to_dict(art_info))
		

		return render(
			request,
			'articles/article_submission.html',
			{
				'system_name': 'Article Form',
				'meta_form': art_form,
				'art_meta':'active',
				'art_info':art_info,
				'main_file':main_file,
			}
		)
	else:
		if request.method == 'POST':
			artform = ArticleForm(request.POST, request.FILES)
			print("we got the form")
			dt = datetime.today()
			if artform.is_valid():
				print("checking for duplicate file", )
				
				# old = request.session['article']
				old = request.POST.get('art_detail')
				old_art = Article.objects.get(id = old)
				check = False
				
				# datetime.today()
				try:
					pasyente = Article.objects.exclude(id__exact = old_art.id).get(title__iexact = request.POST.get('title'))
					check = True		
					message = 'Article Info exist.'
				except Article.DoesNotExist or Article:
					pass

				if not check:
					print("no duplicate")

					old_art.title 					= artform.cleaned_data['title']
					old_art.section 				= artform.cleaned_data['section']
					old_art.references 				= artform.cleaned_data['references']
					old_art.keywords 				= artform.cleaned_data['keywords']
					old_art.abstract				= artform.cleaned_data['abstract']
					old_art.is_featured 			= False
					old_art.pub_date				= None
					old_art.require_review			= False
					date_modified					= dt

					old_art.save()

					if 'main_file' in request.FILES:
						# print(request.FILES['image_path'])
						art_file = request.FILES['main_file']
						if ArticleFile.objects.filter( article=old_art, main=True).exists():
							main_art_file = ArticleFile.objects.get( article=old_art, main=True)
							os.unlink( main_art_file.file_path.path )
							main_art_file.file_name = art_file.name+'_1'
							main_art_file.file_path = art_file
							main_art_file.date_created=dt
							main_art_file.save()

						else:
							a_file = ArticleFile(
								file_name=art_file.name,
								file_path=art_file,
								article = old_art,
								date_created=dt,
								uploader =request.user,
								state= 'AUTH',
								main=True,
								stage=1
							)
							a_file.save()

					# saved_pats = str(request.session['patient']) + patientform.cleaned_data['firstname'] + patientform.cleaned_data['lastname']

					# delete session
					# del request.session['article']
					# request.session['article_auths']

					request.session['updated_succ_messages'] = 'Article Successfully updated.'					
					
					direct = ('/articles/submission/'+encrypt_text(str(old_art.id)))
					
					return HttpResponseRedirect(direct)
				else:
					return HttpResponseRedirect('/error-404/')

			else:
				print("form is not valid")
				main_file =None
				old = request.POST.get('art_detail')
				if ArticleFile.objects.filter(article=art_info,main =True).exists():
					main_file = ArticleFile.objects.get(article=art_info,main =True)
				art_info = Article.objects.get(id=old)
				form = ArticleForm()


				form.fields['title'].initial 				= request.POST.get('title')
				form.fields['abstract'].initial 				= request.POST.get('abstract')
				form.fields['keywords'].initial 				= request.POST.get('keywords')
				form.fields['references'].initial 		= request.POST.get('references')
				
				# del request.session['article']

				return render(
					request,
					'articles/article_submission.html',
					{
						'system_name': 'Article Form',
						'meta_form': form,
						'art_meta':'active',
						'art_info':art_info,
						'message':'Please fill form properly. Unable to update data.',
						'main_file':main_file,
					}
				)

	return HttpResponse(message)

def del_article_author(request):
	art_auth_id_ = request.GET.get('art_auth')
	art_auth_id_ = decrypt_text(art_auth_id_)
	ArticleAuthor.objects.get(id=art_auth_id_).delete()
	return HttpResponse('yes')


'''
note affiliation will be intended for authors who wish to publish their article  in MSRC 
'''
def article_author_save(request):
	message = None
	
	if request.method == 'POST':
		print('saving author data...')
		art_form = Author_Form(request.POST)
		
		art_id_=request.POST.get('submission_meta')
		
		_id=decrypt_text(art_id_)
		arts=Article.objects.get(id=_id)
		
		if art_form.is_valid():
			print('author form  valid...')
			dt = datetime.today()
			article_auth = User(
				user_type       = 'AUTH',
				gender          = '0',
				contact_no      = art_form.cleaned_data['contact_no'],
				address         = art_form.cleaned_data['address'],
				email   		= art_form.cleaned_data['email'],
				affiliation     = art_form.cleaned_data['affiliation'],
				department      = art_form.cleaned_data['department'],
				position_title  = art_form.cleaned_data['position_title'],
				first_name		= art_form.cleaned_data['first_name'],
				last_name		= art_form.cleaned_data['last_name'],
				# middle_name		= art_form.cleaned_data['middle_name'],
				username		= genEmpUsername(),
				is_superuser 	=False,
				is_staff		= True,
				is_active		= False,
				# degree          = models.CharField(max_length = 120, null=True)
				# research_interest = models.CharField(max_length = 420, null=True)
				# fax_number      = models.CharField(max_length = 20 , null=True)
			)

			article_auth.save()

			# User.save()
			# if not is_author_exists(arts,article_auth):
			sub_author= ArticleAuthor(
				author = 				article_auth,
				article = 				arts,
				date_added  = 			dt,
				main_author =			False,
				)
			sub_author.save()
				
			# class Meta():
			# 	db_table = 'article_author'
			

			direct='/articles/submission/'+art_id_+'/authors'
			request.session['article_auths'] = art_form.cleaned_data['first_name']+', '+art_form.cleaned_data['last_name']
			return HttpResponseRedirect(direct)

		else:
			print('form is not valid')
			print(art_form.errors)
			return render(
				request,
				'articles/article_submission.html',
				{
					'system_name': 'Article Form - Author',
					'auth_form': art_form,
					'art_auth':'active',
					'art_info':arts,
					'author_list': None,
				}
			)
	else:
		return HttpResponse('notpost !')

# def is_author_exists(_article_id, _auth_id):
# 	try:
# 		ArticleAuthor.objects.get(article=_article_id, author=_auth_id)
# 		return True
# 	except ArticleAuthor.DoesNotExist or ArticleAuthor:
# 		return False

@login_required(login_url='/sign-in/')
def submit_article(request, article_name=None):
	message=None

	if article_name:
		pk = decrypt_text(article_name)
		dt = datetime.today()
		try:
			art_info = Article.objects.get(id__exact=pk)

			try:
				ArticleFile.objects.get(main=True, article=art_info)
				art_info.is_submitted = True
				art_info.date_submitted = dt
				art_info.state = 'ACC'
				art_info.save()
			except ArticleFile.DoesNotExist or ArticleFile:
				request.session['joumsy_message'] = "Please Complete Submission"
				
				
				direct='/articles/submission_info/'+encrypt_text(str(art_info.id))
				return HttpResponseRedirect(direct)


			message=art_info.title +'- has been submitted.'
			request.session['joumsy_message'] = message

		except Article.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
			return HttpResponse(message)

		direct='/articles/submission_info/'+encrypt_text(str(art_info.id))

		return HttpResponseRedirect(direct)

	return HttpResponse(message)

