from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import time, timedelta

from main.models import UsefulHabit
from users.models import User
from django_celery_beat.models import PeriodicTask


class UsefulHabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru', password='test', chat_id='1234567890')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.course_id_01 = UsefulHabit.objects.create(
            title='Привычка №01',
            location='Кухня',
            action='Съесть яблоко',
            is_good=True,
            is_public=False,
            period=1,
            time_to_complete=timedelta(seconds=120),
            owner=self.user
        )

        self.course_id_02 = UsefulHabit.objects.create(
            title='Привычка №02',
            location='Ванна',
            action='Чистить зубы',
            is_good=False,
            is_public=False,
            period=1,
            time_to_complete=timedelta(seconds=120),
            time=time(7, 30),
            award='Завтрак',
            owner=self.user
        )

        self.course_id_03 = UsefulHabit.objects.create(
            title='Привычка №03',
            location='Спальня',
            action='Делать зарядку',
            is_good=False,
            is_public=True,
            period=1,
            time_to_complete=timedelta(seconds=90),
            time=time(21, 30),
            related_habit=self.course_id_01,
            owner=self.user
        )

    def test_create_habit_error_required_field(self):
        """
            Тестирование ошибки не заполнения обязательного поля при создании экземпляра модели Привычка.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '17:35'}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'action': ['Обязательное поле.']}
        )

    def test_create_habit_error_validator_one_of_related_habit_or_award(self):
        """
            Тестирование ошибки использования одновременно связанной привычки и вознаграждения.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место', 'action': 'Зарядка для глаз',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '17:35', 'award': 'Успех!', 'related_habit': self.course_id_01.id}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Исключить одновременный выбор связанной '
                                  'привычки и указания вознаграждения.']}
        )

    def test_create_habit_error_validator_time_to_complete_no_more_120seconds(self):
        """
            Тестирование ошибки использования времени выполнения привычки более 2-х минут.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место', 'action': 'Зарядка для глаз',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 999,
                      'time': '17:35', 'award': 'Успех!'}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд.']}
        )

    def test_create_habit_error_validator_only_good_habit_into_related_habit(self):
        """
            Тестирование ошибки использования в связанных привычках не приятные привычки.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место', 'action': 'Зарядка для глаз',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 120,
                      'time': '17:35', 'related_habit': self.course_id_02.id}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['В связанные привычки могут попадать только привычки с '
                                  'признаком приятной привычки.']}
        )

    def test_create_habit_error_validator_good_habit_cannot_have_award_or_related_habit(self):
        """
            Тестирование ошибки использования в приятных привычках вознаграждения или связанной привычки.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место', 'action': 'Зарядка для глаз',
                      'is_good': 'True', 'is_public': 'True', 'period': 1, 'time_to_complete': 120,
                      'time': '17:35', 'related_habit': self.course_id_01.id}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEquals(
            response.json(),
            {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']}
        )

    def test_create_habit(self):
        """
            Тестирование создания экземпляра модели Привычка.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место', 'action': 'Зарядка для глаз',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '17:35'}

        response = self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(
            response.json(),
            {'id': self.course_id_03.id + 1, 'title': 'Привычка №04', 'location': 'Любое место',
             'action': 'Зарядка для глаз', 'is_good': False, 'award': None, 'is_public': True, 'period': 1,
             'time_to_complete': '00:01:00', 'time': '17:35:00', 'owner': 1, 'related_habit': None}
        )

    def test_create_habit_periodic_task(self):
        """
            Тестирование создания регламентной задачи при создании экземпляра модели Привычка.
        """
        data_habit = {'title': 'Привычка №04', 'location': 'Любое место', 'action': 'Зарядка для глаз',
                      'is_good': 'False', 'is_public': 'True', 'period': 1, 'time_to_complete': 60,
                      'time': '17:35'}

        self.client.post(
            '/create/',
            data=data_habit
        )

        self.assertEquals(
            PeriodicTask.objects.filter(name=f'HabitTask{self.course_id_03.id + 1}').exists(),
            True
        )

    def test_list_habit(self):
        """
            Тестирование отображения реквизитов списка экземпляров модели Привычка принадлежащих Владельцу
        """
        response = self.client.get(
            '/list/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json().get('count') is not None and response.json().get('count') == 3,
            True
        )

    def test_view_habit(self):
        """
            Тестирование отображения реквизитов одного экземпляра модели Привычка.
        """
        response = self.client.get(
            f'/view/{self.course_id_02.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.course_id_02.id, 'title': self.course_id_02.title,
             'location': self.course_id_02.location, 'action': self.course_id_02.action,
             'is_good': self.course_id_02.is_good, 'award': self.course_id_02.award,
             'is_public': self.course_id_02.is_public, 'period': self.course_id_02.period,
             'time_to_complete': '0'+str(self.course_id_02.time_to_complete),
             'time': str(self.course_id_02.time),
             'owner': self.user.id, 'related_habit': None}
        )

    def test_update_habit(self):
        """
            Тестирование обновления данных (редактирование) экземпляра модели Привычка.
        """
        data = {'id': self.course_id_02.id, 'title': 'Изменим название для теста!',
                'location': self.course_id_02.location, 'action': self.course_id_02.action,
                'is_good': self.course_id_02.is_good, 'award': self.course_id_02.award,
                'is_public': self.course_id_02.is_public, 'period': self.course_id_02.period,
                'time_to_complete': self.course_id_02.time_to_complete, 'time': self.course_id_02.time,
                'owner': self.user.id}

        response = self.client.patch(
            f'/edit/{self.course_id_02.id}/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.course_id_02.id, 'title': 'Изменим название для теста!',
             'location': self.course_id_02.location, 'action': self.course_id_02.action,
             'is_good': self.course_id_02.is_good, 'award': self.course_id_02.award,
             'is_public': self.course_id_02.is_public, 'period': self.course_id_02.period,
             'time_to_complete': '0'+str(self.course_id_02.time_to_complete),
             'time': str(self.course_id_02.time),
             'owner': self.user.id, 'related_habit': None}
        )

    def test_delete_habit(self):
        """
            Тестирование удаления экземпляра модели Привычка.
        """
        response = self.client.delete(
            f'/delete/{self.course_id_02.id}/',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_list_habit_public(self):
        """
            Тестирование отображения реквизитов списка экземпляров модели Привычка с признакам "Публичные".
        """
        response = self.client.get(
            '/list_public/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json()[0].get('id') is not None and response.json()[0].get('id') == self.course_id_03.id,
            True
        )

    def tearDown(self):
        UsefulHabit.objects.all().delete()
