from django.utils import timezone

from social import models
from social import services


def procceed_not_posted_messages():
    log = models.Log.info_log()
    try:
        message_list = models.Message.objects.filter(
            date__lte=timezone.now(),
            draft=False,
            messageservicestatus__posted=False
        ).values_list('pk', flat=True)
        for message in message_list:
            log.log_update(f'post_message: {message}')
            post_message(message)
    except Exception as exc:
        log.log_update(exc)
    else:
        log.log_update(status=models.Log.STATUS_SUCCESS)


def post_message(pk):
    message = models.Message.objects.get(pk=pk)
    service_qset = message.services.filter(active=True, message__messageservicestatus__posted=False)
    for service in service_qset:
        method = getattr(services, service.name)
        data = message.profile.profileservicedata_set.get(service)
        result = method.post(text=message.text, pict=message.pict, owner=data.owner, token=data.token)
        if result:
            models.MessageServiceStatus.objects.filter(message=message, service=service).update(posted=True)
