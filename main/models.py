from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import datetime


class University(models.Model):
    name = models.CharField(max_length=100)
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    graduation_year = models.IntegerField(default=2023)


class Question(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='mainapp/question_images/', null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=datetime.datetime.now)
    

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='mainapp/question_images/', null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=datetime.datetime.now())



class Job(models.Model):
    company_name = models.CharField(max_length=500)
    position = models.CharField(max_length=30)
    link = models.URLField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(default=datetime.datetime.now())
    

class Internship(models.Model):
    company_name = models.CharField(max_length=500)
    position = models.CharField(max_length=30)
    appln_form = models.URLField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(default=datetime.datetime.now())
    duration = models.CharField(max_length=20)
    batches_allowed = models.CharField(max_length=50)
    stipend = models.CharField(max_length=50)


class Referral(models.Model):
    company_name = models.CharField(max_length=500)
    position = models.CharField(max_length=30)
    job_id = models.CharField(max_length=100)
    link = models.URLField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    date_posted = models.DateField(default=datetime.datetime.now())


# class Project(models.Model):
#     pass

# class Referral_request(models.Model):
#     from_user = models.ForeignKey(Student)
#     to_user = models.ForeignKey(Student)
#     refer_requested = models.ForeignKey(Referral)

