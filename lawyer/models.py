from django.db import models
from django.contrib.auth.models import User
SEMESTER_CACHE = {}
class LawyerOffice(models.Model):
    class Meta:
        verbose_name = "律所"
        verbose_name_plural = verbose_name
    name = models.CharField('名称', max_length=20, unique=True)
    def __str__(self):
        return self.name
    

class Lawyer(models.Model):
    class Meta:
        verbose_name = "律师"
        verbose_name_plural = verbose_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def get_current_office(self):
        # get office for the current semester
        s = Semester.objects.get_current()
        return self.lawyer_office_semesters.get(semester__id = s['id']).office
    def set_current_office(self, office_id):        
        s = Semester.objects.get_current()
        office_semester = self.lawyer_office_semesters.get(semester__id = s['id'])
        office_semester.office_id = office_id
        office_semester.save()
    def __str__(self):
        return self.user.__str__()

class School(models.Model):
    class Meta:
        verbose_name = "学校"
        verbose_name_plural = verbose_name
    name = models.CharField('名称', max_length=20, unique=True)
    def __str__(self):
        return self.name

class SemesterManager(models.Manager):
    def get_current(self):
        # select the latest semester
        if(SEMESTER_CACHE.get('id') is None):
            s = Semester.objects.order_by('-end_date')[0]
            SEMESTER_CACHE['id'] = s.id
            SEMESTER_CACHE['name'] = s.name
        return SEMESTER_CACHE
    def clear_cache(self):
        global SEMESTER_CACHE
        SEMESTER_CACHE = {}  
        
class Semester(models.Model):
    class Meta:
        verbose_name = '学期'
        verbose_name_plural = verbose_name
    name = models.CharField('名称', max_length=20, unique=True)
    end_date = models.DateField('结束的日期')
    objects = SemesterManager()
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
    name = models.CharField('名称', max_length=15)
    grade = models.CharField('年级', choices = GRADE, default='5', max_length=2)
    grade_2 = models.CharField('年级2', choices = GRADE, default='6', max_length=2, null=True, blank=True)
    abandon_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='被淘汰的学期', null=True, blank=True)
    def __str__(self):
        return '《' + self.name + '》'

class Class(models.Model):
    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name
    school = models.ForeignKey(School, related_name='classes', on_delete=models.CASCADE)
    grade = models.IntegerField('年级')
    class_id = models.IntegerField('班级')
    def __str__(self):
        return (self.school.name + '%d年级%d班' % (self.grade, self.class_id))
   
    def second_start_time(self):
        return True
 
class Lecture(models.Model):
    class Meta:
        verbose_name = '课时'
        verbose_name_plural = verbose_name
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, 
                                  related_name = 'lectures', verbose_name='班级')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, verbose_name='律师', null=True, blank=True, related_name='lawyer_lectures')
    start_time = models.DateTimeField('开始时间', null=True)    
    duration = models.IntegerField('持续时间', default=40)
    def __str__(self):
        if(self.start_time):
            return self.start_time.strftime('%m{m}%d{d}').format(m='月', d='日')
        else:
            return '未确定时间'

class LawyerOfficeSemester(models.Model):
    class Meta:
        verbose_name = '各学期所在律所'
        verbose_name_plural = verbose_name
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, verbose_name='律师', related_name='lawyer_office_semesters')
    office = models.ForeignKey(LawyerOffice, on_delete=models.CASCADE, verbose_name='律所')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name='学期')

def initialize_empty_office(lawyer_p):
    s = Semester.objects.get_current()
    # to do, cache empty office
    empty_office = LawyerOffice.objects.get(name='空')
    # to do, add get_current_semester_obj func
    instance = LawyerOfficeSemester(lawyer=lawyer_p, office=empty_office, semester=Semester.objects.get(id=s['id']))
    instance.save()
