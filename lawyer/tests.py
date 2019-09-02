from django.test import TestCase
from django.contrib.auth.models import User
from .models import Lawyer, Semester, initialize_empty_office, LawyerOffice, Semester, School, Class, Lecture, Course
from datetime import datetime
# Create your tests here.
def create_necessary_test_data():
        # create current Semester
        s = Semester(name='2019', end_date=datetime.now())
        s.save()
        # create empty office
        o = LawyerOffice(name='空')
        o.save()
        # create the user first
        u = User.objects.create_user('testuser', 'test@example.org', 'pd')
        u.save()
        # create the lawyer
        p = Lawyer(user=u)
        p.save()
        initialize_empty_office(p)
        # create the school
        sch = School(name='testschool')
        sch.save()
        # create the class
        cla = Class(school=sch, grade='6', class_id='1')
        cla.save()
        # create the course
        cour = Course(name='coursename')
        cour.save()
        # create the lecture
        lec = Lecture(classroom=cla, course=cour, lawyer=p, start_time=datetime.now(), duration=40)
        lec.save()

class LawyerModelTests(TestCase):
    def test_can_bind_lawyer_with_user(self):
        create_necessary_test_data()
        p = Lawyer.objects.get(user__username='testuser')        
        s = Semester.objects.get_current()
        office_semester = p.lawyer_office_semesters.get(semester__id = s['id'])
        self.assertTrue(office_semester.office.name == '空')