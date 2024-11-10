from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'excelTipsAndTricks.accounts'

    def ready(self):
        import excelTipsAndTricks.accounts.signals
