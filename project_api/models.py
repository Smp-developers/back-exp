from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations=True
    
    def create_user(self,email,password=None, **extra_fields):
        
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must have is_staff true')
        
        return self.create_user(email,password,**extra_fields)




# adding spec and mobile fields into User model

class User(AbstractUser):
    username=None
    email=models.EmailField(unique=True)
    image=CloudinaryField('image')
    year_of_graduation=models.CharField(max_length=100,null=True,blank=True)
    experience_in_python=models.CharField(max_length=100,null=True,blank=True)
    batch=models.CharField(max_length=100,null=True,blank=True)
    paid_amount=models.CharField(max_length=12,null=True,blank=True)
    role=models.CharField(max_length=20)
    batch_started=models.CharField(max_length=20,null=True,blank=True)
    meeting_url=models.URLField(max_length=500,null=True,blank=True)
    college=models.CharField(max_length=30,null=True,blank=True)
    mobile=models.CharField(max_length=30,null=True,blank=True)
    Total=models.CharField(max_length=30,null=True,blank=True)
    referals=models.CharField(max_length=30,null=True,blank=True)
    social_media=models.URLField(max_length=500,null=True,blank=True)
    skills=models.CharField(max_length=500,null=True,blank=True)
    company=models.CharField(max_length=500,null=True,blank=True)
    designation=models.CharField(max_length=500,null=True,blank=True)
    batch_request=models.CharField(max_length=500,null=True,blank=True)
    
    objects=UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['password']
    def __str__(self):
        if self.is_superuser:
            return self.email +"("+" "+ "Admin" + " " +")"
        else:
            return  " "+"("+" "+ self.role + " " +")" +" "+self.email +" "+"------->"+" "+self.first_name
        
class Courses(models.Model):
    image=CloudinaryField('course')
    course_name=models.CharField(max_length=30)
    course_author=models.CharField(max_length=30)
    author_designation=models.CharField(max_length=30)
    author_image=CloudinaryField('course')
    def __str__(self):
        
        return   self.course_name  +"    "+"teaching by"+"    "+self.course_author 
    
class Trainees(models.Model):
    image=CloudinaryField('trainee')
    name=models.CharField(max_length=30)
    designation=models.CharField(max_length=30)
    company=models.CharField(max_length=30)
    mobile=models.CharField(max_length=30)
    batch=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    experience_field=models.CharField(max_length=500)
    def __str__(self):
        
        return   "teaching by"+"    "+self.name 