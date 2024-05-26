import pytest

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',
    (
        'news:home',
        'users:login',
        'users:logout',
        'users:signup',
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name):
    """
    Тестирование доступности страниц для анонимного пользователя:
    Главная, регистрация, вход и выход.
    """
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_detail_page_availability(get_url_news_detail, client):
    """Страница отдельной новости доступна анонимному пользователю."""

    response = client.get(get_url_news_detail)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    #Список фикстур авторизованного автора и неавторизованного.
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('non_author_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'get_url',
    #Список фикстур получения юрл для редактирования и удаления комментария.
    (
        pytest.lazy_fixture('get_url_comment_edit'),
        pytest.lazy_fixture('get_url_comment_delete'),
    ),
)
def test_pages_availability_for_different_users(
        parametrized_client, get_url, expected_status
):
    """
    Страницы удаления и редактирования комментария доступны
    только автору комментария.
    Авторизованный пользователь не может зайти на страницы редактирования
    или удаления чужих комментариев (возвращается ошибка 404).
    """
    response = parametrized_client.get(get_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'get_url',
    (
        pytest.lazy_fixture('get_url_comment_edit'),
        pytest.lazy_fixture('get_url_comment_delete'),
    ),
)
@pytest.mark.django_db
def redirect_to_login_from_comments(get_url, url_user_login, client):
    """
    Редирект на страницу логина при попытке перейти
    на страницу комментария через анонимного пользователя.
    """
    expected_url = f'{url_user_login}?next={get_url}'
    response = client.get(get_url)
    assertRedirects(response, expected_url)
