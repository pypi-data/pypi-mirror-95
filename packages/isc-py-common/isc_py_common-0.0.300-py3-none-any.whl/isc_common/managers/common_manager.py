import logging
from typing import List

from bitfield import Bit, BitHandler
from django.core.exceptions import EmptyResultSet
from django.db import connection, transaction
from django.db.models import Manager, QuerySet, Q, ForeignKey
from django.forms import model_to_dict

from isc_common import delAttr, setAttr
from isc_common.bit import TurnBitOn, TurnBitOff
from isc_common.fields.related import ForeignKeyProtect
from isc_common.http.DSRequest import DSRequest
from isc_common.number import DelProps

logger = logging.getLogger(__name__)


class CommonQuerySet(QuerySet):

    def soft_restore(self):
        res = super().update(deleted_at=None)
        return res

    def hard_delete(self):
        res = super().delete()
        return res

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

    def __init__(self, model=None, query=None, using=None, hints=None, alive_only=True, enabledAll=False):
        self.alive_only = alive_only
        self.enabledAll = enabledAll
        super().__init__(model=model, query=query, using=using, hints=hints)

    def get_field(self, field_name):
        fld = [x for x in self.model._meta.fields if x.name == field_name]
        if len(fld) > 0:
            return fld[0]
        return None

    def get_id_tuple(self, group):
        iter = [x for x in group]
        # print(iter)
        res = [x[1] for x in iter if x[0][1] == 'id']
        if len(res) > 0:
            return res[0]
        return None

    def getRecord(self, record):
        return record

    def getOperator(self, operator):
        if operator == "and":
            return Q.AND
        elif operator == "or":
            return Q.OR
        elif operator == "equals":
            return "exact"
        elif operator == "iEquals":
            return "iexact"
        elif operator == "notEqual":
            return "exact"
        elif operator == "iNotEqual":
            return "iexact"
        elif operator == "greaterThan":
            return "gt"
        elif operator == "lessThan":
            return "lt"
        elif operator == "greaterOrEqual":
            return "gte"
        elif operator == "lessOrEqual":
            return "lte"
        elif operator == "contains":
            return "contains"
        elif operator == "startsWith":
            return "startswith"
        elif operator == "endsWith":
            return "endswith"
        elif operator == "iContains":
            return "icontains"
        elif operator == "iStartsWith":
            return "istartswith"
        elif operator == "iEndsWith":
            return "iendswith"
        elif operator == "notContains":
            return "contains"
        elif operator == "notStartsWith":
            return "startswith"
        elif operator == "notEndsWith":
            return "endswith"
        elif operator == "iNotContains":
            return "icontains"
        elif operator == "iNotStartsWith":
            return "istartswith"
        elif operator == "iNotEndsWith":
            return "endswith"
        elif operator == "iBetween":
            return "range"
        elif operator == "iBetweenInclusive":
            return "range"
        elif operator == "matchesPattern":
            return "regex"
        elif operator == "iMatchesPattern":
            return "iregex"
        elif operator == "containsPattern":
            return "regex"
        elif operator == "startsWithPattern":
            return "regex"
        elif operator == "endsWithPattern":
            return "regex"
        elif operator == "iContainsPattern":
            return "iregex"
        elif operator == "iStartsWithPattern":
            return "iregex"
        elif operator == "iEndsWithPattern":
            return "iregex"
        elif operator == "regexp":
            return "regex"
        elif operator == "iregexp":
            return "iregex"
        elif operator == "isBlank":
            return "isblank"
        elif operator == "notBlank":
            return "notblank"
        elif operator == "isNull":
            return "isnull"
        elif operator == "notNull":
            return "notnull"
        elif operator == "inSet":
            return "in"
        elif operator == "notInSet":
            return "in"
        # elif operator == "equalsField":
        #     return ""
        # elif operator == "notEqualField":
        #     return ""
        # elif operator == "iEqualsField":
        #     return ""
        # elif operator == "iNotEqualField":
        #     return ""
        # elif operator == "greaterThanField":
        #     return ""
        # elif operator == "lessThanField":
        #     return ""
        # elif operator == "greaterOrEqualField":
        #     return ""
        # elif operator == "lessOrEqualField":
        #     return ""
        # elif operator == "containsField":
        #     return ""
        # elif operator == "startsWithField":
        #     return ""
        # elif operator == "endsWithField":
        #     return ""
        # elif operator == "iContainsField":
        #     return ""
        # elif operator == "iStartsWithField":
        #     return ""
        # elif operator == "iEndsWithField":
        #     return ""
        # elif operator == "notContainsField":
        #     return ""
        # elif operator == "notStartsWithField":
        #     return ""
        # elif operator == "notEndsWithField":
        #     return ""
        # elif operator == "iNotContainsField":
        #     return ""
        # elif operator == "iNotStartsWithField":
        #     return ""
        # elif operator == "iNotEndsWithField":
        #     return ""
        # elif operator == "not":
        #     return ""
        elif operator == "between":
            return "range"
        elif operator == "nbetweenInclusiveot":
            return "range"
        else:
            raise Exception(f'Неизветный operator: {operator}')

    def isNotOperator(self, operator):
        if operator == "notEqual":
            return True
        if operator == "iNotEqual":
            return True
        if operator == "notContains":
            return True
        if operator == "notStartsWith":
            return True
        if operator == "notEndsWith":
            return True
        if operator == "iNotContains":
            return True
        if operator == "iNotStartsWith":
            return True
        if operator == "iNotEndsWith":
            return True
        if operator == "notBlank":
            return True
        if operator == "notNull":
            return True
        if operator == "notInSet":
            return True
        if operator == "notEqualField":
            return True
        if operator == "iNotEqualField":
            return True
        if operator == "notContainsField":
            return True
        if operator == "notStartsWithField":
            return True
        if operator == "notEndsWithField":
            return True
        if operator == "iNotContainsField":
            return True
        if operator == "iNotStartsWithField":
            return True
        if operator == "iNotEndsWithField":
            return True
        if operator == "not":
            return True
        else:
            return False

    def textMatchStyleMapping(self, textMatchStyle):
        if textMatchStyle == 'exact':
            return 'iexact'
        elif textMatchStyle == 'exactCase':
            return 'exact'
        elif textMatchStyle == 'substring':
            return 'icontains'
        elif textMatchStyle == 'startsWith':
            return 'istartswith'
        else:
            return 'exact'
            # raise Exception(f'Неизветный textMatchStyle: {textMatchStyle}')

    def getValue(self, criterion):
        value = criterion.get('value')
        operator = criterion.get('operator')
        if value is None:
            if operator == "isNull":
                return True
            elif operator == "notNull":
                return True
            elif operator == "isBlank":
                return "''"
            elif operator == "notBlank":
                return "''"
            else:
                return value

        if isinstance(value, str):
            return value.strip()
        elif isinstance(value, int):
            return value
        elif isinstance(value, list):
            return value
        else:
            raise Exception(f'Неизветный value: {value}')

    def getCriteria(self, crireria, operator):
        res = Q()
        if isinstance(crireria, list):
            # <editor-fold desc="Fixed by Y.Andrew">
            criteria = [item for item in crireria if item.get('fieldName') != 'ts']
            # </editor-fold>

            for criterion in criteria:
                _criteria = criterion.get("criteria")
                if _criteria:
                    if self.isNotOperator(operator):
                        res.add(~Q(self.getCriteria(_criteria, criterion.get("operator"))), operator)
                    else:
                        res.add(Q(self.getCriteria(_criteria, criterion.get("operator"))), operator)
                elif criterion.get('fieldName') != 'ts':
                    _operator = self.getOperator(criterion.get('operator'))
                    if _operator == "notnull":
                        _operator = "isnull"

                    if _operator == 'isblank' or _operator == 'notblank':
                        _operator = ''
                    else:
                        _operator = f'__{_operator}'

                    if self.isNotOperator(criterion.get('operator')):
                        res.add(~Q(**{f"{criterion.get('fieldName')}{_operator}": self.getValue(criterion)}), operator)
                    else:
                        if _operator == '__icontains':
                            if self.getValue(criterion) != '':
                                res.add(Q(**{f"{criterion.get('fieldName')}{_operator}": self.getValue(criterion)}), operator)
                        else:
                            res.add(Q(**{f"{criterion.get('fieldName')}{_operator}": self.getValue(criterion)}), operator)

        return res

    def delete_underscore_element(self, data):
        if not isinstance(data, dict):
            raise Exception('data must be dict')

        res = dict()
        for key, value in data.items():
            if str(key).find('_', 0, 1) == -1:
                setAttr(res, key, value)
        return res

    def get_criteria(self, json=dict()):

        if json is None:
            data = dict()
        else:
            data = json.get('data', dict())
        _data = dict()
        if data is not None:
            for key, value in data.items():
                if value is not None and key != 'full_name':
                    setAttr(_data, key, value)
        data = _data
        delAttr(data, 'ts')

        # fields_name = [field.name for field in self.model._meta.fields]
        _data = data.copy()
        delAttr(_data, 'guid')
        for key, value in data.items():
            if key.find('__id') == -1 and key.find('_id') != -1:
                if len([item.name for item in self.model._meta.fields if item.name == key]) == 0:
                    delAttr(_data, key)
                    setAttr(_data, key.replace('_id', '__id'), value)
            elif isinstance(value, str) and value.strip() == '':
                delAttr(_data, key)

        data = _data

        criteria = Q()
        operator = Q.AND

        if data.get('_constructor') == 'AdvancedCriteria':
            operator = self.getOperator(data.get("operator"))
            _criteria = data.get("criteria")
            if self.isNotOperator(data.get("operator")):
                criteria.add(~Q(self.getCriteria(_criteria, operator)), operator)
            else:
                criteria.add(Q(self.getCriteria(_criteria, operator)), operator)
        else:
            # "exact"	case-insensitive exact match ("foo" matches "foo" and "FoO", but not "FooBar")  iexact
            # "exactCase"	case-sensitive exact match ("foo" matches only "foo")                       exact
            # "substring"	case-insenstive substring match ("foo" matches "foobar" and "BarFoo")       icontains
            # "startsWith"	case-insensitive prefix match ("foo" matches "FooBar" but not "BarFoo")     istartswith
            textMatchStyle = self.textMatchStyleMapping(json.get('textMatchStyle'))
            for key, value in data.items():
                if isinstance(value, Bit):
                    criteria.add(Q(**{f"{key}": value}), operator)
                elif isinstance(value, list):
                    criteria.add(Q(**{f"{key}__in": value}), operator)
                else:
                    if textMatchStyle == "iexact" and isinstance(value, int):
                        textMatchStyle = "exact"

                    if isinstance(value, int) or isinstance(value, bool):
                        criteria.add(Q(**{f"{key}": value}), operator)
                    elif value == 'null':
                        criteria.add(Q(**{f"{key}__isnull": True}), operator)
                    else:
                        criteria.add(Q(**{f"{key}__{textMatchStyle}": value}), operator)
        return criteria

    def _get_range_rows(self, *args, **kwargs):
        json = kwargs.get('json')
        distinct_field_names = kwargs.get('distinct_field_names')
        end = kwargs.get('end')
        start = kwargs.get('start')

        criteria = self.get_criteria(json=json)
        # print(f'json: {json}')
        # print(f'self.alive_only: {self.alive_only}')

        ob = json.get("sortBy", [])

        if isinstance(distinct_field_names, tuple) or (isinstance(distinct_field_names, list)):
            if self.alive_only == False:
                if start is not None and end is not None:
                    queryResult = super().filter(*args, criteria).distinct(*distinct_field_names)[start:end]
                elif start is not None and end is None:
                    queryResult = super().filter(*args, criteria).distinct(*distinct_field_names)[start:]
                elif end is not None and start is None:
                    queryResult = super().filter(*args, criteria).distinct(*distinct_field_names)[:end]
                else:
                    queryResult = super().filter(*args, criteria).distinct(*distinct_field_names)
            else:
                if start is not None and end is not None:
                    queryResult = super().filter(*args, criteria).filter(deleted_at__isnull=True).distinct(*distinct_field_names)[start:end]
                elif start is not None and end is None:
                    queryResult = super().filter(*args, criteria).filter(deleted_at__isnull=True).distinct(*distinct_field_names)[start:]
                elif end is not None and start is None:
                    queryResult = super().filter(*args, criteria).filter(deleted_at__isnull=True).distinct(*distinct_field_names)[:end]
                else:
                    queryResult = super().filter(*args, criteria).filter(deleted_at__isnull=True).distinct(*distinct_field_names)
        else:
            if self.alive_only == False:
                if start is not None and end is not None:
                    queryResult = super().order_by(*ob).filter(*args, criteria).distinct()[start:end]
                elif start is not None and end is None:
                    queryResult = super().order_by(*ob).filter(*args, criteria)[start:]
                elif end is not None and start is None:
                    queryResult = super().order_by(*ob).filter(*args, criteria)[:end]
                else:
                    queryResult = super().order_by(*ob).filter(*args, criteria)
            else:
                if start is not None and end is not None:
                    queryResult = super().order_by(*ob).filter(*args, criteria).filter(deleted_at__isnull=True)[start:end]
                elif start is not None and end is None:
                    queryResult = super().order_by(*ob).filter(*args, criteria).filter(deleted_at__isnull=True)[start:]
                elif end is not None and start is None:
                    queryResult = super().order_by(*ob).filter(*args, criteria).filter(deleted_at__isnull=True)[:end]
                else:
                    queryResult = super().order_by(*ob).filter(*args, criteria).filter(deleted_at__isnull=True)
        return queryResult

    def get_range_rows(self, start=None, end=None, function=None, json=None, distinct_field_names=None, user=None, *args, **kwargs):
        queryResult = self._get_range_rows(*args, start=start, end=end, function=function, json=json, distinct_field_names=distinct_field_names)

        try:
            logger.debug(f'\n\n{queryResult.query}\n')
        except EmptyResultSet:
            pass

        if function:
            res = [function(record) for record in queryResult]
            return res
        else:
            res = [model_to_dict(record) for record in queryResult]
            return res

    def get_range_rows1(self, request, function=None, distinct_field_names=None, remove_fields=None):
        request = DSRequest(request=request)
        if isinstance(remove_fields, list):
            data = request.json.get('data')
            deleted = False
            for remove_field in remove_fields:
                if delAttr(data, remove_field) == True:
                    deleted = True
            if deleted == True:
                setAttr(request.json, 'data', data)

        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        res = self.get_range_rows(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            criteria=request.get_criteria(),
            user=request.user
        )
        return res

    def get_range_rows2(self, *args, **kwargs):
        function = kwargs.get('function')
        user_id = kwargs.get('user_id')
        username = kwargs.get('username')
        ws_channel = kwargs.get('ws_channel')
        ws_port = kwargs.get('ws_port')
        host = kwargs.get('host')
        queryResult = self._get_range_rows(*args, **kwargs)

        try:
            logger.debug(f'\n\n{queryResult.query}\n')
        except Exception as ex:
            logger.warning(ex)

        if function:
            res = [function(record=record, user_id=user_id, ws_channel=ws_channel, ws_port=ws_port, host=host, username=username) for record in queryResult]
            return res
        else:
            res = [model_to_dict(record) for record in queryResult]
            return res

    def get_range_rows3(self, start=None, end=None, function=None, json=None, distinct_field_names=None, user=None, *args, **kwargs):
        queryResult = self._get_range_rows(*args, start=start, end=end, function=function, json=json, distinct_field_names=distinct_field_names)

        logger.debug(f'\n\n{queryResult.query}\n')
        if function:
            res = [function(record, self.enabledAll) for record in queryResult]
            return res
        else:
            res = [model_to_dict(record) for record in queryResult]
            return res

    def get_range_rows11(self, request, **kwargs):
        distinct_field_names = kwargs.get('distinct_field_names')
        function = kwargs.get('function')

        request = DSRequest(request=request)
        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        return self.get_range_rows2(
            start=request.startRow,
            end=request.endRow,
            function=function,
            distinct_field_names=distinct_field_names,
            json=request.json,
            username=request.username,
            user_id=request.user_id,
            ws_channel=request.ws_channel,
            ws_port=request.ws_port,
            host=request.host,
        )

    def get_info(self, request, *args):
        request = DSRequest(request=request)
        delAttr(request.json.get('data'), 'full_name')
        criteria = self.get_criteria(json=request.json)
        cnt = super().filter(*args, criteria).count()
        cnt_all = super().filter().count()
        return dict(qty_rows=cnt, all_rows=cnt_all)


