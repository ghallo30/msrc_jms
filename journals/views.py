# from django.shortcuts import render
import json
import datetime

from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_protect,csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,  user_passes_test

from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db import connection, transaction


from django.contrib.auth.models import PermissionsMixin, Group

# tools
from tools.tools import decrypt_text, encrypt_text, hasAccess, genEmpUsername,hasAssignedEditor, convert_to_text
from functools import reduce
# # database
from django.db.models import Q

# # forms
from django.forms.models import model_to_dict
from .forms import JMSTemplateForm, IssueSelectionForm

from articles.forms import IssueForm

# # models
from .models import JMSTemplate, Announcement, JMSMessage
from articles.models import  Section, Article, ArticleFile, Copyright, ArticleAuthor,ArticleSubmissionLog
from employee.models import User
from reviews.models import (
		ReviewDetails, 
		EditorDecision,
		AssignEditor, 
		ReviewForm, 
		ReviewerElement, 
		ReviewerResponse, 
		ReviewFormItem
	)
from issues.models import Issue,IssueGroup,IssueEditorialBoard

'''
	initial editor decision
	include reviewer version
	include reviewer file
	
	assign issue on article- done
	create search on article
	add category on article

'''
@login_required(login_url='/sign-in/')
def index(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	# user = request.user
	# a =  User.objects.get(username=user)
	jms_articles = Article.objects.filter( is_submitted=True, state='ACC').exclude(id__in= ReviewDetails.objects.filter(is_active=True).values_list('article', flat=True))
	b='unassigned'
	
	print('create')
	convert_to_text()

	return render(
		request,
		'journals/index.html',
		{
			'system_name': 'JMS-Editor',
			'page_title': 'List of Article',
			'jms_articles':jms_articles,
			b:'active',

		}
	)

# functions to search articles on opdqueue
def search_submitted_data(request):
	search_val = request.GET.get('search_text')
	search_type = request.GET.get('search_filter')
	search_state = request.GET.get('state') 
	# path_begins = request.GET.get('begs')
	
	if search_type == 'art_title':
		if search_state:
			submitted_art = Article.objects.filter( title__icontains=search_val, is_submitted=True, state=search_state)
		else:
			submitted_art = Article.objects.filter( title__icontains=search_val, is_submitted=True)
	else:

		pats = search_val.split()

		qset1 =  reduce(Q.__or__, [Q(submitting_author__firstname__istartswith=query) |
					 Q(submitting_author__lastname__istartswith=query ) for query in pats])

		if search_state:
			submitted_art = Article.objects.filter( qset1, is_submitted=True, state=search_state)
		else:
			submitted_art = Article.objects.filter( qset1, is_submitted=True)
		
		data ={
			'submitted_art':submitted_art,

		}

	return render(request,'outpatient/list_queue.html', data)

@login_required(login_url='/sign-in/')
def get_submissions(request, art_state=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	state = art_state
	# user = request.user
	# a =  User.objects.get(username=user)
	jms_articles = None
	issue_select_form  = None
	pubs = False

	if art_state:
		if art_state =='unassigned':
			jms_articles = Article.objects.filter( is_submitted=True, state='ACC').exclude(id__in= ReviewDetails.objects.filter(is_active=True).values_list('article', flat=True))
		elif art_state =='in_review':
			jms_articles = Article.objects.filter(is_submitted=True, state='REV')
		elif art_state =='for_publish':
			jms_articles = Article.objects.filter(is_submitted=True, state='ED')
			issue_select_form  = IssueSelectionForm()
		elif art_state =='published':
			jms_articles = Article.objects.filter(is_submitted=True, state='PUB')
			pubs= True
		elif art_state =='archived':
			# jms_articles = Article.objects.filter(Q(state='DEC')| Q(state='WITH'))
			jms_articles = Article.objects.filter(Q(state='DEC')| Q(state='WITH')| Q(state='UPUB'))
			# issue_select_form  = IssueSelectionForm()
		else:
			return HttpResponseRedirect('/error-404/')		
	else:
		jms_articles = Article.objects.filter(is_submitted=True)

	return render(
		request,
		'journals/index.html',
		{
			'system_name': 'Article List',
			'page_title': 'List of Article',
			'jms_articles':jms_articles,
			state:'active',
			'issue_select_form':issue_select_form,
			'published':pubs,
		}
	)

def reject_submission(request, article_name = None):

	art_det = request.GET.get('art_det')
	
	dt = datetime.datetime.now()
	outs= None
	try:
		art = Article.objects.get(id=art_det)
		# # iss= Issue.objects.get(id=issue_det)
		# art.article_issue = iss
		art.state ='DEC'
		art.save()
		outs ={
			'submit_info':art.title,
			'success':'yes',
			'submit_det':art.id,
		}
		
	except Article.DoesNotExist or Article:
		outs=None
	
	if outs:
		data = outs
	else:
		data={
				'success':'no',
		}

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")
	# return render(request,'journals/review_response.html', data)

def assign_issue_article_publish(request):

	art_det = request.GET.get('art_det')
	issue_det = request.GET.get('issue_det')
	dt = datetime.datetime.now()
	try:
		art = Article.objects.get(id=art_det)
		iss = Issue.objects.get(id=issue_det)
		art.article_issue = iss
		art.state ='PUB'
		art.pub_date = dt
		art.save()

	except Article.DoesNotExist or Article:
		return HttpResponse('no')

	
	return HttpResponse('ok')

# FOR PUBLISH ARTICLE
def assign_issue_article_display(request, article_name):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=None
	issue_select_form = IssueSelectionForm()
	
	pk = decrypt_text(article_name)
	art_info=None
	art_auths=None
	eddie_decision=None
	try:
		art_info = Article.objects.get(id__exact=pk)
		art_auths =  ArticleAuthor.objects.filter(article = art_info)
		art_files = ArticleFile.objects.filter(article = art_info )
		try:
			eddie_decision = EditorDecision.objects.filter(article=art_info, decided=True, decision='ACC')
		except EditorDecision.DoesNotExist or EditorDecision:
			print('unable to retrieve decision!!!')

	except Article.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	
	if 'joumsy_message' in request.session:
		message = request.session.get('joumsy_message')
		del request.session['joumsy_message']

	return render(
		request,
		'journals/inedit_article_info.html',
		{
			'system_name': 'Submission InEdit',
			'art_info':art_info,
			'author_list': art_auths,
			'art_files_list': art_files,
			'eddie_decision':eddie_decision,
			'message':message,
			'issue_select_form':issue_select_form,
		}
	)

def get_issue_info(request, iss_det=None):
	message=""
	print('gettinng issue info')
	jms_issue=None
	try:

		jms_issue=Issue.objects.get(id=iss_det)
		issue_article = Article.objects.filter(article_issue=jms_issue)
	except Issue.DoesNotExist or Issue:
		message="Unable to retreive issue info"	

	data={
		'jms_issue':jms_issue,
		'message': message,
		'system_name':'Issue Info',
		'issue_article':issue_article,
	}
	# json_response = json.dumps(data)
	# return HttpResponse(json_response, content_type="application/json")
	return render(request,'journals/issue_info.html', data)

def view_issue(request, iss_state=None):
	if iss_state=='published':
		print('published')
		jms_issue=Issue.objects.filter(is_published=True)
	else:		
		jms_issue=Issue.objects.filter(is_published=False)
		iss_state='not_published'
	
	message=""

	is_saved = request.session.get('issue_saved')
	
	if is_saved is not None:
		if is_saved==0:
			message=" Issue title exist."
		else:	
			try:
				a=Issue.objects.get(id = is_saved)
				message=a.title + " - Issue has been saved."
				# delete session
				del request.session['issue_saved']
			except Issue.DoesNotExist or Issue:
				message=None

	data={
		'issues':jms_issue,
		'page_title': 'Issues List',
		'message': message,
		'system_name':'Issues List',
		iss_state:'active',
	}
	# json_response = json.dumps(data)
	# return HttpResponse(json_response, content_type="application/json")
	return render(request,'journals/index_issue.html', data)

def publish_issue(request):

	iss_det = request.GET.get('issue_info')

	print('publishing_issue--',iss_det)
	dt = datetime.datetime.now()
	try:
		issue_meta=Issue.objects.get(id__exact=iss_det)
		if Article.objects.filter(article_issue=issue_meta).exists():
			issue_meta.is_published = True
			issue_meta.date_published =dt
			issue_meta.save()
			return HttpResponse('yes')
		else:
			return HttpResponse('no_article')
	except Issue.DoesNotExist or Issue:
		print('not pulished')
		return HttpResponseRedirect('/joumsy/issues_view/published/')

	# special_issue =     models.BooleanField(default = False)

	return HttpResponseRedirect('/joumsy/issues_view/not_published/')

def create_issue(request, issue_state):
	data=None
	if issue_state =='create':
		data={
			'issue_form': IssueForm(),
			'issue_create':'active',
			'page_title':'Create Issue',
			'system_name':'Create Issue',
		}
	elif issue_state =='save':
		if request.method == 'POST':
			iss_form = IssueForm(request.POST, request.FILES)
			
			if iss_form.is_valid():
					
				dt = datetime.datetime.now()
				curr=request.user

				if not Issue.objects.filter(title__iexact=iss_form.cleaned_data['title'] ).exists():

					issue_meta = Issue(
						issue_volume = 		int(iss_form.cleaned_data['issue_volume']),
						issue_number = 		int(iss_form.cleaned_data['issue_number']),
						issue_year = 		iss_form.cleaned_data['issue_year'],
						title = 			iss_form.cleaned_data['title'],
						description = 		iss_form.cleaned_data['description'],
						printIssn =			iss_form.cleaned_data['printIssn'],
						is_published =		False,
						# special_issue =     models.BooleanField(default = False)
					)
					issue_meta.save()

					if 'cover_photo' in request.FILES:
						# print(request.FILES['image_path'])
						issue_meta.cover_photo = request.FILES['cover_photo']

					issue_meta.save()

					request.session['issue_saved'] = issue_meta.id
				else:
					request.session['issue_saved'] = 0
				return HttpResponseRedirect('/joumsy/issues_view/not_published')
			
		else:
			print('not post')
				
	# json_response = json.dumps(data)
	# return HttpResponse(json_response, content_type="application/json")
	return render(request,'journals/index_issue.html', data)

# view reviewer response on article review
def get_review_response(request):
	review_id = request.GET.get('review_det')
	data=None
	outs=None

	try:
		revs = ReviewDetails.objects.get(id=review_id)
		# print('quality ----- ',revs.get_quality_display)
		outs = {

			'recommendation': revs.recommendation,
			'quality': revs.quality,
			'clarity': revs.clarity,
			'abstract_review': revs.abstract_review,
			'abstract_suggestions': revs.abstract_suggestions,
			'date_submitted': str(revs.date_submitted.date),
			'date_start': str(revs.date_start),
			'date_due': str(revs.date_ended),
			'response_id': revs.id,
			'rev_article': revs.article.id,
			'rev_article_title': revs.article.title,
			'acceptability': revs.acceptability,
			'success': 'yes'	
		}

		# outs = serializers.serialize('json', ReviewDetails.objects.get(id=review_id))
		outs= {'review_response':revs,
				'success': 'yes'}

	except ReviewDetails.DoesNotExist or ReviewDetails:
		outs = None
		message = 'Unable to retreive review response'
		
	if outs:
		print('outs');
		data=outs
	else: 
		data={
			'success':'no',
			'message': message,
		}

	# json_response = json.dumps(data)
	# return HttpResponse(json_response, content_type="application/json")
	return render(request,'journals/review_response.html', data)


@login_required(login_url='/sign-in/')
def accept_article(request):

	art_pk = request.GET.get('art_det')
	recommend_val = request.GET.get('recommend_val')
	
	url = 'journals/editor_list.html';
	# url = request.GET.get('url')
	# s_type = request.GET.get('opd_search_filter')
	# print(url)
	pname = request.GET.get('search_text').split()

	SYSTEM_NAME = 'Search Result'

	chk=False

	outs = None

	if chk:
		data=outs
	else: 
		data={
			'success':'no',
			'message': message,
		}

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

@login_required(login_url='/sign-in/')
def search_editor(request, art_state=None):

	search_val = request.GET.get('search_text')
	art_pk = request.GET.get('art')
	pk = decrypt_text(art_pk)
	url = 'journals/editor_list.html';
	# url = request.GET.get('url')
	# s_type = request.GET.get('opd_search_filter')
	# print(url)
	pname = request.GET.get('search_text').split()

	SYSTEM_NAME = 'Search Result'

	qset1 =  reduce(Q.__or__, [Q(first_name__istartswith=query) | Q(last_name__istartswith=query) for query in pname])
	
	eddie =  User.objects.filter( (qset1) & Q(groups__id__exact=4) )

	assoc_editors_list = []

	try:
		art_info = Article.objects.get(id__exact=pk)

		for x in eddie:
			chk=EditorDecision.objects.filter(editor= x,article=art_info).exists()
			is_auth = ArticleAuthor.objects.filter(author= x, article=art_info).exists()
			if not is_auth and not chk:
				h = {
					'editor_name': x.first_name +" "+x.last_name,
					'assoc_editor_info': x,
					'done_decision':EditorDecision.objects.filter(editor= x, decided=True, is_rescind_descision=False).count(),
					'current_work':AssignEditor.objects.filter(assoc_editor= x, is_accepted= True, is_active=True, is_done=False).count(),
				}

				assoc_editors_list.append(h)

	except Article.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	data ={
		'assoc_editors_list':assoc_editors_list,
		'art_info':art_info,
		'from_search':search_val
	}
	return render(request, url, data)

@transaction.atomic()
@login_required(login_url='/sign-in/')
def submit_editor_decide(request ):
	
	art_info=None
	art_auths=None
	dt= datetime.datetime.now()
	edit_note = None
	auth_note = None
	chk = False
	outs = None
	data = None
	message=""

	pk = request.GET.get('art_det')
	decision_val = request.GET.get('recommend_val')
	edit_note = request.GET.get('eddie_note')

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')


	try:
		with transaction.atomic():

			try:
				art_info = Article.objects.get(id__exact=pk)
				chk=True
				not_done_review = ReviewDetails.objects.filter(article=art_info, is_done=False, is_active=True)

				if not not_done_review :
					eddie_done = EditorDecision.objects.filter(article=art_info, rounds=art_info.current_rounds, decided=True).exists()
					
					if not eddie_done:

						eddie_decision = EditorDecision(
							editor = request.user,
							decision   = decision_val,
							article     =   art_info,
							date_created = dt,
						    decided=True,
						    date_decided = dt,
						    notes_for_author = auth_note,
							notes_for_editor = edit_note,
							rounds=1,
						)

						eddie_decision.save()
						print(' eddie_decision saved\n')

						if decision_val=='ACC':
							art_info.state = 'ED' 
							print(' creatinng article log.<br/>')
							art_log= ArticleSubmissionLog(
								creator = request.user,
								# desc of work done
								work_desc = 'Accepted - '+str(art_info.id)+' Article - by Editor -> ' + eddie_decision.editor.username,
								# dictionary of model and id
								att_obj = str(eddie_decision.id)+'-'+'EditorDecision',
							)
							art_log.save()
						elif decision_val=='DEC':
							art_info.state = 'DEC'
							art_log= ArticleSubmissionLog(
								creator = request.user,
								# desc of work done
								work_desc = 'Declined -'+str( art_info.id)+' Article - by Editor -> ' +eddie_decision.editor.username,
								# dictionary of model and id
								att_obj = str(eddie_decision.id)+'-'+'EditorDecision',
							)

							art_log.save()

						elif decision_val=='REV':
							art_info.state = 'VIS'

							art_log= ArticleSubmissionLog(
								creator = request.user,
								# desc of work done
								work_desc = 'Require Revision - '+str( art_info.id)+' Article - by Editor -> ' +eddie_decision.editor.username,
								# dictionary of model and id
								att_obj = str(eddie_decision.id)+'-'+'EditorDecision',
							)
							art_log.save()
						print(' creating output article.\n')
						
						outs={
							'recommend': eddie_decision.decision,
							'recommend_date':str(eddie_decision.date_decided.date()),
							'success':'yes',
						}
						print(' updating article.\n')
						art_info.save()

					else:
						message="Article has decision in this round"
						print("Article has decision in this round")

				else:
					message="Reviews must all be submitted."
					print("Reviews must all be submitted.")

			except Article.DoesNotExist or Article:
				message='Invalid Data. Unable to retreive Article Info.<br/> Please refresh page.'
				print('Invalid Data. Unable to retreive Article Info.<br/> Please refresh page.')
	except:
		message ='Unable to process editor decision. Some error occurs.'
		print('Unable to process editor decision. Some error occurs.')
	
	if not outs or outs == None:
		data={
			'success':'no',
			'message':message
		}
	else:
		data =outs

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

def get_editor_assign_template(tempform, assoc_edit, sub_info, curr_user):
	
	temp_key = tempform
	assoc = assoc_edit
	artid = sub_info

	
	message=""
	# user = request.user
	# a =  User.objects.get(username=user)
	try:
		email_temp = JMSTemplate.objects.get( template_title = temp_key )
		assoc_eddie = User.objects.get(id=assoc)
		art_info = Article.objects.get(id=artid)
		
		userpicks=dict()
		
		userpicks['editor_name'] = assoc_eddie.get_full_name()
		userpicks['editor_uname'] = assoc_eddie.username

		userpicks['article_title'] = art_info.title
		userpicks['article_abstract'] = art_info.abstract
		userpicks['article_review_url'] = str(art_info.id)
		userpicks['submissionUrl'] = 'at editor'
		
		edit = User.objects.get(username=curr_user)
		userpicks['eic_name'] = edit.get_full_name()
		

		test_content=email_temp.content
		email_format = test_content.format(**userpicks)
		
		# print('----------------------\n',email_format)


	except JMSTemplate.DoesNotExist or JMSTemplate:
		message="template does no longer_exist"

	return email_format

@login_required(login_url='/sign-in/')
@transaction.atomic()
def assign_accept_editor(request):
	edie = request.GET.get('ass_editor')

	edie_id = decrypt_text(edie)

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message = ""
	dt = datetime.datetime.now()
	art_info = None
	outs = None
	chk = False
	eddie =None
	try:
		with transaction.atomic():			
			try:

				eddie = AssignEditor.objects.get(id=edie_id)
				chk=True

				has_assigned=hasAssignedEditor(eddie.article,'article')
					
				if not has_assigned:
					eddie.is_accepted=True
					eddie.save()
					print('asdasd---',eddie.assoc_editor.username)
					art_log= ArticleSubmissionLog(
						creator = request.user,
						# desc of work done
						work_desc = 'Accepted role - Assigned Editor -'+ eddie.assoc_editor.username +' - to article -'+ str( eddie.article.id),
						# dictionary of model and id
						att_obj = str(eddie.id)+'-'+'AssignEditor',
					)

					art_log.save()
					
					outs={
						'success':'yes',
						'art_title':eddie.article.title,
						'ass_edit':eddie.assoc_editor.first_name+', '+eddie.assoc_editor.last_name,
						'ass_edit_info':eddie.id,
						'art_ident':encrypt_text(str(eddie.article.id)),
					}

					
				else:
					chk=False
					message="Article has been assigned"

			except AssignEditor.DoesNotExist or AssignEditor:
				chk= False
	except:
		print('accept-assign not saved. error occurs on data insertion!')

	if chk:
		data=outs
	else: 
		data={
			'success':'no',
			'message': message,
		}

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

@transaction.atomic()
@login_required(login_url='/sign-in/')
def assign_editor(request):
	art_det = request.GET.get('art_curr')
	edie = request.GET.get('ass_editor')
	enddate = request.GET.get('date_due')

	edie_id = decrypt_text(edie)
	pk= decrypt_text(art_det)

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=""
	dt = datetime.datetime.now()
	art_info=None
	outs=None
	chk=False
	# try:
	# 	with transaction.atomic():

	try:
		eddie = User.objects.get(id=edie_id)
		chk=True
		print('Getting User editor Info')
		try:
			art_info = Article.objects.get(id__exact=pk)
			print('Getting article Info')
			has_assigned=hasAssignedEditor(art_info,'article')
			
			if not has_assigned:
				accept= False

				if eddie.id == request.user.id:
					accept= True
					# article has been assigned notify other user

				assign_eddie = AssignEditor(
				    assoc_editor   = eddie,
				    article     =   art_info,
				    date_assigned = dt,
				    can_edit = True,
				    can_review = True,
				    date_notified = dt,
				    assigned_by = request.user,
				    is_accepted = accept,
				)
				assign_eddie.save()

				art_info.state='REV'
				art_info.date_review_start=dt
				art_info.save()

				# print(get_editor_assign_template('assign_editor', eddie.id ,art_info.id, request.user))

				# notif_message= JMSMessage(
				# 	creator     = request.user,
				# 	target    = eddie
				# 	content      = 'content',
				# 	title    = 'title',
				# 	is_opened = False,
				# 	date_sent = dt,
				# 	# date_update = 
				# )
				
				# notif_message.save()
				
				outs={
					'success':'yes',
					'art_title':art_info.title,
					'ass_edit':eddie.first_name+', '+eddie.last_name,
					'ass_edit_info':eddie.id,
					'art_ident':encrypt_text(str(art_info.id)),
				}

				art_log= ArticleSubmissionLog(
					creator = request.user,
					# desc of work done
					work_desc = 'Assigned Editor '+ eddie.username +' to article '+ str( art_info.id),
					# dictionary of model and id
					att_obj = str(eddie.id)+'-'+'AssignEditor',
				)

				art_log.save()
			
			else:
				chk=False
				message="Article has been assigned"


		except Article.DoesNotExist or Article:
			message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
			return HttpResponse(message)

	except User.DoesNotExist or User:
		chk= False
	# except:			
	# 	message ='Unable to assign Editor. Some error occurs.'
	# 	print('Unable to process editor decision. Some error occurs.')

	if chk:
		data=outs
	else: 
		data={
			'success':'no',
			'message': message,
		}

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

@login_required(login_url='/sign-in/')
def assign_reviewer(request):

	temp_key = request.GET.get('sub_info')
	rev = request.GET.get('assigned_reviewer')
	enddate = request.GET.get('date_due')
	
	rev_id = decrypt_text(rev)
	pk= decrypt_text(temp_key)

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=""
	dt = datetime.datetime.now()
	outs=None
	rev_user=None
	try:
		art_info = Article.objects.get(id__exact=pk)
		rev_exists=False

		if User.objects.filter(id__exact=rev_id).exists():
			rev_user=User.objects.get(id__exact=rev_id)

			rev_exists = ReviewDetails.objects.filter(article=art_info, reviewer=rev_user).exists()

			if not rev_exists:
				rev = ReviewDetails(
					article       = art_info,
					reviewer         = rev_user,
					date_start = 		dt,
					date_ended =		enddate,
					review_rounds  =	1,
					is_done         = False,
					assigned_by = request.user,
					is_invited = True,
					date_invited= dt,
					is_active = False,
				)

				rev.save()

				outs={
					'success':'yes',
					'submit_reviewer': rev.reviewer.last_name[0].upper()+', '+rev.reviewer.first_name,
					'submission':rev.article.title.title(),
				}

			else:
				outs={
					'success':'no',
					'message':'Review already assigned to this submission'
				}
		else:
			outs={
					'success':'no',
					'message':'User info does not exist.'
				}

	except Article.DoesNotExist or Article:
		outs={
				'success':'no',
				'message':'Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
			}
		
		return HttpResponseRedirect("message")
	# user = request.user
	# a =  User.objects.get(username=user)

	data=outs

	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

@login_required(login_url='/sign-in/')
def get_invite_template(request):
	
	temp_key = request.GET.get('tempform')
	artid= request.GET.get('sub_info')
	_id_art=decrypt_text(artid)
	rev = request.GET.get('assigned_reviewer')
	rev_id = decrypt_text(rev)

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=""
	# user = request.user
	# a =  User.objects.get(username=user)

	dt = datetime.datetime.now()
	dt= dt+ timedelta(days=2)
	try:
		email_temp = JMSTemplate.objects.get( template_title = temp_key )
		assigned_reviewer = User.objects.get(id=rev_id)
		art_info = Article.objects.get(id=_id_art)

		art_auths=ArticleAuthor.objects.filter(article=art_info)
		a_names=""
		
		for x in art_auths:
			a_names=a_names+ x.author.last_name.title() +', '+x.author.first_name.title()+'<br />'

		userpicks=dict()
		userpicks['article_authors'] = a_names
		userpicks['reviewer'] = assigned_reviewer.get_full_name()
		userpicks['date_response_review'] = dt.strftime('We are the %b %d, %Y')
		userpicks['date_ended']='December 2, 2016'

		userpicks['article_title'] = art_info.title
		userpicks['article_abstract'] = art_info.abstract
		
		userpicks['article_review_url'] = 'http://localhost:8000/articles/submission/'+str(art_info.id)
		

		userpicks['reset_url_password'] = 'http://'
		
		
		edit = User.objects.get(username=request.user)
		userpicks['editor_name'] =edit.get_full_name()
		userpicks['affiliation']= edit.affiliation
		userpicks['email_address']=edit.email
		userpicks['web_main_address']='http://localhost:8000/'


		test_content=email_temp.content
		email_format = test_content.format(**userpicks)

	except JMSTemplate.DoesNotExist or JMSTemplate:
		message="template does no longer_exist"


	return render(
		request,
		'journals/email_template.html',
		{
			'page_title': 'List of Article',
			'email_title':email_temp.title,
			'email_content':email_format,
			'to_user':assigned_reviewer,
			'art_details': art_info.id,
		}
	)

@login_required(login_url='/sign-in/')
def search_reviewer(request, art_state=None):

	search_val = request.GET.get('search_text')
	art_pk = request.GET.get('art')
	pk = decrypt_text(art_pk)
	url = 'journals/reviewer_list.html';
	# url = request.GET.get('url')
	# s_type = request.GET.get('opd_search_filter')
	# print(url)
	pname = request.GET.get('search_text').split()

	SYSTEM_NAME = 'Search Result'

	qset1 =  reduce(Q.__or__, [Q(first_name__istartswith=query) | Q(last_name__istartswith=query) for query in pname])
	
	revs =  User.objects.filter((qset1) & Q(groups__id__exact=2) )

	reviewers_list =[]

	try:
		art_info = Article.objects.get(id__exact=pk)

		for x in revs:
			chk=ReviewDetails.objects.filter(reviewer= x,article=art_info).exists()
			if not chk:
				h = {
					'reviewers_name': x.first_name +" "+x.last_name,
					'reviewer_info': x,
					'done_review':ReviewDetails.objects.filter(reviewer= x,is_done=True).count(),
					# 'current_invitation':ReviewDetails.objects.filter(reviewer= x,is_invited=True).count(),
				}

				reviewers_list.append(h)
		

	except Article.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	data ={
		'reviewers_list':reviewers_list,
		'art_info':art_info
	}

	return render(request, url, data)

@login_required(login_url='/sign-in/')
def jms_article_info_review(request, article_name=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=None

	pk = decrypt_text(article_name)
	art_info=None
	art_auths=None
	assigned_eddie = None
	invited_eddie  = None
	eds_decision  = None
	try:
		art_info = Article.objects.get(id__exact=pk)
		art_auths = ArticleAuthor.objects.filter( article = art_info )
		art_files = ArticleFile.objects.filter( article = art_info )
		
		
		try:
			main_file = ArticleFile.objects.get(article = art_info, main=True)
		except ArticleFile.DoesNotExist or ArticleFile:
			main_file=None	
		
		if EditorDecision.objects.filter(article=art_info).exists():
			eds_decision = EditorDecision.objects.filter(article=art_info, decided=True).latest('date_decided')

		try:
			assigned_eddie = AssignEditor.objects.get(article = art_info, is_accepted=True)
		except AssignEditor.DoesNotExist or AssignEditor:
			assigned_eddie = None
			invited_eddie = AssignEditor.objects.filter(article = art_info, is_accepted=False)
			
		revs = User.objects.filter(groups__id__exact=2)
		
		reviewers_list =[]

		for x in revs:
			chk=ReviewDetails.objects.filter(reviewer= x,article=art_info).exists()
			if not chk:
				rev_info=ReviewDetails.objects.filter(reviewer= x)
				h = {
					'reviewers_name': x.first_name +" "+x.last_name,
					'reviewer_info': x,
					'done_review':rev_info.filter(is_done=True).count(),
					'active_review':rev_info.filter(invitation_accepted=True, is_done=False, is_active=True).count(),
				}

				reviewers_list.append(h)
		
		submit_reviewers=ReviewDetails.objects.filter(article=art_info)
		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'


	except Article.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	
	if 'joumsy_message' in request.session:
		message = request.session.get('joumsy_message')
		del request.session['joumsy_message']

			

	return render(
		request,
		'journals/jms_article_info.html',
		{
			'system_name': 'Submission InReview',
			'art_info':art_info,
			'author_list': art_auths,
			'art_files_list': art_files,
			'reviewers_list': reviewers_list,
			'message':message,
			'art_review':'active',
			'assigned_eddie':assigned_eddie,
			'invited_eddie':invited_eddie,
			'submit_reviewers':submit_reviewers,
			'eds_decision':eds_decision,
			'main_file':main_file,

		}
	)

@login_required(login_url='/sign-in/')
def get_jms_article_info(request, article_name=None):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')
	
	message=None
	
	pk = decrypt_text(article_name)
	art_info=None
	art_auths=None
	assigned_eddie=None
	eds_decision=None
	main_file=None
	try:
		art_info = Article.objects.get(id__exact=pk)
		art_auths =  ArticleAuthor.objects.filter(article = art_info)
		art_files = ArticleFile.objects.filter(article = art_info )
		try:
			main_file = ArticleFile.objects.get(article = art_info, main=True)
		except ArticleFile.DoesNotExist or ArticleFile:
			main_file=None	
		

		try:
			assigned_eddie = AssignEditor.objects.get(article=art_info, is_accepted=True, is_active=True)
		except AssignEditor.DoesNotExist or AssignEditor:
			assigned_eddie = None
		
		if EditorDecision.objects.filter(article=art_info).exists():
			eds_decision = EditorDecision.objects.filter(article=art_info, decided=True).latest('date_decided')

		# message=art_info.title +'- Article .<a href="/articles/articles-list/"> Click here</a> to see article list'
	except Article.DoesNotExist or Article:
		message='Invalid Data.<a href="articles/articles-list/"> Click here</a> to see article list'
		return HttpResponse(message)
	
	if 'joumsy_message' in request.session:
		message = request.session.get('joumsy_message')
		del request.session['joumsy_message']

	return render(
		request,
		'journals/jms_article_info.html',
		{
			'system_name': 'Submission InReview',
			'art_info':art_info,
			'author_list': art_auths,
			'art_files_list': art_files,
			'assigned_eddie':assigned_eddie,
			'message':message,
			'art_meta':'active',
			'eds_decision':eds_decision,
			'main_file':main_file,
		}
	)

@login_required(login_url='/sign-in/')
def show_jms_templates(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	# user = request.user
	# a =  User.objects.get(username=user)
	jms_articles = JMSTemplate.objects.all()

	return render(
		request,
		'journals/index.html',
		{
			'system_name': 'Article List',
			'page_title': 'List of Article',
			'jms_articles':jms_articles,
		}
	)


@login_required(login_url='/sign-in/')
def create_jms_template(request):
	
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/sign-in/')

	
	if request.method == 'POST':
		tempform = JMSTemplateForm(request.POST)
		if tempform.is_valid():
			dt = datetime.datetime.now()
			user = request.user
			a =  User.objects.get(username=user)

			jms_test = JMSTemplate(
				title = tempform.cleaned_data['title'],
				content = tempform.cleaned_data['content'],
				date_created = dt,
				creator = a
			)

			direct = ('/jms/email_templates/')
			jms_test.save()

			# data = (admit_id, "edited")
			return HttpResponseRedirect(direct)
		else:
			return HttpResponseRedirect("Denied")

	return render(
		request,
		'journals/index.html',
		{
			'system_name': 'Article List',
			'page_title': 'List of Article',
			'jms_articles':jms_articles,
		}
	)