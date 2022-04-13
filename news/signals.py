from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import SendMail


@receiver(post_save, sender=SendMail)
def notify_managers_news(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Post change for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )

post_save.connect(notify_managers_news, sender=SendMail)