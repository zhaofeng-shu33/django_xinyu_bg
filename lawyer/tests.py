from datetime import datetime
import unittest
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Lawyer, Semester, initialize_empty_office, LawyerOffice, Semester, School, Class, Lecture, Course
from .admin import LectureResource
from .cleanse import unpack_class_name, parse_time
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

class ClassModelTests(TestCase):
    def test_class_manager_get_class(self):
        create_necessary_test_data()
        cc = Class.objects.get_class('testschool', '6年级1班')
        self.assertTrue(cc is not None)
        cc2 = Class.objects.get_class('testschool2', '6年级1班')
        self.assertTrue(cc2 is None)
        cc3 = Class.objects.get_class('testschool', '7年级1班')
        self.assertTrue(cc3 is None)

class LawyerModelTests(TestCase):
    def test_can_bind_lawyer_with_user(self):
        create_necessary_test_data()
        p = Lawyer.objects.get(user__username='testuser')        
        s = Semester.objects.get_current()
        office_semester = p.lawyer_office_semesters.get(semester__id = s['id'])
        self.assertTrue(office_semester.office.name == '空')

class LectureIOTest(TestCase):
    def test_import_export_lectures_data(self):
        create_necessary_test_data()
        dataset = LectureResource().export()
        new_row = list(dataset[0])
        new_row[1] = '6年级2班'
        dataset.append(new_row)
        result = LectureResource().import_data(dataset, dry_run=True, raise_errors=True)
    def test_non_raise_error(self):
        create_necessary_test_data()
        dataset = LectureResource().export()
        new_row = list(dataset[0])
        new_row[1] = '6年级二班'
        dataset.append(new_row)
        result = LectureResource().import_data(dataset, dry_run=True, raise_errors=False)
        self.assertTrue(result.has_errors())
        self.assertTrue(isinstance(result.row_errors()[0][1][0].error, NameError))

class CleansingTest(unittest.TestCase):
    def test_cleanse_class_name(self):
        right_class_name_1 = '4年级5班'
        grade_id, class_id = unpack_class_name(right_class_name_1)
        self.assertEqual(grade_id, 4)
        self.assertEqual(class_id, 5)
        right_class_name_2 = '3年级11班'
        grade_id, class_id = unpack_class_name(right_class_name_2)
        self.assertEqual(grade_id, 3)
        self.assertEqual(class_id, 11)
        wrong_class_name = '五年级三班'
        try:
            grade_id, class_id = unpack_class_name(wrong_class_name)
        except NameError:
            pass
    def test_cleanse_datetime(self):
        right_datetime_1 = '4月2日15:30-16:10';
        dt, duration = parse_time(right_datetime_1)
        dt = timezone.localtime(dt)
        self.assertEqual(dt.month, 4)
        self.assertEqual(dt.day, 2)
        self.assertEqual(dt.hour, 15)
        self.assertEqual(dt.minute, 30)
        self.assertEqual(duration, 40)
        negative_datetime_1 = '4月26日 15：30-16:10'
        try:
            dt, duration = parse_time(right_datetime_1)
        except NameError:
            pass