from skins.models import Case, Category, Skin, Weapon
from skins.serializers import CaseSerializer, CaseListSerializer, CategoryListSerializer, SkinSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView 


class CaseView(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CaseListSerializer
        else:
            return self.serializer_class

class AllDataView(viewsets.ViewSet):
   def list(self, request):
       categories = Category.objects.all()
       cases = Case.objects.all()

       categories_serializer = CategoryListSerializer(categories, many=True)
       cases_serializer = CaseListSerializer(cases, many=True)

       return Response({
           'categories': categories_serializer.data,
           'cases': cases_serializer.data
       })

class WeaponSkinsView(APIView):
    def get(self, request, weapon_id):
        try:
            weapon = Weapon.objects.get(id=weapon_id)
            skins = Skin.objects.filter(weapon=weapon)
            serializer = SkinSerializer(skins, many=True)
            return Response(serializer.data)
        except Weapon.DoesNotExist:
            return Response({"error": "Weapon not found"})