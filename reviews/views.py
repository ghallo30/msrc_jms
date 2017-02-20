import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_protect,csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,  user_passes_test

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection, transaction


from tools.tools import decrypt_text, encrypt_text, hasAccess, genEmpUsername
# database
from django.db import transaction
from django.db.models import Q

# forms
from django.forms.models import model_to_dict
from .forms import Review_Submission_Form

from employee.forms import Registration_Form, Author_Form

# models
from articles.models import Section,Article, ArticleFile, Copyright, ArticleAuthor
from employee.models import User
from journals.models import Journal, JMSTemplate, JMSMessage
from .models import ReviewDetails, ReviewerElement, ReviewerResponse, ReviewForm 

@login_required(login_url='/sign-in/')
def index(request, state=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	# user = request.user
	a =  User.objects.get(username=request.user)
	
	jms_rev_details=ReviewDetails.objects.filter(reviewer=a, invitation_declined=False, date_cancelled=None,date_replaced=None)
	
	return render(
		request,
		'reviews/index.html',
		{
			'system_name': 'Review Submission',
			'page_title': 'Assigned Submission',
			'jms_rev_details':jms_rev_details,
		}
	)

@login_required(login_url='/sign-in/')
def get_review_article_info(request, ref_det=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=None
	
	pk = decrypt_text(ref_det)
	art_info=None
	art_auths=None
	rev_form = None
	try:
		rev_info = ReviewDetails.objects.get(id__exact=pk, invitation_declined=False)
		
		if rev_info.invitation_accepted==True:
			rev_form='active'

		art_auths =  ArticleAuthor.objects.filter(article = rev_info.article)
		art_files = ArticleFile.objects.filter(article = rev_info.article, state='SUP' )
		art_submission_file =ArticleFile.objects.get(article = rev_info.article, main=True)

		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
	except ReviewDetails.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)

	return render(
		request,
		'reviews/submission_review.html',
		{
			'system_name': 'Article Info',
			'rev_info':rev_info,
			'author_list': art_auths,
			'files_list': art_files,
			'message':message,
			'art_meta':'active',
			'is_accepted':rev_form,
			'art_submission_file':art_submission_file,
		}
	)

@login_required(login_url='/sign-in/')
def display_review_form(request, ref_det=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=None
	
	pk = decrypt_text(ref_det)
	jms_rev_details_form=None
	art_info=None
	art_files =None
	try:
		rev_info = ReviewDetails.objects.get(id__exact=pk, invitation_declined=False)

		if rev_info.invitation_accepted==True:
			rev_form='active'

			jms_rev_details_form= Review_Submission_Form(initial=model_to_dict(rev_info))
			art_info=Article.objects.get(id =rev_info.article.id)
			art_files=ArticleFile.objects.filter(article=rev_info.article)
		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
	except ReviewDetails.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)

	

	return render(
		request,
		'reviews/submission_review.html',
		{
			'system_name': 'Review Form',
			'rev_info':rev_info,
			'message':message,
			'is_accepted':rev_form,
			'art_rev_form':'active',
			'review_form':jms_rev_details_form,
			'art_info':art_info,
			'art_files':art_files,
		}
	)

@login_required(login_url='/sign-in/')
def accept_review(request, ref_det=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=None
	
	pk = decrypt_text(ref_det)
	art_info=None
	art_auths=None
	dt= datetime.datetime.now()
	try:
		rev_info = ReviewDetails.objects.get(id__exact=pk)
		print(rev_info.article.title,'--rev_article----')
		
		rev_info.invitation_accepted=True
		rev_info.is_active=True

		rev_info.date_confirmed=dt

		rev_info.save()
		# rev_info.article.status='REV'
		# rev_info.article.save()
		# check if updating article state is_saved

		art_auths =  ArticleAuthor.objects.filter(article = rev_info.article)
		art_files = ArticleFile.objects.filter(article = rev_info.article, state='SUP' )

		return HttpResponseRedirect('/reviews/submission_meta/'+encrypt_text(str(rev_info.id))+'/')

		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
	except ReviewDetails.DoesNotExist or Article:
		message='Invalid Data.<a href="/reviews/"> Click here</a> to see article list'
		return HttpResponse(message)

	return HttpResponseRedirect('/reviews/submission_meta/'+encrypt_text(str(rev_info.id))+'/')

@login_required(login_url='/sign-in/')
def review_form_save(request, ref_det=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	pk = decrypt_text(ref_det)
	art_info=None
	art_auths=None
	dt= datetime.datetime.now()

	if request.method == 'POST':	
		rev_form = Review_Submission_Form(request.POST, request.FILES)

		try:
			rev_info = ReviewDetails.objects.get(id__exact=pk)
			print(rev_info.article.title,'--rev_article----')
			
    
			rev_info.recommendation = request.POST.get('recommendation')
			rev_info.acceptability = request.POST.get('acceptability')
			rev_info.clarity = request.POST.get('clarity')
			rev_info.quality = request.POST.get('quality')
			rev_info.abstract_review = request.POST.get('abstract_review')
			
			rev_info.comments_for_editor      = request.POST.get('comments_for_editor')
			rev_info.comments_for_author         = request.POST.get('comments_for_author')

			rev_info.save()

			art_auths =  ArticleAuthor.objects.filter(article = rev_info.article)
			art_files = ArticleFile.objects.filter(article = rev_info.article, state='SUP' )

			return HttpResponseRedirect('/reviews/submission_meta/'+encrypt_text(str(rev_info.id)))

			# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
		except ReviewDetails.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
			return HttpResponse(message)
		
	else:
		return HttpResponseRedirect("Denied")

@login_required(login_url='/sign-in/')
def review_form_submit(request, ref_det=None):
	
	pk = request.GET.get('revs_info')

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	art_info=None
	art_auths=None
	dt= datetime.datetime.now()
	chk = False
	outs=None
	data=None
	print(pk)
	message=""
	try:
		rev_info = ReviewDetails.objects.get(id__exact=pk)
		
		rev_info.date_submitted=dt

		rev_info.recommendation = request.GET.get('recommend_val')
		rev_info.is_done=True
		rev_info.is_active=False

		rev_info.save()

		outs={
			'recommend': rev_info.recommendation,
			'recommend_date':str(rev_info.date_submitted.date()),
			'success':'yes',
		}
		chk = True
		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
	except ReviewDetails.DoesNotExist or Article:
		chk=False
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	
	if chk:
		data=outs
	else: 
		data={
			'success':'no',
			'message': message,
		}

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")