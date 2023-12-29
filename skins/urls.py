from django.urls import path, include
from rest_framework import routers
from skins.views import CaseView

router = routers.DefaultRouter()
router.register(r'cases', CaseView, 'cases')

urlpatterns = [
    path("api/v1/", include(router.urls))
]
