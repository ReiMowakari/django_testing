from django.conf import settings

from news.forms import CommentForm


def test_news_count(lists_of_news, get_url_news_home, client):
    """Количество новостей на главной странице — не более 10."""
    response = client.get(get_url_news_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(lists_of_news, get_url_news_home, client):
    """
    Новости отсортированы от самой свежей к самой старой
    Свежие новости в начале списка.
    """
    response = client.get(get_url_news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(lists_of_news, get_url_news_detail, client):
    """
    Комментарии на странице отдельной новости отсортированы в хронологическом
    порядке: старые в начале списка, новые — в конце.
    """
    response = client.get(get_url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    for i in range(all_comments.count() - 1):
        if all_comments[i].created > all_comments[i + 1].created:
            assert False, 'Необходимо отсортировать комментарии по возрастанию'


def test_anonymous_client_has_no_form(get_url_news_detail, client):
    """
    Анонимному пользователю недоступна форма для отправки комментария на
    странице отдельной новости.
    """
    response = client.get(get_url_news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(get_url_news_detail, author_client):
    """
    Авторизованному пользователю доступна форма для отправки комментария на
    странице отдельной новости.
    """
    response = author_client.get(get_url_news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
