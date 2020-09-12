from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'CoreRepetition.users'

    def ready(self):
        from . import signals
