from django.db import models
from django.contrib.auth.models import User

class LawyerOffice(models.Model):
    class Meta:
        verbose_name = "律所"
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Lawyer(models.Model):
    class Meta:
        verbose_name = "律师"
        verbose_name_plural = verbose_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(LawyerOffice, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.__str__()

class School(models.Model):
    class Meta:
        verbose_name = "学校"
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
        
class Course(models.Model):
    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name
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
    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name
    school = models.ForeignKey(School, related_name='classes', on_delete=models.CASCADE)
    grade = models.IntegerField(help_text='年级')
    class_id = models.IntegerField(help_text = '班级')
    lawyer = models.ForeignKey(Lawyer, null=True, on_delete=models.CASCADE, blank=True, related_name='lawyer_classes')    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    start_time = models.DateTimeField()    
    duration = models.IntegerField(default=40)    
    course_2 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_2', null=True, blank=True)    
    start_time_2 = models.DateTimeField(help_text = '第二堂普法课', null=True, blank=True)
    duration_2 = models.IntegerField(default=40, help_text = '第二节课持续时间', null=True, blank=True)
    def __str__(self):
        return (self.school.name + '%d年级%d班' % (self.grade, self.class_id))
   
    def second_start_time(self):
        return True
 
class Lecture(models.Model):
    class Meta:
        verbose_name = '课时'
        verbose_name_plural = verbose_name
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name = 'lectures')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)    
    duration = models.IntegerField(default=40)
    def __str__(self):
        if(self.start_time):
            return self.start_time.strftime('%m{m}%d{d}').format(m='月', d='日')
        else:
            return '未确定时间'