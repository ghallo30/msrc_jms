from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from .views import(
	index,
	get_submissions,
	get_jms_article_info,
	jms_article_info_review,
    search_reviewer,
    get_invite_template,
    assign_editor,
    assign_reviewer,
    search_editor,
    assign_accept_editor,
    submit_editor_decide,
    get_review_response,
    view_issue,
    create_issue,
    assign_issue_article_display,
    assign_issue_article_publish,
    reject_submission,
    
    publish_issue,
    get_issue_info,

   # list_review_form,
)

submission_patterns = [

    url(r'^$', get_jms_article_info),
    url(r'^review/$', jms_article_info_review),
    # url(r'^files/$', article_file_form),
]

urlpatterns = [
    
    url(r'^issue_info/(?P<iss_det>\w+)/', get_issue_info),
    url(r'publish_issue?', publish_issue),
    url(r'reject_submission?', reject_submission),
    url(r'assign_issue_publish?', assign_issue_article_publish),
    
    url(r'^issue/(?P<issue_state>\w+)/', create_issue),    
    url(r'^issues_view/(?P<iss_state>\w+)/', view_issue),
    url(r'^$', index),
    url(r'view_reviewer_response?', get_review_response),
    url(r'submit_decision?', submit_editor_decide),

    url(r'accept_submission_editor?', assign_accept_editor),
    url(r'search_editor?', search_editor),
    url(r'assign_submission_editor?', assign_editor),
    url(r'assign_submission_reviewer?', assign_reviewer),
    url(r'invite_email?', get_invite_template),
    url(r'^submission/(?P<art_state>\w+)/', get_submissions),
    url(r'^sub_info/(?P<article_name>\w+)/',  include(submission_patterns)),
    url(r'search_reviewer?', search_reviewer),
]
