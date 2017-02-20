from django.conf.urls import patterns, include, url

from .views import(
	index,
	view_articles,
	article_author_form,
	article_metadata_form,
	article_meta_save,
	article_file_form,
	article_author_save,
	update_article_info,
	my_articles,
	del_article_author,
	get_article_info,
	submit_article,
	upload_article_file,
	get_author_info,
	article_author_update_form,
	update_article_author,
	del_article_file,
)

submission_patterns = [
	url(r'^$', update_article_info),
	url(r'^authors/$', article_author_form),
	url(r'^files/$', article_file_form),
]


urlpatterns = [
	
	url(r'remove-file?', del_article_file),

	url(r'^coauthor_save/(?P<article_det>\w+)/(?P<auth_info>\w+)/$', update_article_author),

	url(r'^edit-coauthor/(?P<article_info>\w+)/(?P<auth_info>\w+)/', article_author_update_form),

	url(r'view-author-info?', get_author_info),
	url(r'^$', index),
	url(r'^upload_file/(?P<article_name>\w+)/save/$', upload_article_file),

	url(r'^submit_article/(?P<article_name>\w+)/', submit_article),

	url(r'remove-author?', del_article_author),

	url(r'^submission_info/(?P<article_name>\w+)/', get_article_info),

	url(r'^submission-list/(?P<article_list>\w+)/', my_articles),
	url(r'^articles-list/', view_articles), 
	url(r'^meta-save/$', article_meta_save),
	url(r'^art-auth-save/$', article_author_save),
	url(r'^submission/(?P<article_name>\w+)/', include(submission_patterns)),
	url(r'^meta-update/', update_article_info),
	url(r'^new_submission/', article_metadata_form),
    
]
