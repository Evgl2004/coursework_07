from rest_framework import serializers
from datetime import timedelta


def one_of_related_habit_or_award(value):
    """
    Проверка на запрет использования одновременно связанной привычки и вознаграждения.
    :param value: Словарь с реквизитами входных данных модели Привычки.
    :return: Ошибка в случае одновременного использования связанной привычки и вознаграждения.
    """
    if (value.get('related_habit') is not None
            and value.get('award') is not None):
        raise serializers.ValidationError('Исключить одновременный выбор связанной привычки и указания вознаграждения.')


def time_to_complete_no_more_120seconds(value):
    """
    Проверка на запрет использования времени выполнения привычки более 2-х минут.
    :param value: Словарь с реквизитами входных данных модели Привычки.
    :return: Ошибка в случае превышения времени выполнения более 2-х минут.
    """
    if value['time_to_complete'] > timedelta(minutes=2):
        raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')


def only_good_habit_into_related_habit(value):
    """
    Проверка на запрет использования в связанных привычка не приятные привычки.
    :param value: Словарь с реквизитами входных данных модели Привычки.
    :return: Ошибка в случае использования в связанной привычке не приятную привычку
    (привычку с признаком Приятная = Ложь).
    """
    if (value.get('related_habit') is not None
            and not value['related_habit'].is_good):
        raise serializers.ValidationError('В связанные привычки могут попадать только привычки '
                                          'с признаком приятной привычки.')


def good_habit_cannot_have_award_or_related_habit(value):
    """
    Проверка на запрет использования в приятных привычках вознаграждения или связанной привычки.
    :param value: Словарь с реквизитами входных данных модели Привычки.
    :return: Ошибка в случае использования в приятных привычках вознаграждения или связанной привычки.
    """
    if (value['is_good'] and
            ((value.get('related_habit') is not None
              or value.get('award') is not None))):
        raise serializers.ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
