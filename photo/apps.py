from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class PhotoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photo'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
