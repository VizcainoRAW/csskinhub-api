from rest_framework import serializers
from skins.models import Case, CaseSkin, Category, Rarity, Weapon

class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Rarity
        fields = ['id','name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class WeaponSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    
    class Meta:
        model = Weapon
        fields = ['id','name','category']

class CaseSkinSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(many=False, read_only=True)
    rarity = RaritySerializer(many=False, read_only=True)

    class Meta:
        model = CaseSkin
        fields = ['id','name','image','weapon','rarity']

class CaseSerializer(serializers.ModelSerializer):
    skins = CaseSkinSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ['id','name','description','image','skins']