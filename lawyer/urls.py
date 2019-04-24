from django.urls import path

from .views import LawyerDetailsView, SchoolListView, ClassListView, ClassRegisterView

urlpatterns = [
    path('lawyer/', LawyerDetailsView.as_view(), name='rest_lawyer_details'),
    path('school/', SchoolListView.as_view(), name='rest_school_list'),
    path('class/', ClassListView.as_view(), name='rest_class_list'),
    path('class/<int:pk>/', ClassRegisterView.as_view(), name='rest_class_register')
]