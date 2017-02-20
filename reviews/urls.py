from django.conf.urls import patterns, include, url

from .views import(
	index,
	get_review_article_info,	
	accept_review,
	display_review_form,
    review_form_save,
    review_form_submit
)

review_patterns = [
    url(r'^$', get_review_article_info),
    url(r'^review_form/$', display_review_form),
    # url(r'^files/$', article_file_form),
]

urlpatterns = [
    url(r'submit_review?',  review_form_submit ),
    url(r'^review_form/(?P<ref_det>\w+)/save/',  review_form_save ),
    url(r'^$', index),
    
    url(r'^review_form/(?P<ref_det>\w+)/save/',  review_form_save ),
    url(r'^submission_meta/(?P<ref_det>\w+)/',  include(review_patterns)),
    url(r'^accept_review/(?P<ref_det>\w+)/',  accept_review),
]
