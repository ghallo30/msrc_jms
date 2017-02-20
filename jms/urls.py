from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
# logs out user
from django.contrib.auth.views import logout

from jms.views import (
	dashboard,
	signin,
	view_404_message,
	view_500_message,
	profile_display,
	profile_save,
)

urlpatterns = [
    # Examples:
    # url(r'^$', 'jms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^save_profile/', profile_save),
    url(r'^my_profile/', profile_display),
	url(r'^error-404/', view_404_message),
	url(r'^error-500/', view_500_message),
	
	url(r'^messages/', include('django_messages.urls')),

	url(r'^articles/', include('articles.urls')),
	url(r'^reviews/', include('reviews.urls')),


	url(r'^joumsy/', include('journals.urls')),
	url(r'^msrc/', include('home.urls')),
	url(r'^$', dashboard),
	url(r'^index$', dashboard),
	url(r'^logout/', logout, {'next_page':'/sign-in/'}),
	url(r'^sign-in/', signin),
	url(r'^admin/', include(admin.site.urls)),

]

urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )