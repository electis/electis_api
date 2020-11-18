from django.utils import timezone

from social import models
from social import services


def proceed_not_posted_messages():
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
        if message_list:
            result = f'posted {len(message_list)} messages'
        else:
            result = 'no messages to post'
        log.log_update(result=result, status=models.Log.STATUS_SUCCESS)


def post_message(pk):
    message = models.Message.objects.get(pk=pk)
    service_qset = message.services.filter(active=True, message__messageservicestatus__posted=False)
    for service in service_qset:
        method = getattr(services, service.name)()
        data = message.profile.profileservicedata_set.get(service=service)
        result = method.post(text=message.text, pict=message.pict, owner=data.owner, token=data.token)
        if result:
            status, _ = models.MessageServiceStatus.objects.get_or_create(message_id=pk, service=service)
            status.posted = True
            status.posted_at = timezone.now()
            status.data['post_id'] = result
            status.save()
