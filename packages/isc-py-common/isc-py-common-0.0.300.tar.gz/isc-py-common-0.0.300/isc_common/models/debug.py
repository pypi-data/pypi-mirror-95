import logging

from django.db.models import TextField, Model

logger = logging.getLogger(__name__)


class Debug(Model):
    params = TextField(null=True, blank=True)
    text = TextField()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Отладочная информация'
