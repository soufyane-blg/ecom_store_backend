from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import Product
from api.serializers import ProductSerializer
from .permissions import IsOwner


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    
    filter_backends = [SearchFilter]
    search_fields = ["name", "description"]

    
    def get_queryset(self):
        return Product.objects.filter(
            created_by=self.request.user,
            is_active=True
        )

    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    

