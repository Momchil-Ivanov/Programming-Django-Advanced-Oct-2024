from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'excelTipsAndTricks.accounts'

    def ready(self):
        import excelTipsAndTricks.accounts.signals
