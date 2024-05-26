from http import HTTPStatus


from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from Ya_Note.ya_note.notes.models import Note


# Получение объекта пользователя
User = get_user_model()


class TestRoutes(TestCase):
    """Класс для тестирования маршрутов."""

    @classmethod
    def setUpTestData(cls):
        """Добавляем в класс необходимые атрибуты."""
        # Атрибуты, связанные с пользователями
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.author_logged = Client()
        cls.reader_logged = Client()
        cls.author_logged.force_login(cls.author)
        cls.reader_logged.force_login(cls.reader)
        # Атрибут создания заметки
        cls.note = Note.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='test-slug',
            author=cls.author
        )
        # Доп. атрибуты для получения юрл
        cls.GET_URL_NOTES_HOME = reverse('notes:home')
        cls.GET_URL_USERS_LOGIN = reverse('users:login')
        cls.GET_URL_USERS_LOGOUT = reverse('users:logout')
        cls.GET_URL_USERS_SIGNUP = reverse('users:signup')
        cls.GET_URL_NOTES_LIST = reverse('notes:list')
        cls.GET_URL_NOTES_ADD = reverse('notes:add')
        cls.GET_URL_NOTES_SUCCESS = reverse('notes:success')
        cls.GET_URL_NOTES_DETAIL = reverse(
            'notes:detail', args=(cls.note.slug,))
        cls.GET_URL_NOTES_EDIT = reverse(
            'notes:edit', args=(cls.note.slug,))
        cls.GET_URL_NOTES_DELETE = reverse(
            'notes:delete', args=(cls.note.slug,))

    def test_pages_availability(self):
        """
        Тестирование доступности страниц для анонимного пользователя:
        Главная, регистрация, вход и выход.
        """
        urls = (
            self.GET_URL_NOTES_HOME,
            self.GET_URL_USERS_LOGIN,
            self.GET_URL_USERS_LOGOUT,
            self.GET_URL_USERS_SIGNUP,
        )
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        """
        Аутентифицированному пользователю доступны:
        страница со списком заметок,
        страница успешного добавления заметки,
        страница добавления новой заметки.
        """
        urls = (
            self.GET_URL_NOTES_LIST,
            self.GET_URL_NOTES_ADD,
            self.GET_URL_NOTES_SUCCESS,
        )
        for url in urls:
            with self.subTest():
                response = self.reader_logged.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        """
        Страницы отдельной заметки, удаления и редактирования заметки
        доступны только автору заметки. Если на эти страницы попытается
        зайти чужой пользователь — вернётся ошибка 404.
        """
        users_statuses = (
            (self.author_logged, HTTPStatus.OK),
            (self.reader_logged, HTTPStatus.NOT_FOUND),
        )
        for client, status in users_statuses:
            for url in (
                    self.GET_URL_NOTES_DETAIL,
                    self.GET_URL_NOTES_EDIT,
                    self.GET_URL_NOTES_DELETE
            ):
                with self.subTest():
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def redirect_to_login_from_note(self):
        """
        Редирект на страницу логина при попытке перейти
        на страницу комментария через анонимного пользователя.
        """
        urls = (
            self.GET_URL_NOTES_DETAIL,
            self.GET_URL_NOTES_EDIT,
            self.GET_URL_NOTES_DELETE,
            self.GET_URL_NOTES_ADD,
            self.GET_URL_NOTES_SUCCESS,
            self.GET_URL_NOTES_LIST,
        )
        for url in urls:
            with self.subTest():
                redirect_url = f'{self.GET_URL_USERS_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
