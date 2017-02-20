from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
from articles.models import Article
from journals.models import Journal, JMSMessage
from employee.models import User

'''
---current work:
creating review form... to be continioude

check datetime ----- this would cause huge error in entering date

journals setting
max # of rescind date after decision has made
min weeks of review date rannge
withdrawn papers process

display for author's response on review
display and template on editors comments and decision
file delete on article_file
main file download, and if supplementary_file is downloadable
review form creation, selection

may include when submitting article:
    - competing interest for reviewer and/or editors
    - copyright

--homepage for readers-- 
display of published submission, by issue, sections, date, author, editors
article's section

-- admin/editors --
crud for message, section, template, user_groups

user profile, registration, deactivation (check resources-msrc)

upload proofread of submission by editor (check htdocs-jms)

'''

class ReviewForm(models.Model):
    form_title = models.CharField(max_length = 250, null=True)
    form_description = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True)
    is_active = models.BooleanField(default=False)
    class Meta():
        db_table = 'review_form'

class ReviewDetails(models.Model):
    article       = models.ForeignKey(Article, null=True)
    reviewer         = models.ForeignKey(User, related_name = 'reviewer', null=True)
    comments_for_editor      = models.TextField( null=True)
    comments_for_author         = models.TextField( null=True)
    
    RECOMMENDATION=[
        ('A', 'Accept Submission'),
        ('RV', 'Revision Required'),
        ('D', 'Reject Submission'),
    ]

    Q_CHOICES=[
        ('Y', 'Yes'),
        ('N', 'No'),
        ('P', 'Partly'),
    ]

    REV_CHOICES=[
    	('E', 'Excellent'),
        ('G', 'Good'),
        ('F', 'Fair'),
        ('P', 'Poor'),
    ]
    
    AB_CHOICES=[
    	('A', 'Adequate and Relevant'),
        ('I', 'Inadequate and/or Irrelevant'),
    ]


    recommendation   = models.CharField(max_length = 2, choices = RECOMMENDATION, null=True)
    
    acceptability = models.CharField(max_length = 2, choices = Q_CHOICES, null=True)

    quality = models.CharField(max_length = 2, choices = REV_CHOICES, null=True)
    clarity = models.CharField(max_length = 2, choices = REV_CHOICES, null=True)

    abstract_review = models.CharField(max_length = 2, choices = AB_CHOICES, null=True)
    abstract_suggestions = models.TextField(null=True)

    date_start = 		models.DateField('date started', null=True)
    date_ended =		models.DateField('date ended' , null=True)

    date_submitted	=	models.DateTimeField('date review submit' , null=True)
    date_reminded =     models.DateTimeField('date reminded', null=True)

    review_rounds  =	models.IntegerField(default=0)
    review_files =		models.FileField(upload_to='reviewer_files')
    
    invitation_accepted = models.BooleanField(default=False)
    invitation_declined = models.BooleanField(default=False)

    date_confirmed = models.DateTimeField('date review confirmed' , null=True)
    
    # date where reviewer was notified
    date_notified = models.DateTimeField( 'date notified' , null=True)
    date_invited = models.DateTimeField( 'date invited' , null=True)
    
    date_replaced         = models.DateTimeField('date replaced',null=True)
    date_cancelled        = models.DateTimeField('date cancelled',null=True)

    is_done         = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    
    assigned_by = models.ForeignKey(User, related_name='assigned_by', null=True)
    
    is_invited = models.BooleanField(default=False)

    can_upload = models.BooleanField(default=True)
    
    review_revision =   models.BooleanField(default=False)
    
    #rescind/recall/abort
    is_rescind_descision = models.BooleanField(default=False)
    rescind_descision_date = models.DateTimeField('rescind review daate',null=True)
    
    class Meta():
        db_table = 'review_details'

# class ReviewAssigment(models.Model):
        
    # date_sent = models.DateTimeField('date invitation sent' , null=True)
    # jmsmessage = models.ForeignKey(JMSMessage, null=True)

    # date_resent = 

class EditorDecision(models.Model):
    editor    = models.ForeignKey(User, null =True)
    article =   models.ForeignKey(Article, null =True )

    DECISION =[
        ('ACC', 'Accepted Submission'),
        ('REV', 'Revision Required'),
        ('RES', 'Resubmit for Review'),
        ('DEC', 'Decline Submission'),
    ]

    decision    = models.CharField(max_length = 4, choices=DECISION, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_decided = models.DateTimeField('date decided', null=True)
    decided  =  models.BooleanField(default=False)
    notes_for_author = models.TextField(null=True)
    notes_for_editor = models.TextField(null=True)
    rounds= models.IntegerField(default=1)

    is_rescind_descision = models.BooleanField(default=False)
    rescind_descision_date = models.DateTimeField('recall date',null=True)

    class Meta():
        db_table = 'editor_decision'

class AssignEditor(models.Model):
    assoc_editor   = models.ForeignKey(User,related_name='assoc_edit', null =True)
    article     =   models.ForeignKey(Article, null =True )
    date_assigned = models.DateTimeField(auto_now_add=True)
    can_edit = models.BooleanField(default=True)
    can_review = models.BooleanField(default=True)
    date_notified = models.DateTimeField('Date notified', null=True)
    assigned_by = models.ForeignKey(User, related_name='eic',null =True)
    is_accepted = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    
    date_replaced = models.DateTimeField('date replaced',null=True)
    date_cancelled = models.DateTimeField('date cancelled',null=True)
    is_active = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)

    class Meta():
        db_table = 'assign_editor'

class ReviewerElement(models.Model):
    FORM_TYPE =[
        ('T','text' ),
        ('S', 'select'),
        ('C', 'check'),
        ('R', 'radio')
    ]
    form_text = models.CharField(max_length = 250, null=True)
    form_value = models.CharField(max_length = 250, null=True)
    form_type = models.CharField(max_length = 4, choices=FORM_TYPE, default='T')
    form_name =  models.CharField(max_length = 100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)
    creator = models.ForeignKey(User,null =True)
    class Meta():
        db_table = 'reviewer_element'

class ReviewFormItem(models.Model):
    review_form = models.ForeignKey( ReviewForm , null=True)
    review_item = models.ForeignKey( ReviewerElement, null=True)
    required = models.BooleanField(default=True)
    # included on author message 
    included = models.BooleanField(default=True)

class ReviewerResponse(models.Model):
    review_element = models.ForeignKey(ReviewerElement,null=True)
    response_value = models.CharField(max_length = 250, null=True)
    review_details = models.ForeignKey(ReviewDetails, null=True)
    enabled = models.BooleanField(default=True)
    is_required = models.BooleanField(default=True)
    order_seq = models.IntegerField(default=1)
    class Meta():
        db_table = 'reviewer_response'

