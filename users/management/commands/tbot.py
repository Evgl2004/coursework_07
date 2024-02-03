from django.core.management import BaseCommand

from main.tasks import send_message_bot


class Command (BaseCommand):
    """
        Тестирование отправки сообщений в Телеграм.
    """

    def handle(self, *args, **options):
        send_message_bot(14)
