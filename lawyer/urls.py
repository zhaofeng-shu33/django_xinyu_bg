from django.urls import path

from .views import LawyerDetailsView

urlpatterns = [
    path('lawyer/', LawyerDetailsView.as_view(), name='rest_lawyer_details')
]