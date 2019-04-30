from django.urls import path

from .views import LawyerOfficeView, LawyerDetailsView, ClassListView, ClassRegisterView

urlpatterns = [
    path('lawyeroffice/', LawyerOfficeView.as_view(), name='rest_lawyer_office'),
    path('lawyer/', LawyerDetailsView.as_view(), name='rest_lawyer_details'),
    path('class/', ClassListView.as_view(), name='rest_class_list'),
    path('class/<int:pk>/', ClassRegisterView.as_view(), name='rest_class_register')
]
