from django.urls import path

from .views import LawyerDetailsView, SchoolListView

urlpatterns = [
    path('lawyer/', LawyerDetailsView.as_view(), name='rest_lawyer_details'),
    path('school/', SchoolListView.as_view(), name='rest_school_list')    
]