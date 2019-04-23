from django.urls import path

from .views import LawyerDetailsView, SchoolListView, ClassListView

urlpatterns = [
    path('lawyer/', LawyerDetailsView.as_view(), name='rest_lawyer_details'),
    path('school/', SchoolListView.as_view(), name='rest_school_list'),
    path('class/', ClassListView.as_view(), name='rest_class_list')        
]