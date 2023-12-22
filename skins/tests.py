from django.test import TestCase
from skins.models import *

from django.core.management import call_command

class TestSkinsModels(TestCase):
    def setUp(self):
        # Creating categories
        pistol_category = Category.objects.create(name="Pistol")
        mid_category = Category.objects.create(name="Mid-Tier")
        rifle_category = Category.objects.create(name="Rifles")
        knife_category = Category.objects.create(name="Knife")

        # Creating rarity
        rarities = ['Industrial Grade', 'Mil-Spec', 'Restricted', 'Classified', 'Covert']
        rarity_objects = [Rarity.objects.get_or_create(name=rarity_name)[0] for rarity_name in rarities]


        # Creating colletions
        revolution_collection = Collection.objects.create(name="Rebolution", description="A cool collection", image="https://example.com/image.jpg")
        train_collection = Collection.objects.create(name="2021 Train", description="A cool collection", image="https://example.com/image.jpg")
        anubis_collection = Collection.objects.create(name="Anubis", description="A cool collection", image="https://example.com/image.jpg")

        # Creating weapons
        awp = Weapon.objects.create(name="AWP", description="Powerful sniper rifle", image="https://example.com/awp.jpg", category=rifle_category)
        m4a4 = Weapon.objects.create(name="M4A4", description="light assault rifle", image="https://example.com/awp.jpg", category=rifle_category)
        ak47 = Weapon.objects.create(name="AK-47", description="heavy assault rifle", image="https://example.com/awp.jpg", category=rifle_category)        

        # Creating skins

        #Basic skin
        m4a4_skin = Skin.objects.create(
            name="The Coalition",
            description="skin",
            image="https://example.com/dragon-lore.jpg",
            rarity=rarity_objects[4],
            min_float=0.1,
            max_float=0.5,
            collection=train_collection,
            weapon=m4a4
        )

        #Souvenir skin
        m4a4_souvenir_skin = SouvenirSkin.objects.create(
            name="Eyes of Horus",
            description="kin",
            image="https://example.com/souvenir-dragon-lore.jpg",
            rarity=rarity_objects[4],
            min_float=0.1,
            max_float=0.5,
            collection=anubis_collection,
            weapon=m4a4
            )
        m4a4_souvenir_skin.crate.add(
            Souvenir.objects.create(
                name="Souvenir Package",
                description="A package containing souvenir items",
                image="https://example.com/souvenir-package.jpg",
                first_sale_date='2020-01-01'
                )
            )

        #Case skin
        m4a4_case_skin = CaseSkin.objects.create(
            name="Temukau",
            description="skin",
            image="https://example.com/stattrak-dragon-lore.jpg",
            rarity=rarity_objects[4],
            min_float=0.1,
            max_float=0.5,
            collection=revolution_collection,
            weapon=m4a4,
            crate=Case.objects.create(
                name="Sticker Capsule",
                description="A capsule containing stickers",
                image="https://example.com/sticker-capsule.jpg",
                first_sale_date='2020-01-01'
            )
        )

    def test_skin_creation(self):
        self.assertEqual(Skin.objects.count(), 3)
        self.assertEqual(SouvenirSkin.objects.count(), 1)
        self.assertEqual(CaseSkin.objects.count(), 1)
    
    def setUp(self):
        call_command('loadbymykelskins')