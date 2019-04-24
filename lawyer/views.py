from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializer import LawyerDetailSerializer, SchoolSerializer, ClassViewSerializer, ClassApplySerializer
from .models import Lawyer, Class, School
# Create your views here.
class LawyerDetailsView(RetrieveUpdateAPIView):
    serializer_class = LawyerDetailSerializer
    permission_classes = (IsAuthenticated, )
    def get_object(self):
        try:
            return Lawyer.objects.get(user=self.request.user)
        except Lawyer.DoesNotExist:
            p = Lawyer(user=self.request.user)
            p.save()
            return p
class SchoolListView(ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class ClassListView(ListAPIView):
    queryset = Class.objects.order_by('-start_time')
    serializer_class = ClassViewSerializer
    
class ClassRegisterView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Class.objects.all()
    serializer_class = ClassApplySerializer