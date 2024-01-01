from rest_framework import serializers, generics
from skins.models import Case, CaseSkin, Category, Rarity, Weapon

class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = ['id','name']

class WeaponSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Weapon
        fields = ['id','name']

class SkinSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(many=False, read_only=True)
    rarity = RaritySerializer(many=False, read_only=True)

    class Meta:
        model = CaseSkin
        fields = ['id','name','image','weapon','rarity']

class CaseSerializer(serializers.ModelSerializer):
    skins = SkinSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ['id','name','description','image','skins']

class CaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id', 'name','image']

class CategoryListSerializer(serializers.ModelSerializer):
    weapons = WeaponSerializer(source='weapon_set', many=True)

    class Meta:
        model = Category
        fields = ['id','name','weapons']
