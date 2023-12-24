from django.test import TestCase
from skins.models import *

from django.core.management import call_command

class TestSkinsModels(TestCase):
    def test_skin_import(self):
        call_command('loadbymykelskins')