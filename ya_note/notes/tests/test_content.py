from django.test import Client, TestCase
from django.urls import reverse

from Ya_Note.ya_note.notes.models import Note

from .test_routes import User


class TestContent(TestCase):
    """Класс для тестирования контента."""

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
        # Доп. атрибуты для получения юрл
        cls.GET_URL_NOTES_LIST = reverse('notes:list')
        cls.GET_URL_NOTES_ADD = reverse('notes:add')
        cls.GET_URL_NOTES_EDIT = reverse('notes:edit', args=(cls.note.slug,))

    def test_notes_list_for_different_users(self):
        """
        Отдельная заметка передаётся на страницу со списком заметок
        в списке object_list в словаре context,
        в список заметок одного пользователя
        не попадают заметки другого пользователя.
        """
        users_statuses = (
            (self.author_logged, True),
            (self.reader_logged, False),
        )
        for user, status in users_statuses:
            with self.subTest():
                response = user.get(self.GET_URL_NOTES_LIST)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, status)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (self.GET_URL_NOTES_ADD, self.GET_URL_NOTES_EDIT)
        for url in urls:
            with self.subTest():
                response = self.author_logged.get(url)
                self.assertIn('form', response.context)
