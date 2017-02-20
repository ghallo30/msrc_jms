from django.conf.urls import patterns, include, url

from .views import(
	view_article_info,
	view_article_issue,
	view_issues,
	view_faq,
	view_msrc_about,
	register_account,
	search_published_data,
	generate_article_info_pdf,
)


urlpatterns = [
	
	url(r'^gen-pdf/(?P<article_det>\w+)/', generate_article_info_pdf),

	# not done
	# url(r'^current/', search_published_data),

	url(r'search_article?', search_published_data),
	url(r'^register_account/', register_account),
    url(r'^about_msrc/', view_msrc_about),
    url(r'^faq/', view_faq),
    url(r'^content/(?P<article_det>\w+)/', view_article_info),
    url(r'^issue/(?P<issue_det>\w+)/', view_article_issue),
    url(r'^issue_list/', view_issues)

    
]
