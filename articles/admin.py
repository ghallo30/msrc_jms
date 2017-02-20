from django.contrib import admin

from .models import Article, Section, ArticleFile, ArticleAuthor

class SectionAdmin(admin.ModelAdmin):
    
	list_display = ('sec_name', 'date_created','was_created_recently')

	exclude = ('date_created', 'date_modified', 'created_by',)

# class ArticleFileInline(admin.TabularInline):
#     model = ArticleFile
#     extra = 1

class ArticleAdmin(admin.ModelAdmin):
    
	list_display = ('title', 'state', 'author_name', 'art_issue' )

	list_select_related = ('submitting_author', 'section')

	list_filter = ['pub_date']
	
	# fields = ('title', ('state', 'section'), 'abstract', )
	exclude = ('journal', 'copyright', 'submission_type', 'date_submitted', 'date_modified', 
		'article_version', 'require_review', 'subtitle', 'cover_letter','current_rounds',
		'parent_submission', 'likes', 'published_by_others', 'date_review_start', 'pub_date'
	)

	search_fields = ['submitting_author__first_name', 'submitting_author__last_name', 'title']

	# inlines = (ArticleFileInline,)

	def author_name(self, obj):
		return ("%s %s" % (obj.submitting_author.first_name, obj.submitting_author.last_name)).title()
	author_name.short_description = 'Author Name'

	def art_issue(self, obj):
		if obj.article_issue != None:
			return obj.article_issue.title.title()
		return 'None'
	art_issue.short_description = 'Issue'

	# def save_model(self, request, obj, form, change):
	# 	if obj.state !='PUB':
	# 		exclude =['article_issue']


class ArticleFileAdmin(admin.ModelAdmin):
    
	list_display = ('file_name','file_path', 'art_title', 'date_created')

	def art_title(self, obj):
		if obj.article != None:
			return obj.article.title.title()
		return 'None'
	art_title.short_description = 'Article'


class ArticleAuthorAdmin(admin.ModelAdmin):
    
	list_display = ('author_name', 'art_title')

	def art_title(self, obj):
		if obj.article != None:
			return obj.article.title.title()
		return 'None'
	art_title.short_description = 'Article'

	def author_name(self, obj):
		return ("%s %s" % (obj.author.first_name, obj.author.last_name)).title()
	author_name.short_description = 'Author Name'

admin.site.register(Section, SectionAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(ArticleFile, ArticleFileAdmin)

admin.site.register(ArticleAuthor, ArticleAuthorAdmin)