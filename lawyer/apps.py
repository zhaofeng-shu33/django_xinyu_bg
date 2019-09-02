from django.apps import AppConfig
import os

class LawyerConfig(AppConfig):
    name = 'lawyer'
    verbose_name = '律师'
    path = os.path.dirname(__file__)