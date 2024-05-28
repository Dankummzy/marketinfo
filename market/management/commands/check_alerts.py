# market/management/commands/check_alerts.py
from django.core.management.base import BaseCommand
from market.models import Alert
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Check alerts and send notifications'

    def handle(self, *args, **kwargs):
        alerts = Alert.objects.filter(notified=False)
        for alert in alerts:
            condition_met = False  # Implement your condition check logic here
            if condition_met:
                send_mail(
                    'Market Alert',
                    f'Alert for {alert.market_data.product_name}',
                    'from@marketinfo.com',
                    [alert.user.email],
                )
                alert.notified = True
                alert.save()
        self.stdout.write(self.style.SUCCESS('Alerts checked and notifications sent'))
