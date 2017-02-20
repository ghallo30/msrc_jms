from django.db import models
from employee.models import User

# Create your models here.
class Issue(models.Model):
    
    issue_volume    = models.IntegerField(default=1)
    issue_number      = models.IntegerField( default=1)
    issue_year = models.CharField( max_length=50, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_submission_expiry = models.DateTimeField('date submission expiry', null=True)
    date_published= models.DateTimeField('date issue published',null=True)

    title = models.CharField(max_length=300, null=True)
    description = models.TextField(null=True)
    date_modified = models.DateTimeField('date issue modified', null=True)
    cover_photo = models.FileField(upload_to = 'issue_cover', null=True)
    cover_photo_desc = models.TextField(max_length=300, null=True)

    is_published = models.BooleanField(default = True)
    is_accepted = models.BooleanField(default = False)
    is_decline = models.BooleanField(default = False)

    onlineIssn =    models.CharField(max_length = 50, null = True)
    printIssn =     models.CharField(max_length = 50, null = True)
    special_issue =     models.BooleanField(default = False)

class IssueGroup(models.Model):
    title = models.CharField(max_length = 250, null = True)
    date_created = models.DateTimeField('date issue created', null=True)
    created_by = models.ForeignKey(User, null = True)
    
    db_table = 'issue_group'

class IssueEditorialBoard(models.Model):
    issue_member = models.ForeignKey(User, null = True)
    issue_group = models.ForeignKey(IssueGroup, null = True)
    issue = models.ForeignKey(Issue, null = True)
    publish_email = models.BooleanField( default = True)
    is_displayed = models.BooleanField( default = True)

    db_table = 'issue_editorial_board'