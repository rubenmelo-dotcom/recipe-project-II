from django.apps import AppConfig


class RecipesConfig(AppConfig):
    name = 'recipes'

    def ready(self):
        import recipes.signals  # noqa
        super_ready =  super().ready()
        return super_ready
