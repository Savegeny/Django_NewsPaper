from django.apps import AppConfig


class SendMailConfig(AppConfig):
    name = 'sendmail'

    def ready(self):
        import NewsPaper.news.signals


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'