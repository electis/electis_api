from typing import Union

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from social import methods


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)


class Service(models.Model):
    name = models.CharField(max_length=32, blank=True, default='')
    data_fields = models.JSONField(default={'token': []}, blank=True)
    active = models.BooleanField(default=False)


class ProfileServiceData(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    owner = models.CharField(max_length=32, default='')
    token = models.CharField(max_length=128, default='')
    # data = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('profile', 'service', 'owner')


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    text = models.TextField(default='', blank=True)
    pict = models.TextField(default='', blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    draft = models.BooleanField(default=True)


class MessageServiceStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    posted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('message', 'service')


class Log(models.Model):
    STATUS_INFO = 1
    STATUS_SUCCESS = 2
    STATUS_WARNING = 3
    STATUS_ERROR = 4
    STATUSES = (
        (STATUS_INFO, 'инфо'),
        (STATUS_SUCCESS, 'успешно'),
        (STATUS_WARNING, 'предупреждение'),
        (STATUS_ERROR, 'ошибка'),
    )
    action = models.CharField(max_length=32)
    status = models.SmallIntegerField(choices=STATUSES, default=STATUS_INFO)
    params = models.CharField(max_length=64)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.created_at} - {self.action} - {self.status}"

    def res(self):
        return self.result[:64]

    @staticmethod
    def get_func_name():
        import traceback
        stack = traceback.extract_stack()
        _, _, func_name, _ = stack[-2]
        return func_name

    @staticmethod
    def error_log(action: str, params='', result: Union[str, Exception]=''):
        if isinstance(result, Exception):
            result = methods.get_detail_exception_info(result)
        return Log.objects.create(
            action=action,
            params=str(params),
            result=str(result),
            status=Log.STATUS_ERROR
        )

    @staticmethod
    def info_log(action='', params='', result=''):
        return Log.objects.create(
            action=action or Log.get_func_name(),
            params=str(params),
            result=str(result),
            status=Log.STATUS_INFO
        )

    def log_update(self, result: Union[str, Exception]='', status: int = None):
        if isinstance(result, Exception):
            result = methods.get_detail_exception_info(result)
            if not status:
                status = Log.STATUS_ERROR
        self.result = result
        self.status = status if status is not None else self.status
        self.save(update_fields=('result', 'status', 'updated_at',))
