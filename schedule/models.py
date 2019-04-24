from django.db import models

# Create your models here.
class Module(models.Model):
    subject = models.CharField(max_length = 200, default = "null")
    code = models.CharField(max_length=200, default = "null")
    term = models.CharField(max_length=200, default = "null")
    core = models.CharField(max_length = 200, default = "null")
    subject_lead = models.CharField(max_length=200, default = "null")
    cohort_size = models.CharField(max_length=200, default = "null")
    enrolment_size = models.CharField(max_length=200, default = "null")    
    cohorts_per_week = models.CharField(max_length = 200, default = "null")
    lectures_per_week = models.CharField(max_length = 200, default = "null")
    labs_per_week = models.CharField(max_length = 200, default = "null")

class Class(models.Model):
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    title = models.CharField(max_length = 200, default = "null")
    Type = models.CharField(max_length=200, default = "null")
    class_related =  models.CharField(max_length=200, default = "null")
    location = models.CharField(max_length=200, default = "null")
    duration =models.CharField(max_length = 200, default = "null")
    start = models.CharField(max_length = 200, default = "null")
    end = models.CharField(max_length = 200, default = "null")
    description = models.CharField(max_length = 200, default = "null")
    makeup = models.CharField(max_length = 200, default = "null")
    assigned_Professors =models.CharField(max_length = 200, default = "null")