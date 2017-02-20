import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from django.db.models import Q

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from datetime import *

# # models
from journals.models import Announcement
from articles.models import Section, Article, ArticleFile, Copyright, ArticleAuthor
from employee.models import User, Keyword, Category, Validation, UserInterest
from issues.models import Issue

from employee.forms import Login_Form, Registration_Form


def generate_article_info_pdf(request, article_det=None):
	
	try:
		art_info = Article.objects.get(id = article_det)
	except Article.DoesNotExist or Article:
		return HttpResponseRedirect('/error-404/')

	return render(
		request,
		'home/htmltopdf.html',
		{
			'system_name': 'Article Info',
			'art_info':art_info,
		}
	)

def get_current_pulished():
	dt = datetime.datetime.now()
	start_date = datetime.date(dt.year, 1, 1)
	end_date = datetime.date(dt.year, 3, 31)
	
	# Article.objects.filter(pub_date__range=)

	return True

def search_published_data(request):

	search_val = request.GET.get('search_text')
	# path_begins = request.GET.get('begs')
	jms_art=None
	
	if search_val:
		jms_art = Article.objects.filter( title__icontains=search_val, is_submitted=True, state='PUB')
		
		# jms_art = Article.objects.filter( (Q(submitting_author__first_name__icontains=search_val)|Q(submitting_author__last_name__icontains=search_val)| Q(title__icontains=search_val)) & Q(is_submitted=True)& Q(state='PUB'))
	
	# signin_form = Login_Form()

	
	return render(
		request,
		'home/search_list.html',
		{
			'system_name': 'Search Articles',
			# 'issue_info':issue_info,
			'jms_research':jms_art,
			# 'signin_form':signin_form,
		}
	)
	

# Create your views here.
def view_article_info(request, article_det=None):
	
	try:
		art_info = Article.objects.get(id =article_det)
	except Article.DoesNotExist or Article:
		return HttpResponse('article not found!!!')

	return render(
		request,
		'home/article_display.html',
		{
			'system_name': 'Article Info',
			'art_info':art_info,
		}
	)

def register_account(request):
	login_form = Login_Form()
	dt = datetime.today()

	uname = request.GET.get('validate_username')
	u_password=request.GET.get('validate_password')
	# except User.DoesNotExist or User:
	is_exist_user = User.objects.filter(username = uname).exists()
	if not is_exist_user:
		article_auth = User(
			user_type       = 'AUTH',
			# gender          = '0',
			# contact_no      = art_form.cleaned_data['contact_no'],
			# address         = None,
			email   		= request.GET.get('validate_email'),
			# affiliation     = art_form.cleaned_data['affiliation'],
			# department      = art_form.cleaned_data['department'],
			# position_title  = art_form.cleaned_data['position_title'],
			first_name		= request.GET.get('validate_firstname'),
			last_name		= request.GET.get('validate_lastname'),
			# middle_name		= art_form.cleaned_data['middle_name'],
			username		= uname,
			is_superuser 	=False,
			is_staff		= True,
			is_active		= True,
			# degree          = models.CharField(max_length = 120, null=True)
			# research_interest = models.CharField(max_length = 420, null=True)
			# fax_number      = models.CharField(max_length = 20 , null=True)
			# password = make_password(request.GET.get('password'), salt=None, hasher='default')
		)

		
		article_auth.set_password(u_password)

		article_auth.save()

		user_in = authenticate(
			username=uname,
			password=u_password
		)

		if user_in:
			login(request, user_in)
			return HttpResponseRedirect('/articles/')
		elif article_auth:
			print('not logged in')
			return render(request,
				'register_login.html', 
				{ 
					'system_name'       : 'Error Registration',
					# 'signin_form'        : login_form,
					'msg'               : 'Unable to register your account. Please fill the form correctly',
					'alert_status': 'alert-warning',
				}
			)
	else:
		return render(request,
				'register_login.html', 
				{ 
					'system_name'       : 'Error Registration',
					# 'signin_form'        : login_form,
					'msg'               : 'Username Info Exist.',
					'alert_status': 'alert-warning',
				}
			)

def view_faq(request):

	return render(
		request,
		'home/faq.html',
		{
			'system_name': 'Article ID',
		}
	)

def view_msrc_about(request):

	return render(
		request,
		'home/about_msrc.html',
		{
			'system_name': 'Article ID',
		}
	)


def view_article_issue(request,issue_det):
	# signin_form = Login_Form()
	sys_info =""
	issue_info =None
	jms_art  = None
	if issue_det.isdigit():
		try:
			issue_info = Issue.objects.get(id=issue_det)
			jms_art=Article.objects.filter(article_issue=issue_info)	
			sys_info = "Issue"+"- Vol."+str(issue_info.issue_volume)
		except Issue.DoesNotExist or Issue:
			sys_info ="Issue-Error"
	else:
		print('error')
	return render(
		request,
		'home/issue_article_list.html',
		{
			'system_name': sys_info,
			'issue_info':issue_info,
			'jms_research':jms_art,
			# 'signin_form':signin_form,
		}
	)

def view_issues(request):
	# signin_form = Login_Form()
	sys_info =""
	issue_info =None
	jms_art  = None

	issues_info = Issue.objects.filter(is_published=True)
	sys_info = 'Issue List'

	return render(
		request,
		'home/issue_list.html',
		{
			'system_name': sys_info,
			'jms_issues':issues_info,
		}
	)