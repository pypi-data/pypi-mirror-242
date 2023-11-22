from django.apps import AppConfig


class NemoPublicationsConfig(AppConfig):
    name = "NEMO_publications"

    def ready(self):
        """
        This code will be run when Django starts.
        """
        pass
