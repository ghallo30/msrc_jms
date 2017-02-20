from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class User(AbstractUser):
	GENDER = [
		('M', 'Male'),
		('F', 'Female')
	]

	USER_TYPES = (
		('AUTH', 'Author'),
		('EDIT', 'Editor'),
		('REV', 'Reviewer'),
		('ADM', 'Admin'),
		('COA', 'Co-Author'),
	)

	user_type       = models.CharField(max_length = 5, choices = USER_TYPES)
	gender          = models.CharField(max_length = 1, choices = GENDER)
	contact_no      = models.CharField(max_length = 20 , null=True)
	address         = models.CharField(max_length = 120, null=True)
    
	affiliation     = models.CharField(max_length = 120 , null=True)
	department      = models.CharField(max_length = 120, null=True)
	position_title  = models.CharField(max_length = 120, null=True)
	degree          = models.CharField(max_length = 120, null=True)
	research_interest = models.CharField(max_length = 420, null=True)
	fax_number      = models.CharField(max_length = 20 , null=True)
	receive_new_issue = models.BooleanField(default=True)
	receive_new_announcement = models.BooleanField(default=True)

class Keyword(models.Model):
	key_type = models.CharField(max_length=100, null=True)
	key_value = models.CharField(max_length=100, null=True)

class Category(models.Model):
	name = models.CharField(max_length=200, null= True)
	date_created = models.DateTimeField(auto_now_add = True)
	created_by = models.ForeignKey(User, null= True)	

class UserInterest(models.Model):
	interest = models.ForeignKey(Category, null =True)
	user_emp = models.ForeignKey(User, null =True)

class Validation(models.Model):
	code = models.CharField(max_length = 9, blank = False, null = False)
	is_used = models.BooleanField(default = False)
	
	expiry_date = models.DateField('validation expiry date', null = True)
	generated_by = models.ForeignKey(User, related_name='generated_by',null= True)
	used_by = models.ForeignKey(User, related_name='used_by',null= True)