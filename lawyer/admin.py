from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from datetime import timedelta
from .models import LawyerOffice, Lawyer, School, Class, Course, Lecture
# Register your models here.
class LawyerOfficeResource(resources.ModelResource):
    class Meta:
        model = LawyerOffice
        import_id_fields = ('name',)
        fields = ('name')

class LawyerOfficeAdmin(ImportExportModelAdmin):
    resource_class = LawyerOfficeResource

admin.site.register(LawyerOffice, LawyerOfficeAdmin)

class LectureTabInline(admin.TabularInline):
    model = Lecture
    extra = 0

class LawyerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'office')
    list_filter = ['office']
    inlines = [ LectureTabInline ]

admin.site.register(Lawyer, LawyerAdmin)

class LectureResource(resources.ModelResource):
    class Meta:
        model = Lecture
        fields =()
    school = Field(attribute='classroom__school__name', column_name='学校名称')
    grade_class_id = Field(column_name='班级')
    lawyer = Field(attribute='classroom__lawyer__user__username', column_name='授课律师')
    course = Field(attribute='course__name', column_name='课程名称')
    course_date_time = Field(column_name='授课时间')

    def dehydrate_grade_class_id(self, lecture_obj):
        class_obj = lecture_obj.classroom
        return '%s年级%s班' % (class_obj.grade, class_obj.class_id)
    def dehydrate_course_date_time(self, lecture_obj):
        start_time = lecture_obj.start_time
        if(start_time):
            date_time_str = start_time.strftime('%m{m}%d{d}%H:%M').format(m='月', d='日')
            end_time = start_time + timedelta(seconds = lecture_obj.duration * 60)
            date_time_str += '-%d:%d'%(end_time.hour, end_time.minute)
        else:
            date_time_str = '未确定时间'
        return date_time_str

    
class LawyerResource(resources.ModelResource):
    class Meta:
        model = Lawyer

class ClassInline(admin.StackedInline):
    model = Class
    extra = 1
    

class SchoolAdmin(admin.ModelAdmin):
    inlines = [ClassInline]

class IsAppliedFilter(admin.SimpleListFilter):
    title = '认领课程情况'
    parameter_name = 'isapplied'
    def lookups(self, request, model_admin):
        return(
            ('applied', '已认领课程'),
            ('not', '未认领课程')
        )
    def queryset(self, request, queryset):
        if self.value() == 'not':
            return queryset.filter(lawyer=None)
        elif self.value() == 'applied':
            return queryset.exclude(lawyer=None)

class HasUndetminedTime(admin.SimpleListFilter):
    title = '课程时间确定情况'
    parameter_name = 'undetermined'
    def lookups(self, request, model_admin):
        return(
            ('has', '有未确定时间的课程'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has':
            return queryset.filter(lectures__start_time=None)

class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 0

class ClassAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['school', 'grade', 'class_id', 'lawyer']})
    ]
    list_filter = ['school', IsAppliedFilter, HasUndetminedTime]
    list_display = ('__str__', 'lawyer')
    inlines = [LectureInline]
admin.site.register(School, SchoolAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Course)

class LectureAdmin(ImportExportModelAdmin):
    resource_class = LectureResource
    list_display = ('classroom', 'course', 'start_time')
    list_filter = ['course', 'classroom__school']
admin.site.register(Lecture, LectureAdmin)