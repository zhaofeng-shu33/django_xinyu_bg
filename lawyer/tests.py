from django.test import TestCase
from django.contrib.auth.models import User
from .models import Lawyer, Semester, initialize_empty_office, LawyerOffice, Semester
from datetime import datetime
# Create your tests here.

class LawyerModelTests(TestCase):
    def test_can_bind_lawyer_with_user(self):
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
        # assert
        self.assertIs(p.user.username, 'testuser')
        
        s = Semester.objects.get_current()
        office_semester = p.lawyer_office_semesters.get(semester__id = s['id'])
        self.assertTrue(office_semester.office.name == '空')