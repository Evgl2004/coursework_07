from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

NULLABLE = {'null': True, 'blank': True}


class UsefulHabit(models.Model):
    """
        Модель привычек.

        Поля:
            - title: Наименование привычки.
            - owner: Внешний ключ на пользователя, создатель привычки.
            - location: Место, в котором необходимо выполнять привычку.
            - time: Время, когда необходимо выполнять привычку.
            - action: Действие, которое представляет из себя привычка.
            - is_good: Признак приятной привычки, которую можно привязать к выполнению полезной привычки.
            - related_habit: Привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
            - period: Периодичность выполнения привычки для напоминания в днях.
            - award: Описание, чем пользователь должен себя вознаградить после выполнения полезной привычки.
            - time_to_complete: Время, которое предположительно потратит пользователь на выполнение привычки.
            - is_public: Признак, указывающий, является ли привычка публичной.

        Методы:
            - __str__: Возвращает описание привычки в виде строки.
        """

    PERIOD_DAY01 = 1
    PERIOD_DAY02 = 2
    PERIOD_DAY03 = 3
    PERIOD_DAY04 = 4
    PERIOD_DAY05 = 5
    PERIOD_DAY06 = 6
    PERIOD_DAY07 = 7

    PERIODS = (
        (PERIOD_DAY01, 'раз в день'),
        (PERIOD_DAY02, 'раз в 2 дня'),
        (PERIOD_DAY03, 'раз в 3 дня'),
        (PERIOD_DAY04, 'раз в 4 дня'),
        (PERIOD_DAY05, 'раз в 5 дней'),
        (PERIOD_DAY06, 'раз в 6 дней'),
        (PERIOD_DAY07, 'раз в неделю'),
    )

    title = models.CharField(max_length=256, verbose_name='наименование')
    location = models.CharField(max_length=256, verbose_name='местоположение')
    action = models.CharField(max_length=256, verbose_name='действие')
    is_good = models.BooleanField(default=False, verbose_name='приятная')
    award = models.CharField(max_length=256, **NULLABLE, verbose_name='вознаграждение')
    is_public = models.BooleanField(default=False, verbose_name='публичная')
    period = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)],
                                 default=PERIOD_DAY01, choices=PERIODS, verbose_name='период')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='владелец')
    time_to_complete = models.DurationField(default=timedelta(seconds=120),
                                            verbose_name='продолжительность')
    time = models.TimeField(default=datetime.time(datetime.now()), **NULLABLE,
                            verbose_name='время выполнения')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, **NULLABLE,
                                      verbose_name='связанная привычка')

    def __str__(self):
        return f'{self.title} - {self.owner}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('title',)
