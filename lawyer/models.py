from django.db import models
from django.contrib.auth.models import User
class Lawyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    law_firm = models.CharField(max_length=20, null=True)
    def __str__(self):
        return self.user.__str__()

class School(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
        
class Course(models.Model):
    GRADE = (
        ('5','五年级'),
        ('6','六年级'),
        ('7','初一'), 
        ('8','初二'))
    name = models.CharField(max_length=15)
    grade = models.CharField(choices = GRADE, default='5', max_length=2)
    def __str__(self):
        return '《' + self.name + '》';
class Class(models.Model):
    school = models.ForeignKey(School, related_name='classes', on_delete=models.CASCADE)
    class_id = models.IntegerField(help_text = '班级')
    duration = models.IntegerField(default=40)
    start_time = models.DateTimeField()
    lawyer = models.ForeignKey(Lawyer, null=True, on_delete=models.CASCADE, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return ('%d班' % self.class_id)