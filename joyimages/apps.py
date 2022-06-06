from django.apps import AppConfig
# from django.utils.translation import ugettext_lazy as _


class JoyimagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'joyimages'

    def ready(self):
        import joyimages.signals 