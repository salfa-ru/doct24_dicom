""" Модуль общих серилизаторов проекта  """
import datetime as dt
import time
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


def to_stemp(value):

    if (isinstance(value, dt.datetime)):
        value = dt.datetime(
            value.year, value.month, value.day,
            value.hour, value.minute, value.second
        )

    try:
        result = time.mktime(value.timetuple())
    except ValueError:
        return ValidationError(
            'time - не допустимое значение времени datetime ')

    return int(result)


class TimestampField(serializers.IntegerField):
    def to_representation(self, value):
        return to_stemp(value)


# self.request.data['user']['birthday']

def to_date(value):
    """ Преобразование числа timeshtemp в формат даты"""
    if isinstance(value, datetime):
        return value
    date_ts = value
    try:
        date_result = datetime.fromtimestamp(date_ts)
    except ValueError:
        return ValidationError(
            'time - не допустимое значение времени timeshtemp '
            'с точностью до секунды')

    return date_result


def to_datetime(value):
    """ Преобразование числа timeshtemp в формат даты и времени"""
    date_ts = int(value)
    datetime_result = dt.datetime.fromtimestamp(date_ts)
    return datetime_result


class TimestampToDataField(serializers.IntegerField):
    value = serializers.IntegerField()

    def to_internal_value(self, data):
        if not isinstance(data, int):
            self.fail('invalid')
        return to_date(data)

    def to_representation(self, value):
        return value
