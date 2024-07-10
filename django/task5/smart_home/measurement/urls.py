from django.urls import path, include
from rest_framework import routers

from measurement.views import SensorViewSet, MeasurementView

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet, basename='sensors')
router.register(r'measurements', MeasurementView, basename='measurement')


urlpatterns = [
    path('', include(router.urls)),
]
