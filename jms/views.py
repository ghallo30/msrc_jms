from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import Group 

from django.forms.models import model_to_dict
from employee.models import User

from employee.forms import Login_Form, Registration_Form, Author_Form
from issues.models import Issue

# Create your views here.
SYSTEM_NAME = 'MSRC-JEMS'

# hahahahaha
def dashboard(request):
	signin_form = Login_Form()
	# return HttpResponseRedirect('/articles/')
	iss = Issue.objects.filter(is_published = True)
	return render(request,'main_content.html',
        {
            'system_name':SYSTEM_NAME,
            'signin_form':signin_form,
            'jms_issues':iss,
        }
    )

def profile_save(request):
	if request.method == 'POST':
		auth_form = Author_Form(request.POST)
		
		art_id_=request.POST.get('submission_meta')

		curr_user = User.objects.get(username=request.user)
		
		
		
		if auth_form.is_valid():
			
			curr_user.contact_no      = auth_form.cleaned_data['contact_no']
			curr_user.address         = auth_form.cleaned_data['address']
			curr_user.email   		= auth_form.cleaned_data['email']
			# curr_user.affiliation     = art_form.cleaned_data['affiliation']
			curr_user.department      = auth_form.cleaned_data['department']
			curr_user.position_title  = auth_form.cleaned_data['position_title']
			curr_user.first_name		= auth_form.cleaned_data['first_name']
			curr_user.last_name		= auth_form.cleaned_data['last_name']
			

			curr_user.save()

			# User.save()
			# if not is_author_exists(arts,article_auth):
			# class Meta():
			# 	db_table = 'article_author'
			

			direct='/my_profile/'
			# request.session['article_auths'] = art_form.cleaned_data['first_name']+', '+art_form.cleaned_data['last_name']
			return HttpResponseRedirect(direct)

		else:
			request.session['prof_message'] = "Invalid Data. Please fill the correctly."
			return HttpResponseRedirect('/my_profile/')

	else:
		request.session['prof_message'] = "Error occured.Not saved."
		return HttpResponseRedirect('/my_profile/')
	
	auth_form = Author_Form()
	# return HttpResponseRedirect('/articles/')
	# iss = Issue.objects.filter(is_published = True)
	return render(request,'profile_display.html',
        {
            'system_name':request.user,
            'author_form':auth_form,
            'curr_user':curr_user,
        }
    )

def profile_display(request):

	asd = User.objects.get(username=request.user)
	
	auth_form = Author_Form(initial=model_to_dict(asd))
	# return HttpResponseRedirect('/articles/')
	# iss = Issue.objects.filter(is_published = True)
	message=None
	if 'prof_message' in request.session:
		message = request.session.get('prof_message')
		del request.session['prof_message']

	return render(request,'profile_display.html',
        {
            'system_name':'User - '+request.user.username,
            'author_form':auth_form,
            'curr_user':asd,
            'message':message,
        }
    )

def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()

def signin(request):
	login_form = Login_Form()
    # next       = None
	msg        = None
	page       = None

	if request.method == 'POST':
		form = Login_Form(request.POST)
		if form.is_valid():
			user_in = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
			if user_in:
				if user_in.is_active:
					login(request, user_in)
					if user_in.user_type == 'AUTH':
					    # if next != 'None':
					    #     return HttpResponseRedirect(next)
					    # else:
						return HttpResponseRedirect('/articles/')
					elif user_in.user_type == 'REV' or has_group(user_in, 'Reviewer'):
						return HttpResponseRedirect('/reviews/')
					    # login(request, user)
					    # return HttpResponseRedirect('/administrator/manage_topics')
					elif user_in.user_type == 'ADM' or has_group(user_in, 'Admin'):
						return HttpResponseRedirect('/joumsy/')
					    # login(request, user)
					    # return HttpResponseRedirect('/administrator/manage_topics')
					elif user_in.user_type == 'EDIT' or has_group(user_in, 'Editor'):
						return HttpResponseRedirect('/joumsy/')
					    # login(request, user)
					    # return HttpResponseRedirect('/administrator/manage_topics')
					else:
					    # if page == 'administrator':
					    #     request.session['message'] = 'Please try again, either your username or password is invalid.'
					    #     return HttpResponseRedirect('/administrator/')
					    # else:
						msg = 'Please try again, either your username or password is invalid.'
						return render(
							'register_login.html', 
							{ 
								'system_name' : 'MSRC Electronic Research Group - Login',
								'signin_form'  : login_form,
								'msg'         : msg, 
								'alert_status': 'alert-danger',
							}
					    )    
				else:
					msg = 'This account has been disabled.'
					return render(request,
					    'register_login.html', 
					    {
					     'system_name' : 'MSRC JMS- Login', 
					     'signin_form'  : login_form,
					     'msg'         : msg,
					     'alert_status': 'alert-danger',
					    }
					)
			else:
				msg = 'Please try again, either your username or password is invalid.'
				return render(request,
				    'register_login.html', 
				    { 
				     'system_name' : 'MSRC Electronic Research Group - Login',
				     'signin_form'  : login_form,
				     'msg'         : msg,
				     'alert_status': 'alert-info',
				    }
    			)
		else:
			return render(request,
				'register_login.html', 
				{ 
					'system_name'       : SYSTEM_NAME,
					'signin_form'        : login_form,
					'msg'               : "Refresh page and enter your account info appropriately",
					'alert_status': 'alert-info',
				}
			)
	else:
		return render(request,
			'register_login.html', 
			{ 
				'system_name'       : SYSTEM_NAME,
				'signin_form'        : login_form,
				'msg'               : msg,
				'alert_status': 'alert-danger',
			}
		)

def view_404_message(request, message=None):
	return render(
		request,
		'page_404.html',
		{
			'system_name': 'Error 404-Not Found',
			'message':message,
			'prev_link':None,

		}
	)

def view_500_message(request, message=None):
	return render(
		request,
		'page_500.html',
		{
			'system_name': 'Error 500',
			'message':message,
			'prev_link':None,
		}
	)