class CommonManager(Manager):
    @classmethod
    def delete_underscore_element(cls, data):
        if not isinstance(data, dict):
            raise Exception('data must be dict')

        res = dict()
        for key, value in data.items():
            if str(key).find('_', 0, 1) == -1:
                setAttr(res, key, value)
        return res

    def delete_dbl_underscore_element(self, data):
        if not isinstance(data, dict):
            raise Exception('data must be dict')

        res = dict()
        for key, value in data.items():
            if str(key).find('_', 0, 1) == -1 and str(key).find('__') == -1:
                setAttr(res, key, value)
        return res

    def refresh_mat_view(self, mat_view):
        with connection.cursor() as cursor:
            logger.debug(f'Refreshing: {mat_view}')
            cursor.execute(f'REFRESH MATERIALIZED VIEW CONCURRENTLY {mat_view};')
            logger.debug(f'Refreshed')

    def get_field(self, field_name, model=None):
        if not model:
            model = self.model

        fld = [x for x in model._meta.fields if x.name == field_name]
        if fld and len(fld) > 0:
            return fld

        if field_name.rfind('_id') + 3 == len(field_name):
            fld = [x for x in model._meta.fields if x.name == field_name.replace('_id', '')]
            if fld and len(fld) > 0:
                return fld

        list_foreign = field_name.split('__')
        if len(list_foreign) > 1:
            list_foreign, spliter = [x.split('_') for x in list_foreign], '__'
        else:
            list_foreign, spliter = field_name.split('_'), '_'

        if len(list_foreign) > 1:
            if isinstance(list_foreign, list):
                for _list_foreign in list_foreign:
                    if isinstance(_list_foreign, list):
                        fld = self.get_field(spliter.join(_list_foreign))
                    else:
                        fld = [x for x in model._meta.fields if x.name == _list_foreign]
                        if len(fld) == 1 and isinstance(fld[0], ForeignKeyProtect):
                            fld = self.get_field(spliter.join(list_foreign[1:]), model=fld[0].related_model)
                        else:
                            break
        else:
            fld = [x for x in model._meta.fields if x.name == field_name]
        if fld and len(fld) > 0:
            return fld

        return None

    def get_queryset(self):
        return CommonQuerySet(self.model, using=self._db)

    def get_range_rows1(self, request, function=None, distinct_field_names=None):
        request = DSRequest(request=request)
        self.alive_only = request.alive_only
        self.enabledAll = request.enabledAll
        return self.get_queryset().get_range_rows(start=request.startRow, end=request.endRow, function=function, distinct_field_names=distinct_field_names, json=request.json)

    def createFromRequest(self, request, removed=None, propsArr: List = None):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()

        if _data.get('parent') is not None and isinstance(_data.get('parent'), int):
            setAttr(_data, 'parent_id', _data.get('parent'))
            delAttr(_data, 'parent')

        delAttr(_data, 'dataSource')
        delAttr(_data, 'operationType')
        delAttr(_data, 'textMatchStyle')
        delAttr(_data, 'form')
        self._remove_prop(_data, removed)

        props = self.get_prp(data=_data, propsArr=propsArr)
        if props > -1:
            setAttr(_data, 'props', props)

        res = super().create(**_data)
        try:
            full_name = res.full_name
        except:
            full_name = None
        res = model_to_dict(res)
        if full_name:
            setAttr(res, 'full_name', full_name)

        setAttr(res, 'isFolder', False)
        data.update(DelProps(res))
        return data

    def _dataIsArray(self, data):
        return isinstance(data, list)

    def _remove_prop(self, data, removed):
        if isinstance(data, dict) and isinstance(removed, list):
            for removed_item in removed:
                delAttr(data, removed_item)

    def _remove_prop_(self, data):
        res = None
        if isinstance(data, dict):
            res = dict()
            for key in data.keys():
                if not key.startswith('_'):
                    setAttr(res, key, data.get(key))
        return res

    def clone_data(self, data):
        _data = dict()
        if isinstance(data, dict):
            for key, val in data.items():
                if self.get_field(key):
                    setAttr(_data, key, val)
        return _data

    def get_prp(self, data, propsArr, props_name='props'):
        if isinstance(data, dict):
            props = data.get(props_name, 0)
            if isinstance(propsArr, list):
                idx = 0
                for prop in propsArr:
                    _prop = data.get(prop)

                    if _prop == True:
                        props = TurnBitOn(props, idx)
                    else:
                        props = TurnBitOff(props, idx)

                    delAttr(data, prop)
                    idx += 1
                return props
            else:
                return -1
        return -1

    def check_data_for_multi_select(self, data):
        for k, v in data.items():
            if k == '0':
                data = v
            break
        return data

    def updateFromRequest(self, request, removed=None, function=None, propsArr: List = None):
        if not isinstance(request, DSRequest):
            request = DSRequest(request=request)
        data = request.get_data()

        data = self.check_data_for_multi_select(data=data)

        _data = data.copy()

        if self._dataIsArray(data):
            data = list(data.values())
            for data_item in data:
                self._remove_prop(data_item, removed)
                data_item = self._remove_prop_(data_item)
                if isinstance(data_item, dict):
                    if function:
                        function(data, data_item)
                    else:
                        props = self.get_prp(data=data_item, propsArr=propsArr)
                        cloned_data = self.clone_data(data)
                        if props > -1:
                            setAttr(cloned_data, 'props', props)

                        if data_item.get('id'):
                            super().update_or_create(id=data_item.get('id'), defaults=cloned_data)
                        else:
                            super().create(**cloned_data)
        else:
            self._remove_prop(data, removed)
            data = self._remove_prop_(data)
            if function:
                function(data)
            else:
                props = self.get_prp(data=data, propsArr=propsArr)
                cloned_data = self.clone_data(data)

                if props > -1:
                    setAttr(cloned_data, 'props', props)

                id = cloned_data.get('id')
                if id is not None:
                    delAttr(cloned_data, 'id')
                    parent = cloned_data.get('parent')
                    if isinstance(parent, int):
                        delAttr(cloned_data, 'parent')
                        setAttr(cloned_data, 'parent_id', parent)
                    res = super().filter(id=id).update(**cloned_data)
                    print(f'res: {res}')
                else:
                    new_item = super().create(**cloned_data)
                    setAttr(_data, 'id', new_item.id)
        return _data

    def copyFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        old = self.get(id=data.get('id'))
        _old = model_to_dict(old)
        delAttr(_old, 'id')
        _old1 = dict()

        for key, value in _old.items():
            if isinstance(self.get_field(key), ForeignKey):
                setAttr(_old1, f'{key}_id', value)
            else:
                setAttr(_old1, key, value)

        _old = _old1

        for field_name in [field.name for field in old._meta.fields if field._unique == True]:
            num = 1
            value = None
            while True:
                try:
                    value = _old.get(field_name)
                    if isinstance(value, str):
                        value = f'{_old.get(field_name)}-{num}'
                        eval(f'self.get({field_name}="{value}")', dict(self=self))
                    else:
                        break
                    num += 1
                except old.DoesNotExist:
                    setAttr(_old, field_name, value)
                    break

        for unique_together in old._meta.unique_together:
            num = 1
            get_dict = dict()
            while True:
                try:
                    get_str = ""
                    for unique_together_item in unique_together:
                        value = _old.get(f'{unique_together_item}_id')
                        if isinstance(self.get_field(unique_together_item), ForeignKey):
                            get_str += f'{unique_together_item}_id={value},'
                            setAttr(_old, f'{unique_together_item}_id', value)
                            delAttr(_old, unique_together_item)
                        elif isinstance(value, int):
                            value += 1
                            get_str += f'{unique_together_item}={value},'
                            setAttr(dict, unique_together_item, value)
                        else:
                            value = f'{_old.get(unique_together_item)}-{num}'
                            get_str += f'{unique_together_item}="{value}",'
                            setAttr(get_dict, unique_together_item, value)

                    eval(f'self.get({get_str})', dict(self=self))
                    num += 1
                except old.DoesNotExist:
                    for key, val in get_dict.items():
                        setAttr(_old, key, val)
                    break

        kwargs = dict()
        for key, val in _old.items():
            # if key.find('_id') != -1:
            field = self.get_field(key)
            if isinstance(field, list):
                field = field[0]
            if field is not None:
                if isinstance(field, ForeignKey):
                    setAttr(kwargs, f'{key}_id', val)
                else:
                    setAttr(kwargs, key, val)
            # else:
            #     setAttr(kwargs, key, val)

        new = self.create(**kwargs)
        setAttr(_old, 'id', new.id)
        return _old

    def lookupFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()

        _data = dict()
        _key = None

        for key, value in data.items():
            if key.find('__') != -1:
                if value == 'null':
                    setAttr(_data, key[key.find('__') + 2:], None)
                else:
                    setAttr(_data, key[key.find('__') + 2:], value)
                _key = key[: key.find('__')]
                # break

        field = self.get_field(_key)
        res = None
        if isinstance(field, list):
            field = field[0]

        if field:
            # if field.null:
            if field is None:
                setAttr(_data, 'id', None)
                res = _data
            else:
                _data = {k: v for k, v in _data.items() if v is not None}
                if isinstance(_data, dict) and len(_data) > 0:
                    try:
                        res = field.related_model.objects.filter(**_data)
                        if len(res) >= 1:
                            res = res[0]
                            res = model_to_dict(res)
                            for key, value in data.items():
                                if str(key).find('full_name') != -1:
                                    setAttr(res, 'full_name', value)
                    except Exception as ex:
                        logger.error(ex)
                else:
                    logger.warning(f'Element {_data} not found')

        _res = dict()
        if isinstance(res, dict):
            for key, value in res.items():
                if not isinstance(value, list) and not isinstance(value, dict):
                    if isinstance(value, BitHandler):
                        props = res.get('props')._value
                        setAttr(_res, 'props', props)
                    else:
                        setAttr(_res, key, value)
        return _res

    def deleteFromRequest(self, request, removed=None, ):
        request = DSRequest(request=request)
        res = 0
        tuple_ids = request.get_olds_tuple_ids()
        with transaction.atomic():
            for id, mode in tuple_ids:
                if mode == 'hide':
                    super().filter(id=id).soft_delete()
                    res += 1
                elif mode == 'visible':
                    super().filter(id=id).soft_restore()
                else:
                    qty, _ = super().filter(id=id).delete()
                    res += qty
        return res

    def get_ex(self, *args, **kwargs):
        """
        Perform the query and return a single object matching the given
        keyword arguments.
        """
        clone = super().get_queryset().filter(*args, **kwargs)
        num = len(clone)
        if num >= 1:
            return clone._result_cache
        if not num:
            return None
        return None
