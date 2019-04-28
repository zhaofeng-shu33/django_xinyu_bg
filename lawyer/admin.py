from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from datetime import timedelta
from .models import Lawyer, School, Class, Course
# Register your models here.
admin.site.register(Lawyer)
class ClassResource(resources.ModelResource):
    class Meta:
        model = Class
        fields =()
    id = Field(attribute='id')
    school = Field(attribute='school__name', column_name='学校名称')
    grade_class_id = Field(column_name='班级')
    lawyer = Field(attribute='lawyer__user__username', column_name='授课律师')
    course = Field(attribute='course__name', column_name='课程名称')
    course_date_time = Field(column_name='授课时间')
    course_2 = Field(attribute='course_2__name', column_name='课程名称2')
    course_date_time_2 = Field(column_name='授课时间2')

    def dehydrate_grade_class_id(self, class_obj):
        return '%s年级%s班' % (class_obj.grade, class_obj.class_id)
    def dehydrate_course_date_time(self, class_obj):
        start_time = class_obj.start_time
        date_time_str = start_time.strftime('%m{m}%d{d}%H:%M').format(m='月', d='日')
        end_time = start_time + timedelta(seconds = class_obj.duration * 60)
        date_time_str += '-%d:%d'%(end_time.hour, end_time.minute)
        return date_time_str
    def dehydrate_course_date_time_2(self, class_obj):
        start_time = class_obj.start_time_2
        if start_time is None:
            return ''
        date_time_str = start_time.strftime('%m{m}%d{d}%H:%M').format(m='月', d='日')
        end_time = start_time + timedelta(seconds = class_obj.duration_2 * 60)
        date_time_str += '-%d:%d'%(end_time.hour, end_time.minute)
        return date_time_str
    
class LawyerResource(resources.ModelResource):
    class Meta:
        model = Lawyer

class ClassInline(admin.StackedInline):
    model = Class
    extra = 1
    list_display = ('__str__', 'lawyer') 

class SchoolAdmin(admin.ModelAdmin):
    inlines = [ClassInline]
    
class ClassAdmin(ImportExportModelAdmin):
    resource_class = ClassResource
    
admin.site.register(School, SchoolAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Course)