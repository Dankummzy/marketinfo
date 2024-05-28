# market/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import MarketData, HistoricalMarketData, CustomUser

@receiver(post_save, sender=MarketData)
def notify_participants(sender, instance, created, **kwargs):
    if created:
        # Fetch all registered users
        participants = CustomUser.objects.all()
        
        # Compose email subject and message
        subject = 'New Market Data Added'
        html_message = render_to_string('market/email_notification.html', {'market_data': instance})
        plain_message = strip_tags(html_message)
        
        # Send email to each participant
        for participant in participants:
            send_mail(subject, plain_message, 'dtkpost01@gmail.com', [participant.email], html_message=html_message)

@receiver(post_save, sender=MarketData)
def create_historical_data(sender, instance, created, **kwargs):
    if not created:
        HistoricalMarketData.objects.create(
            market_data=instance,
            price=instance.price,
            date=timezone.now()
        )
