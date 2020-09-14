from django.apps import AppConfig


class BrukereConfig(AppConfig):
    name = 'brukere'

    def ready(self):
        import brukere.signals
