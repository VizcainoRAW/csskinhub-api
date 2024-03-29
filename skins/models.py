from audioop import reverse

from urllib.parse import quote

from django.db import models
from django.utils.translation import gettext_lazy as _

#Steam Item, abstract class with the commons fields
class SteamItem(models.Model):
    name = models.TextField(_("Name"))
    description = models.TextField(_("Description"), blank=True, null=True)
    image = models.URLField(_("Image URL"), default='non url')

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name

#Ceate, Abstract class for extend cases, capsules, packages, etc.
class Crate(SteamItem):

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
    
class Rarity(models.Model):
    name = models.TextField(_("Rarity name"))
    
    class Meta:
        verbose_name = _("Rarity")
        verbose_name_plural = _("Raritys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rarity_detail", kwargs={"pk": self.pk})

class Pattern(models.Model):
    name = models.TextField(_("Name"))

    class Meta:
        verbose_name = _("Pattern")
        verbose_name_plural = _("Patterns")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Pattern_detail", kwargs={"pk": self.pk})

class Collection(SteamItem):
    pass

class Case(Crate):

    class Meta:
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")

    def get_absolute_url(self):
        return reverse("Case_detail", kwargs={"pk": self.pk})

class Souvenir(Crate):

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
    name = models.TextField(_("Name"), default='vanilla')
    weapon = models.ForeignKey(Weapon, verbose_name=_("Weapon"), on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, verbose_name=_("Rarity"), on_delete=models.CASCADE)
    pattern = models.ForeignKey(Pattern, verbose_name=_("Pattern"), on_delete=models.CASCADE, null=True)
    min_float = models.FloatField(_("Minimum Float"), null=True)
    max_float = models.FloatField(_("Maximum Float"),null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _("Skin")
        verbose_name_plural = _("Skins")

    def get_absolute_url(self):
        return reverse("Skin_detail", kwargs={"pk": self.pk})
    
    def get_steam_selling_list(self):
        steam_selling_url_list = []
        self._get_steam_selling_urls(steam_selling_url_list)
        return steam_selling_url_list
    
    def _get_steam_selling_urls(self, url_list):
        condition_list = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
        steamcommunity_selling_url = 'https://steamcommunity.com/market/listings/730/'

        for condition in condition_list:
            steam_selling_url = f'{steamcommunity_selling_url}{quote(f'{self.weapon.name} | {self.name} ({condition})')}'
            url_list.append(steam_selling_url)

        return url_list

    
    def __str__(self):
        return self.weapon.name + " | " + self.name

class CrateSkin(Skin):
    SPECIAL_CONDITION = None

    class Meta:
        abstract = True

    def get_steam_selling_list(self):
        url_list = super().get_steam_selling_list()
        if self.SPECIAL:
            self._get_steam_selling_urls(url_list, pre_condition_name = self.SPECIAL_CONDITION)
        
        return url_list
    
    def _get_steam_selling_urls(self, url_list):
        condition_list = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
        steamcommunity_selling_url = f'https://steamcommunity.com/market/listings/730/{self.SPECIAL_CONDITION}'

        for condition in condition_list:
            steam_selling_url = f'{steamcommunity_selling_url}{quote(f'{self.weapon.name} | {self.name} ({condition})')}'
            url_list.append(steam_selling_url)

        return url_list

class SouvenirSkin(CrateSkin):
    crates = models.ManyToManyField(Souvenir, verbose_name=_("Soubenir packages"))
    SPECIAL_CONDITION = 'Souvenir'

class CaseSkin(CrateSkin):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name=_("Case"))
    SPECIAL_CONDITION = 'StatTrak™'

class RareSkin(CrateSkin):
    crates = models.ManyToManyField(Case, verbose_name=_("Cases"))

    class meta:
        abstract = True

class GloveSkin(RareSkin):
    pass

class KniveSkin(RareSkin):
    SPECIAL_CONDITION = 'StatTrak™'