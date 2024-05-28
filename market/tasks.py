# market/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Alert
from django.contrib import messages


@shared_task
def check_alerts(request):
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
    messages.success(request, 'Alerts checked and notifications sent')
