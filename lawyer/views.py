from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .serializer import LawyerDetailSerializer, ClassViewSerializer, ClassApplySerializer
from .models import Lawyer, Class

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

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

class ClassListView(ListAPIView):
    queryset = Class.objects.all()
    pagination_class = StandardResultsSetPagination
    serializer_class = ClassViewSerializer
    
class ClassRegisterView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Class.objects.all()
    serializer_class = ClassApplySerializer
