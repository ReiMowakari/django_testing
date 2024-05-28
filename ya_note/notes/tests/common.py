from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from .test_routes import User


class CommonTest(TestCase):
    """Общий класс для тестирования."""
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
            author=cls.author,
        )
        # Атрибут создания формы
        cls.form_data = {
            'title': 'Новый тестовый заголовок',
            'text': 'Новый тестовый текст',
            'slug': 'new-test-slug'
        }
        # Атрибут кол-ва заметок перед вызовом
        cls.NOTES_BEFORE_REQUEST = Note.objects.count()
        # Доп. атрибуты для получения юрл
        cls.GET_URL_NOTES_HOME = reverse('notes:home')
        cls.GET_URL_USERS_LOGIN = reverse('users:login')
        cls.GET_URL_USERS_LOGOUT = reverse('users:logout')
        cls.GET_URL_USERS_SIGNUP = reverse('users:signup')
        cls.GET_URL_NOTES_LIST = reverse('notes:list')
        cls.GET_URL_NOTES_ADD = reverse('notes:add')
        cls.GET_URL_NOTES_EDIT = reverse(
            'notes:edit', args=(cls.note.slug,))
        cls.GET_URL_NOTES_DELETE = reverse(
            'notes:delete', args=(cls.note.slug,))
        cls.GET_URL_NOTES_DETAIL = reverse(
            'notes:detail', args=(cls.note.slug,))
        cls.GET_URL_NOTES_SUCCESS = reverse('notes:success')
