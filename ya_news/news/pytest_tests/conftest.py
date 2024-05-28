import random
import pytest

from datetime import datetime, timedelta

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.test.client import Client

from news.models import Comment, News

COMMENT_TEXT = 'Текст комментария'


@pytest.fixture
def author(django_user_model):
    """Фикстура автора."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def non_author(django_user_model):
    """Фикстура не автора."""
    return django_user_model.objects.create(username='не автор')


@pytest.fixture
def author_client(author):
    """Фикстура залогининного автора."""
    # Создаём новый экземпляр клиента, чтобы не менять глобальный
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def non_author_client(non_author):
    """Фикстура залогининного не автора."""
    client = Client()
    client.force_login(non_author)
    return client


@pytest.fixture
def news():
    """Фикстура объекта новости."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def lists_of_news():
    """Фикструра для списка новостей и сортировки."""
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        one_news = News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index),
        )
        all_news.append(one_news)
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(news, author):
    """Фикстура для комментария автора."""
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=COMMENT_TEXT,
    )
    return comment


@pytest.fixture
def news_with_ten_comments(news, author):
    """Фикстура для 10 комментариев и сортировки"""
    start_date = timezone.now()
    end_date = start_date + timedelta(days=10)
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = (
            start_date + (end_date - start_date) * random.random()
        )
        comment.save()
    return news


@pytest.fixture
def get_url_news_home():
    """Получение юрл для главной страницы."""
    return reverse('news:home')


@pytest.fixture
def get_url_news_detail(news):
    """Получение юрл для подробной страницы новости."""
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def get_url_comment_edit(comment):
    """Получения юрл для страницы редактирования комментария."""
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def get_url_comment_delete(comment):
    """Получения юрл для страницы удаления комментария."""
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Фикстура для автоматического доступа к БД."""
    pass
