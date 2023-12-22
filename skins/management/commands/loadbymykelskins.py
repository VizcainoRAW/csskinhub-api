from django.core.management.base import BaseCommand
from skins.models import *

import requests

class Command(BaseCommand):
    help = "Cargar datos de skins desde un archivo JSON o una URL"

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            dest='url', 
            type=str, 
            default='https://bymykel.github.io/CSGO-API/api/en/skins.json', 
            help='URL para descargar el archivo JSON'
        )

    def handle(self, *args, **options):
        self.create_collections()
        self.create_categories()
        self.create_crates()
        self.create_skins()

    def get_json(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error al obtener datos desde la URL: {e}'))
            return None
    
    def clear_string(self, string:str, part:int, character):
        return string.split(character)[part].strip()

    def create_crates(self):
        crates = self.get_json('https://bymykel.github.io/CSGO-API/api/en/crates.json')

        for crate in crates:
            if crate['type']:
                if 'Case' in crate['type']:
                    self.create_crate(Case, crate)
                
                if 'Souvenir' in crate['type']:
                    self.create_crate(Souvenir, crate)

    def create_crate(self, crate_instance: type[Crate], json):
        try:
            crate_instance.objects.get_or_create(
                name=json['name'],
                description=json['description'],
                image=json['image'],
                first_sale_date='2020-01-01'
            )
            print(f"created {json['name']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la caja {json["name"]}: {e}'))

    def create_collections(self):
        collections = self.get_json('https://bymykel.github.io/CSGO-API/api/en/collections.json')

        for collection in collections:
            self.create_collection(collection)

    def create_collection(self, json):
        try:
            Collection.objects.get_or_create(name=json['name'], image=json['image'])
            print(f"created {json['name']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la colección {json["name"]}: {e}'))

    def create_categories(self):
        categories = ['Knives', 'Pistols', 'SMGs', 'Heavy', 'Rifles']

        categories_objects = [Rarity.objects.get_or_create(name=category_name)[0] for category_name in categories]

        return categories_objects

    def create_rarities(self):
        rarities = ['Consumer Grade', 'Base Grade', 'Industrial Grade', 'Mil-Spec', 'Restricted', 'Classified', 'Covert', 'Extraordinary', 'Rare Special', 'Gloves', 'Knives', 'Contraband']

        rarity_objects = [Rarity.objects.get_or_create(name=rarity_name)[0] for rarity_name in rarities]

        return rarity_objects

    def create_skins(self):
        skins = self.get_json('https://bymykel.github.io/CSGO-API/api/en/skins.json')

        for skin in skins:
            category = skin['category']['name']
            crate = skin['crates']

            if 'Knive' in category:
                self.create_rare_skin(skin, KniveSkin)

            elif 'Gloves' in category:
                self.create_rare_skin(skin, GloveSkin)

            elif crate:
                crate_name = skin['crates'][0]['name']
                print(crate_name)

                if 'Case' in crate_name:
                    self.create_case_skin(skin)
                if 'Souvenir' in crate_name:
                    self.create_souvenir_skin(skin)
            else:
                self.create_skin(skin)

    def create_skin(self, skin):
        try:
            Skin.objects.get_or_create(
                name=self.clear_string(string=skin['name'], character='|', part=1),
                description=skin['description'],
                image=skin['image'],
                weapon=Weapon.objects.get_or_create(
                    name=skin['weapon']['name'],
                    category=Category.objects.get(name=skin['category']['name'])
                )[0],
                rarity=Rarity.objects.get(name=skin['rarity']['name'].replace('Mil-spec Grade','Mil-spec').strip()),
                pattern=Pattern.objects.get_or_create(name=skin['pattern']['name'])[0],
                collection=Collection.objects.get(name=skin['collections'][0]['name']),
                min_float=skin['min_float'],
                max_float=skin['max_float']
            )
            print(f"created {skin['name']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la skin {skin["name"]}: {e}'))

    def create_case_skin(self, skin):
        try:
            CaseSkin.objects.get_or_create(
                name=self.clear_string(string=skin['name'], character='|', part=1),
                description=skin['description'],
                image=skin['image'],
                weapon=Weapon.objects.get_or_create(
                    name=skin['weapon']['name'],
                    category=Category.objects.get_or_create(name=skin['category']['name'])[0]
                )[0],
                rarity=Rarity.objects.get_or_create(name=skin['rarity']['name'])[0],
                pattern=Pattern.objects.get_or_create(name=skin['pattern']['name'])[0],
                collection=Collection.objects.get(name=skin['collections'][0]['name']),
                crate=Case.objects.get(name=skin['crates'][0]['name']),
                min_float=skin['min_float'],
                max_float=skin['max_float']
            )
            print(f"created {skin['name']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la skin de caja {skin["name"]}: {e}'))

    def create_souvenir_skin(self, skin):
        try:
            SouvenirSkin.objects.get_or_create(
                name=self.clear_string(string=skin['name'], character='|', part=1),
                description=skin['description'],
                image=skin['image'],
                weapon=Weapon.objects.get_or_create(
                    name=skin['weapon']['name'],
                    category=Category.objects.get_or_create(name=skin['category']['name'])[0]
                )[0],
                rarity=Rarity.objects.get_or_create(name=skin['rarity']['name'])[0],
                pattern=Pattern.objects.get_or_create(name=skin['pattern']['name'])[0],
                collection=Collection.objects.get(name=skin['collections'][0]['name']),
                min_float=skin['min_float'],
                max_float=skin['max_float']
            )
            print(f"created {skin['name']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la Souvenir skin: {skin["name"]}: {e}'))
    
    def create_rare_skin(self, skin, skin_instance:type[RareSkin]):
        try: 
            created_skin = skin_instance.objects.get_or_create(
            name=self.clear_string(string=skin['name'], character='|', part=1),
            description=skin['description'],
            image=skin['image'],
            weapon=Weapon.objects.get_or_create(
                name=skin['weapon']['name'],
                category=Category.objects.get_or_create(name=skin['category']['name'])[0]
            )[0],
            rarity=Rarity.objects.get_or_create(name=skin['rarity']['name'])[0],
            pattern=Pattern.objects.get_or_create(name=skin['pattern']['name'])[0],
            min_float=skin['min_float'],
            max_float=skin['max_float']
            )[0]
            for case in skin['crates']:
                created_skin.crate.add( Case.objects.get(name=case['name']) )
                print(f"created {skin['name']}")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al crear la Souvenir skin: {skin["name"]}: {e}'))


        