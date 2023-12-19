from audioop import reverse

from django.db import models
from django.utils.translation import gettext_lazy as _

#Steam Item, abstract class with the commons fields
class SteamItem(models.Model):
    name = models.TextField(_("Name"))
    description = models.TextField(_("Description"), blank=True, null=True)
    image = models.URLField(_("Image URL"))

    class Meta:
        abstract = True

#Ceate, Abstract class for extend cases, capsules, packages, etc.
class Create(SteamItem):
    first_sale_date = models.DateField(_("First Sale Date"))

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

class Collection(SteamItem):
    pass

class Category(models.Model):
    name = models.TextField(_("category name"))    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Case(Create):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")

    def get_absolute_url(self):
        return reverse("Case_detail", kwargs={"pk": self.pk})

class Souvenir(Create):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Souvenir")
        verbose_name_plural = _("Souvenirs")

    def get_absolute_url(self):
        return reverse("Souvenir_detail", kwargs={"pk": self.pk})

class Weapon(SteamItem):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Weapon")
        verbose_name_plural = _("Weapons")

    def get_absolute_url(self):
        return reverse("Weapon_detail", kwargs={"pk": self.pk})

class Skin(SteamItem):
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    rarity = models.CharField(_("Rarity"), max_length=50)
    pattern_string = models.CharField(_("Pattern String"), max_length=50)
    min_float = models.FloatField(_("Minimum Float"))
    max_float = models.FloatField(_("Maximum Float"))
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Skin")
        verbose_name_plural = _("Skins")

    def get_absolute_url(self):
        return reverse("Skin_detail", kwargs={"pk": self.pk})

    def get_steam_selling_list(self):
        steam_selling_url_list=[]
        self._get_steam_selling_urls(steam_selling_url_list)
        return steam_selling_url_list
        
    def _get_steam_selling_urls(self, url_list):
        condition_list = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
        steamcommunity_selling_url = 'https://steamcommunity.com/market/listings/730/'

        for condition in condition_list:
            condition_slug = condition.lower().replace(' ', '-')
            skin_name_slug = self.name.lower().replace(' ', '%20')
            steam_selling_url = f'{steamcommunity_selling_url}{self.weapon.name}{skin_name_slug}{condition_slug}'
            url_list.append(steam_selling_url)
        return url_list
    
    def __str__(self):
        return self.weapon.name + " | " + self.name

class CreateSkin(Skin):
    create = models.ForeignKey(Create, on_delete=models.CASCADE)
    SPECIAL_CONDITION = None

    class Meta:
        abstract = True

    def get_steam_selling_list(self):
        url_list = super().get_steam_selling_list()
        if self.SPECIAL:
            self._get_steam_selling_urls(url_list, pre_condition_name = self.SPECIAL_CONDITION)
        
        return url_list
    
    def _get_steam_selling_urls(self, url_list, special_condition_name):
        condition_list = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
        steamcommunity_selling_url = f'https://steamcommunity.com/market/listings/730/{special_condition_name}'

        for condition in condition_list:
            condition_slug = condition.lower().replace(' ', '-')
            skin_name_slug = self.name.lower().replace(' ', '%20')
            steam_selling_url = f'{steamcommunity_selling_url}{self.weapon.name}{skin_name_slug}{condition_slug}'
            url_list.append(steam_selling_url)
        return url_list

        

class SouvenirSkin(CreateSkin):
    create = models.ForeignKey(Souvenir, on_delete=models.CASCADE)
    SPECIAL_CONDITION = 'Souvenir'

class CaseSkin(CreateSkin):
    create = models.ForeignKey(Case, on_delete=models.CASCADE)
    SPECIAL_CONDITION = 'StatTrak™'