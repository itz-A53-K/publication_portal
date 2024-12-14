from django.db import models
from django.db.models import Max
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .manager import UserManager


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=75)
    abbreviation = models.CharField(max_length=5, unique=True) # example 'CSIT' for 'Computer Science and Information Technology'
    publication_count = models.IntegerField(default=0,editable=False)

    def __str__(self) :
        return self.abbreviation


class Faculty(AbstractUser):
    designation_choices = [
        ('P', 'Professor'),
        ('ASP','Assistant Professor'),
        ('AP', 'Associate Professor'),
        ('RS', 'Research Scholar'),
        ('S','Student')
    ]


    username = None
    first_name = None
    last_name = None
    
    fid = models.CharField(max_length=25,primary_key=True, editable= False)
    email = models.EmailField(unique=True, max_length=75)
    name = models.CharField(max_length=75)

    dept = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    designation = models.CharField(max_length=5,choices= designation_choices, default= 'AP')

    is_admin = models.BooleanField(default=False)
    is_superAdmin = models.BooleanField(default=False)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS= []

    objects= UserManager()

    
    def save(self, *args, **kwargs):
        if not self.fid:  # If ID is not set, generate it
            self.fid = self.get_next_fid()
        super().save(*args, **kwargs)
    
    
    def get_next_fid(self):

        # Filter to find the highest existing fid with the same dept abbreviation
        
        prefix = 'SADMIN' if self.is_superuser else self.dept.abbreviation.upper()
        filter_params = {'is_superuser': True} if self.is_superuser else {'dept__abbreviation': prefix}

        last_fid = Faculty.objects.filter(**filter_params).aggregate(max_fid=Max('fid'))['max_fid']


        if last_fid:
            next_sl_number = int(last_fid[-3:]) + 1
        else:
            next_sl_number = 1

        new_fid = f"{prefix}{next_sl_number:03d}"

        return new_fid
    
    def __str__(self) :
        return self.fid


class Faculty_details(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)    
    phone = models.BigIntegerField(default=1234567890)
    profile_img = models.ImageField(default='user_profile/profile_default.png', blank=True, upload_to='user_profile')

    qualification = models.CharField(max_length=255,null=True, blank= True)  
    co_authors = models.JSONField(null=True,blank=True)
    citation_count= models.IntegerField(default=0)

    h_index = models.IntegerField(default=0)
    h5_median = models.IntegerField(default=0)
    def __str__(self) :
        return f"{self.faculty.fid}"







class Publication(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    abstract = models.CharField(max_length=500)
    authors = models.ManyToManyField(Faculty)
    keywords = models.JSONField(default=list)
    publisher = models.CharField(max_length=75, null=True, blank=True)
    publish_date = models.DateField()
    pdf = models.FileField(upload_to='uploads/pdfs/', null=True, blank=True)
    pages = models.CharField(max_length=30,null=True, blank=True)

    category = models.CharField(max_length=15, editable= False)
    views = models.BigIntegerField(default=0)

    # class Meta:
    #     abstract = True

    def __str__(self):
        return str(self.id) 

class Article(Publication):
    content = models.TextField(null=True, blank=True)
    volume = models.IntegerField(default=1)
    impact_factor = models.FloatField(default=0.0)
    h_index = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.category = 'Article'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class Book(Publication):
    edition = models.IntegerField(default=1)
    language = models.CharField(max_length=10, default="Eng",choices=[('Eng','English'),('Hin','Hindi'),('Asm','Assamese')])
    isbn = models.CharField(max_length=20, null=True, blank=True)
    issn = models.CharField(max_length=20, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.category = 'Book'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Citation(models.Model):
    publication = models.ForeignKey(Publication, related_name='citing_publication', on_delete=models.CASCADE)
    cited_by = models.ForeignKey(Publication, related_name='cited_by', on_delete=models.CASCADE)
    #it needs to be filtered based of uploading 'book' or 'Article' in the view and should show option of publication which is relavent to that