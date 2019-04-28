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
    grade_2 = models.CharField(choices = GRADE, default='6', max_length=2, null=True, blank=True)
    def __str__(self):
        return '《' + self.name + '》'

class Class(models.Model):
    school = models.ForeignKey(School, related_name='classes', on_delete=models.CASCADE)
    class_id = models.IntegerField(help_text = '班级')
    grade = models.IntegerField(help_text='年级', null=True)
    duration = models.IntegerField(default=40)
    start_time = models.DateTimeField()
    lawyer = models.ForeignKey(Lawyer, null=True, on_delete=models.CASCADE, blank=True, related_name='lawyer_classes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    start_time_2 = models.DateTimeField(help_text = '第二堂普法课', null=True, blank=True)
    course_2 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_2', null=True, blank=True)
    duration_2 = models.IntegerField(default=40, help_text = '第二节课持续时间', null=True, blank=True)
    def __str__(self):
        return (self.school.name + '%d年级%d班' % (self.grade, self.class_id))
