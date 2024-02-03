from celery import shared_task
from requests import post
from django.conf import settings

from main.models import UsefulHabit


@shared_task
def send_message_bot(habit_id):
    """
    Отправка сообщения в телеграм-бот.
    :param habit_id: Идентификатор экземпляра модели Привычки.
    """
    habit = UsefulHabit.objects.get(id=habit_id)
    post(
        url=f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        data={
            'chat_id': habit.owner.chat_id,
            'text': f'Я буду [{habit.action}] в [{habit.time}] в [{habit.location}] !'
        }
    )
