import datetime
from django.db import models

from employee.models import User, Keyword
from journals.models import Journal
from issues.models import Issue

from django.utils import timezone

'''
type manuscripts
'''
# 'article': 'JOUR',
# 				'book': 'BOOK',
# 				'booklet': 'PAMP',
# 				'inbook': 'CHAP',
# 				'conference': 'CHAP',
# 				'inproceedings': 'CHAP',
# 				'incollection': 'CHAP',
# 				'manual': 'BOOK',
# 				'masterthesis': 'THES',
# 				'phdthesis': 'THES',
# 				'misc': 'GEN',
# 				'proceedings': 'CONF',
# 				'techreport': 'RPRT',
# 				'unpublished': 'UNPB',
# 				'patent': 'PAT',
# 				'abstract': 'ABST',

class Submission_Type(models.Model):
	type_name = models.CharField(max_length=200, null= True)
	type_abbrev = models.CharField(max_length=200, null= True)
	
	date_created = models.DateTimeField(auto_now_add = True)
	created_by = models.ForeignKey(User, null= True)
	date_modified = models.DateTimeField(null = True)

class Section(models.Model):
	sec_name = models.CharField(max_length=200, null= True)
	date_created = models.DateTimeField(auto_now_add = True)
	created_by = models.ForeignKey(User, null= True)
	date_modified = 			models.DateTimeField(null = True)

	#this is to check if the instance is created recently 
	def was_created_recently(self):
		return self.date_created >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		return self.sec_name
	class Meta():
		db_table = 'section'

class Copyright(models.Model):
	cr_name = 				models.CharField(max_length=100, null= True)
	cr_description = 		models.CharField(max_length=300, null= True)
	date_created = 		models.DateTimeField(auto_now_add = True)
	created_by = models.ForeignKey(User, related_name = 'created_by' ,null= True)
	date_modified = 			models.DateTimeField(null = True)
	modified_by = models.ForeignKey(User, related_name = 'modified_by' ,null= True)


	#this is to check if the instance is created recently 
	def was_created_recently(self):
		return self.date_created >= timezone.now() - datetime.timedelta(days=1)

	def __str__(self):
		return self.cr_name
	class Meta():
		db_table = 'copyright'
		
# add these attribute:
''' 
	generate ArtNumber when article is submitted

	copyright
	
	assigning_issue

	is_submitted - True cannot be modified/ False submission is a draft(done)
	if review state - article can be edited

	category and journal will not be filled up by author

'''
class Article(models.Model):
	submission_type = 			models.ForeignKey(Submission_Type, null = True)
	section = 					models.ForeignKey(Section, null = True)
	title = 					models.CharField(max_length=200, null = True)

	art_number   =				models.CharField(max_length=300, null = True)		
	cover_letter = 				models.CharField(max_length=500, null = True)
	references   =				models.TextField( null = True)
	
	journal   =					models.ForeignKey(Journal, null=True)
	copyright   =				models.ForeignKey(Copyright, null=True)
	is_featured =				models.BooleanField(default=False)
	
	article_version =			models.CharField(max_length=300, null = True)
	parent_submission =			models.IntegerField(null=True)
	
	published_by_others =		models.BooleanField(default=False)

	is_submitted = 				models.BooleanField(default=False)
	current_rounds = 			models.IntegerField(default=1)
	abstract = 					models.TextField(null = True)
	likes = 					models.IntegerField(default=0)
	pub_date = 					models.DateTimeField('date published', null= True )
	date_created = 				models.DateTimeField(auto_now_add = True)
	require_review = 			models.BooleanField(default=True)
	restrict_access_article = 	models.BooleanField(default=False)
	date_modified = 			models.DateTimeField(null = True)
	submitting_author =  		models.ForeignKey(User, null=True)
	date_review_start =			models.DateTimeField(null = True)
	article_issue =				models.ForeignKey(Issue, null=True)
	# volume_number =		models.CharField(max_length=50, null=True)
	
	date_submitted = 			models.DateTimeField('date submitted',null = True)

	STATE =[
		( 'DRT', 'Draft Submission'),
		( 'ACC', 'Accepted Submission'),
		( 'REV', 'Review State' ),
		( 'VIS', 'Revision State'),
		( 'RES', 'Resubmit State'),
		( 'DEC', 'Declined Submission'),
		( 'ED', 'Editing State'),
		( 'PUB', 'Published'),
        ( 'UPUB', 'Unpublished'),
		( 'WITH', 'Withdrawn Submission')
	]

	state = 				models.CharField(max_length = 4, choices = STATE, null=True)
	
	def was_created_recently(self):
		return self.date_created >= timezone.now() - datetime.timedelta(days=1)

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	was_published_recently.admin_order_field = 'pub_date'
		
	class Meta():
		db_table = 'article'

class ArticleFile(models.Model):
	STATE =[
		( 'EDIT','editor_version'),
		( 'AUTH', 'author_version'),
		( 'REV', 'review_version' ),
		( 'SUP', 'supp_file' ),
	]

	state = 				models.CharField(max_length = 4, choices = STATE, null=True)

	file_name = 				models.CharField(max_length=100, null= True)
	file_path = 				models.FileField(upload_to='article_file')
	date_created  = 			models.DateTimeField(auto_now = True)
	article =					models.ForeignKey(Article, null=True)
	uploader =					models.ForeignKey(User, null=True)
	main = 				models.BooleanField(default= False)
	review_accessible = 		models.BooleanField(default= True)
	stage =						models.IntegerField(null=True)
	is_temp =					models.BooleanField(default= False)

	version_number = models.CharField(max_length=100,null=True)

	class Meta():
		db_table = 'article_file'

class ArticleAuthor(models.Model):
	author = 				models.ForeignKey(User, null= True)
	article = 				models.ForeignKey(Article, null = True)
	date_added  = 			models.DateTimeField(auto_now = True)
	main_author =			models.BooleanField(default= False)
	class Meta():
		db_table = 'article_author'

class ArticleKeywords(models.Model):
	article = 				models.ForeignKey(Article, null = True)
	keyword = 				models.ForeignKey(Keyword, null = True)
	date_added  = 			models.DateTimeField(auto_now = True)
	added_by =				models.ForeignKey(User,null=True)


class ArticleSubmissionLog(models.Model):
	date_done = models.DateTimeField(auto_now_add=True)
	creator = models.ForeignKey(User,null=True)
	# desc of work done
	work_desc = models.CharField(max_length=100)
	# dictionary of model and id
	att_obj = models.CharField(max_length=250)
		