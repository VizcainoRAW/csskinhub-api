from django.urls import path, include
from rest_framework import routers
from skins.views import CaseView, AllDataView, WeaponSkinsView

router = routers.DefaultRouter()
router.register(r'cases', CaseView, basename='case')

urlpatterns = [
    path('weapon/<int:weapon_id>/skins/', WeaponSkinsView.as_view(), name='weapon-skins'),
    path('all/', AllDataView.as_view({'get': 'list'})),
    path("", include(router.urls), name='case-list'),
]