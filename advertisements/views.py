from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from api_with_restrictions.permissions import IsOwnerOrReadOnly




class AdvertisementFilter(FilterSet):
    created_at = DateFromToRangeFilter()


    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator']



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['creator',]
    filterset_class = AdvertisementFilter
    throttle_classes = [AnonRateThrottle]



    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        if IsAuthenticated():
            super().destroy(request, *args, **kwargs)