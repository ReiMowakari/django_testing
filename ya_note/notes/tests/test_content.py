from .common import CommonTest


class TestContent(CommonTest):
    """Класс для тестирования контента."""

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
            with self.subTest(user=user, status=status):
                response = user.get(self.GET_URL_NOTES_LIST)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, status)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = (self.GET_URL_NOTES_ADD, self.GET_URL_NOTES_EDIT)
        for url in urls:
            with self.subTest(url=url):
                response = self.author_logged.get(url)
                self.assertIn('form', response.context)
