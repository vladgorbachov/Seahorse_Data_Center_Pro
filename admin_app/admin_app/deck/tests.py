# admin_app/admin_app/deck/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from admin_app.deck.models import Folder, Table
import json


class FolderModelTest(TestCase):
    def setUp(self):
        self.folder = Folder.objects.create(index=1, name='Test Folder', link='http://example.com')

    def test_folder_creation(self):
        self.assertEqual(self.folder.name, 'Test Folder')
        self.assertEqual(self.folder.link, 'http://example.com')
        self.assertTrue(self.folder.visible)

    def test_folder_string_representation(self):
        self.assertEqual(str(self.folder), 'Test Folder')


class DeckDepartmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Folder.objects.create(index=1, name='Visible Folder', visible=True)
        Folder.objects.create(index=2, name='Hidden Folder', visible=False)

    def test_deck_department_view(self):
        response = self.client.get(reverse('deck_department'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visible Folder')
        self.assertNotContains(response, 'Hidden Folder')


class AddFolderViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_add_folder(self):
        response = self.client.post(reverse('add_folder'), json.dumps({
            'index': 1,
            'name': 'New Folder',
            'link': 'http://example.com'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(Folder.objects.first().name, 'New Folder')


class UpdateFolderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Old Name', link='http://example.com')

    def test_update_folder(self):
        response = self.client.post(reverse('update_folder', args=[self.folder.id]), json.dumps({
            'name': 'Updated Name'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.folder.refresh_from_db()
        self.assertEqual(self.folder.name, 'Updated Name')


class DeleteFolderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Folder to be deleted')

    def test_delete_folder(self):
        response = self.client.post(reverse('delete_folder', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Folder.objects.count(), 0)


class FolderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='View Folder', link='http://example.com')

    def test_folder_view(self):
        response = self.client.get(reverse('folder_view', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Folder')


class GetMaxFolderIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Folder.objects.create(index=1, name='First Folder')
        Folder.objects.create(index=2, name='Second Folder')

    def test_get_max_folder_index(self):
        response = self.client.get(reverse('get_max_folder_index'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['max_index'], 2)


class FolderContentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Local Folder', link='file:///path/to/local/folder',
                                            is_local_link=True)

    def test_folder_content_view(self):
        response = self.client.get(reverse('folder_content_view', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Local Folder')
        self.assertContains(response, 'Folder Path: file:///path/to/local/folder')


class TableViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Table Folder')

    def test_save_and_load_table_data(self):
        # Сохранение данных таблицы
        response = self.client.post(reverse('save_table'), json.dumps({
            'folder_id': self.folder.id,
            'rows': 2,
            'columns': 3
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        table_id = json.loads(response.content)['table_id']

        # Загрузка данных таблицы
        response = self.client.get(reverse('table_view', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Table Folder')
        self.assertContains(response, f'data-cell-id="{table_id}"')


class DeleteTableInFolderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Folder with Table')
        self.table = Table.objects.create(folder=self.folder, rows=2, columns=2)

    def test_delete_table_in_folder(self):
        response = self.client.post(reverse('delete_table_in_folder', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Table.objects.count(), 0)


class ErrorHandlingTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_invalid_folder_id(self):
        response = self.client.get(reverse('folder_view', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_invalid_file_path(self):
        folder = Folder.objects.create(index=1, name='Invalid File Path', link='file:///invalid/path',
                                       is_local_link=True)
        response = self.client.get(reverse('folder_content_view', args=[folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No content found')
