from http import HTTPStatus

from .common import CommonTest


class TestRoutes(CommonTest):
    """Класс для тестирования маршрутов."""

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
            with self.subTest(url=url):
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
            with self.subTest(url=url):
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
                with self.subTest(client=client, status=status, url=url):
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_to_login_from_note(self):
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
            with self.subTest(url=url):
                redirect_url = f'{self.GET_URL_USERS_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
