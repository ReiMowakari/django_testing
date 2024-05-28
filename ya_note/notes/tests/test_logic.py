from http import HTTPStatus
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .common import CommonTest


class TestLogicNote(CommonTest):
    """Класс для тестирования логики."""

    def test_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку."""
        response = self.author_logged.post(
            self.GET_URL_NOTES_ADD,
            data=self.form_data
        )
        self.assertRedirects(response, self.GET_URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST + 1)
        new_note = Note.objects.order_by('id').last()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        response = self.client.post(
            self.GET_URL_NOTES_ADD, data=self.form_data)
        expected_url = (f'{self.GET_URL_USERS_LOGIN}'
                        f'?next={self.GET_URL_NOTES_ADD}')
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST)

    def test_not_unique_slug(self):
        """Невозможно создать две заметки с одинаковым slug."""
        self.form_data['slug'] = self.note.slug
        response = self.author_logged.post(
            self.GET_URL_NOTES_ADD,
            data=self.form_data
        )
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST)

    def test_empty_slug(self):
        """
        Если при создании заметки не заполнен slug, то он формируется
        автоматически, с помощью функции pytils.translit.slugify.
        """
        self.form_data.pop('slug')
        response = self.author_logged.post(
            self.GET_URL_NOTES_ADD,
            data=self.form_data
        )
        self.assertRedirects(response, self.GET_URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST + 1)
        new_note = Note.objects.order_by('id').last()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_can_edit_note(self):
        """Пользователь может редактировать свои заметки."""
        response = self.author_logged.post(
            self.GET_URL_NOTES_EDIT,
            data=self.form_data
        )
        self.assertRedirects(response, self.GET_URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        """Пользователь не может редактировать чужие заметки."""
        response = self.reader_logged.post(
            self.GET_URL_NOTES_EDIT,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        """Пользователь может удалять свои заметки."""
        response = self.author_logged.post(self.GET_URL_NOTES_DELETE)
        self.assertRedirects(response, self.GET_URL_NOTES_SUCCESS)
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST - 1)

    def test_other_user_cant_delete_note(self):
        """Пользователь не может удалять чужие заметки."""
        response = self.reader_logged.post(self.GET_URL_NOTES_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), self.NOTES_BEFORE_REQUEST)
