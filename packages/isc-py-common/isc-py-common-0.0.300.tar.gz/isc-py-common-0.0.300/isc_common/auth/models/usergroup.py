import logging

from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from isc_common import delAttr
from isc_common.auth.models.usergroup_permission import Usergroup_permission
from isc_common.auth.models.widgets_trees import Widgets_trees
from isc_common.fields.code_field import CodeField
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.models.audit import AuditManager
from isc_common.models.base_ref import BaseRef

logger = logging.getLogger(__name__)


class GroupManager(AuditManager):
    @classmethod
    def getRecord(cls, record):
        res = {
            "id": record.id,
            "code": record.code,
            "name": record.name,
            "description": record.description,
            "parent_id": record.parent_id,
            "lastmodified": record.lastmodified,
            "editing": record.editing,
            "deliting": record.deliting,
        }
        return res

    def createFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        delAttr(_data, 'dataSource')
        delAttr(_data, 'operationType')
        delAttr(_data, 'textMatchStyle')
        delAttr(_data, 'form')

        res = super().create(**_data)
        for widget in Widgets_trees.objects.all():
            Usergroup_permission.objects.get_or_create(usergroup=res, widget=widget)

        res = model_to_dict(res)
        data.update(res)
        return data


class UserGroup(BaseRef):
    code = CodeField(unique=True)
    parent = ForeignKeyProtect('self', null=True, blank=True)

    @property
    def is_admin(self):
        return self.code.lower() == 'administrators' or self.code.lower() == 'admin'

    @property
    def is_develop(self):
        return self.code == 'developers'

    def __str__(self):
        return f"{self.code}"

    objects = GroupManager()

    class Meta:
        verbose_name = _('группа')
        verbose_name_plural = _('группы')
