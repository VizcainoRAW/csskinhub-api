from django.core.management.base import BaseCommand
from skins.models import *

import requests

class Command(BaseCommand):
    help = "Load skin data from a JSON file or URL"
    SKINS_JSON_URL = 'https://bymykel.github.io/CSGO-API/api/en/skins.json'

    def handle(self, *args, **options):
        self.create_collections()
        self.create_rarities()
        self.create_categories()
        self.populate_crates_from_json()
        self.create_skins()


    def get_json(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error fetching data from URL: {e}'))
            return None


    def populate_crates_from_json(self) -> None:
        """Populate crates data from a JSON source."""
        crates_data = self.get_json('https://bymykel.github.io/CSGO-API/api/en/crates.json')

        for crate_data in crates_data:
            if not crate_data['type']:
                continue
            if 'Case' in crate_data['type']:
                self.create_crate_from_data(Case, crate_data)
            if 'Souvenir' in crate_data['type']:
                self.create_crate_from_data(Souvenir, crate_data)


    def create_crate_from_data(self, crate_instance:type[Crate],crate_data) -> None:
        try:   
            crate = crate_instance.objects.get_or_create(
            name=crate_data['name'],
            description=crate_data['description'],
            image=crate_data['image'],
            )[0]
            print(f'created {crate.__class__.__name__}: {crate}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating crate {crate_data["name"]}: {e}'))


    def create_collections(self):
        collections_data = self.get_json('https://bymykel.github.io/CSGO-API/api/en/collections.json')

        for collection_data in collections_data:
            self.create_collection(collection_data)


    def create_collection(self, collection_data):
        try:
            Collection.objects.get_or_create(
                name=collection_data['name'],
                image=collection_data['image'])
            print(f"Created {collection_data['name']}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating collection {collection_data["name"]}: {e}'))


    def create_categories(self):
        categories = ['Gloves', 'Knives', 'Pistols', 'SMGs', 'Heavy', 'Rifles']
        for category_name in categories:
            print(f'Created category: {Category.objects.get_or_create(name=category_name)[0]}')



    def create_rarities(self):
        rarities = ['Consumer Grade', 'Base Grade', 'Industrial Grade', 'Mil-Spec Grade', 'Restricted', 'Classified', 'Covert', 'Extraordinary', 'Rare Special', 'Gloves', 'Knives', 'Contraband']
        for rarity_name in rarities:
            print(f'created rarity: {Rarity.objects.get_or_create(name=rarity_name)[0]}')


    def create_skins(self) -> None:
        skins = self.get_json(self.SKINS_JSON_URL)

        for skin in skins:
            skin_type, skin_values = self.create_skin_info_dict(skin)
            self.create_skin(skin_type, **skin_values)


    def create_skin_info_dict(self, data):
        name = data['pattern']['name'] if data['pattern'] else 'Vanilla'
        pattern = Pattern.objects.get_or_create(name=name)[0]
        description = data['description']
        image = data['image']
        weapon = Weapon.objects.get_or_create(
            name = data['weapon']['name'],
            category = Category.objects.get(name=data['category']['name'])
            )[0]
        rarity = Rarity.objects.get(name=data['rarity']['name'])
        crates_data = data['crates']
        min_float = data['min_float'] 
        max_float = data['max_float']
        skin_type = Skin  # default 

        skin_values = {
            'name': name,
            'description': description,
            'image': image,
            'weapon': weapon,
            'rarity': rarity,
            'pattern': pattern,
            'min_float': min_float,
            'max_float': max_float
        }
        
        if crates_data:
            crate_name = data['crates'][0]['name']

            if 'Case' in crate_name:
                case = Case.objects.get(name=crates_data[0]['name'])
                skin_type = CaseSkin
                skin_values['case'] = case
            
            if 'souvenir' in crate_name:
                skin_type = SouvenirSkin
                crates = self.list_skin_crates(Souvenir, crates_data)
                skin_values['crates_list'] = crates

            return skin_type, skin_values

        if 'Knives' in data['category']['name']:
            skin_type = KniveSkin

            if crates_data:
                crates = self.list_skin_crates(Case, crates_data)
                skin_values['crates_list'] = crates
                return skin_type, skin_values

        if 'Gloves' in data['category']['name']:
            skin_type = GloveSkin

            if crates_data:
                crates = self.list_skin_crates(Case, crates_data)
                skin_values['crates_list'] = crates
                return skin_type, skin_values
        
        if data['stattrak'] and not data['souvenir']:
            case = Case.objects.last()
            skin_type = CaseSkin
            skin_values['case'] = case
            return skin_type, skin_values

        return skin_type, skin_values


    def list_skin_crates(self, crates_instance:type[Crate], crates_data):
        crates = []
        for crate in crates_data:
            try:
                crates.append( crates_instance.objects.get(name=crate['name']) )
            except Exception as e:
                print(f'append crate error, crate {crate['name']}, error: {e}')
        return crates


    def create_skin(self, skin_type:type[Skin],**skin_values):
        try:
            valid_field_names = [f.name for f in skin_type._meta.get_fields()]
            filtered_data = {k: v for k, v in skin_values.items() if k in valid_field_names}

            instance = skin_type.objects.create(**filtered_data)
            
            if  hasattr(instance, 'crates'):
                instance.crates.add(*skin_values['crates_list'])
            print(f'Created {instance.__class__.__name__}: {instance}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating {skin_type}: {skin_values["name"]}: {e}'))