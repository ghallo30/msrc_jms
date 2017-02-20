from django.db import models

from employee.models import User
'''
delete usertype

add to articles
    classficiation
    section
    remove is_accepted
'''

class Journal(models.Model):    
    title       = models.CharField(max_length = 100, null=True)
    aim      = models.CharField(max_length = 300, null=True)

    scope         = models.CharField(max_length = 320)
    start_date		= models.DateTimeField('journal start date', null=True)
    pub_date		= models.DateTimeField('journal date published', null=True)
    allow_external_submission = models.BooleanField(default=True)
    restrict_access_article = models.BooleanField(default=False)
    require_review	= models.BooleanField(default=True)
    journal_rate = models.BooleanField(default=True)
    rate = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField('journal date modified',null=True)
    cheif_editor  = models.ForeignKey(User, null=True)


class JMSMessage(models.Model):
    creator     = models.ForeignKey(User, related_name = 'actor', null =True)
    target    = models.ForeignKey(User, related_name = 'target',null =True)
    content      = models.TextField(null=True)
    title    = models.CharField(max_length = 500)
    is_opened = models.BooleanField(default = False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateTimeField('date sent', null=True)
    date_update = models.DateTimeField('date updated', null=True)
    is_task = models.BooleanField(default=False)
    # invitation_accepted = models.BooleanField(default = False)
    # invitation_declined = models.BooleanField(default = False)

    date_created = models.DateTimeField(auto_now_add=True)
    class Meta():
        db_table = 'jms_message'

        

class JMSTemplate(models.Model):
    TEMP_TYPE = [
        ('EMAIL', 'E'),
        ('NOTIFICATION', 'N'),
    ]
    template_title = models.CharField(max_length = 500, null=True)
    creator     = models.ForeignKey(User, null =True)
    content      = models.TextField(null=True)
    title    = models.CharField(max_length = 500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField('date modified', null=True)
    temp_type = models.CharField( max_length=2, choices=TEMP_TYPE, null=True)

    class Meta():
        db_table = 'jms_template'

class Announcement(models.Model):
    created_by     = models.ForeignKey(User, null=True)
    
    TARGET = (
        ('ALL', 'ALL'),
        ('AUTH', 'Author'),
        ('EDIT', 'Editor'),
        ('REV', 'Reviewer'),
    )

    target_user    = models.CharField(max_length = 10, choices = TARGET)
    title      = models.CharField(max_length = 600)
    content    = models.TextField(null=True)
    # is_opened = models.BooleanField(default = False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_expiry = models.DateTimeField('date expiry')
    class Meta():
        db_table = 'jms_announcement'

class Policies(models.Model):
    CTYPE = (
        ('G', 'Guidelines'),
        ('P', 'Policies'),
    )

    content_type    = models.CharField(max_length = 2, choices = CTYPE, default='G')

    title = models.CharField(max_length=10,null=True)
    description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(null=True)
    intended_for= models.CharField(max_length=70, null=True)