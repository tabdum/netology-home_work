# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer


class SensorViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    serializer_class = SensorSerializer


    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Sensor.objects.all()
        return Sensor.objects.filter(pk=pk)


class MeasurementView(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):

    serializer_class = MeasurementSerializer
    queryset = Measurement

