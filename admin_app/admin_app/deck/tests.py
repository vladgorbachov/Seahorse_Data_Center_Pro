import tempfile
from django.test import TestCase, Client
from django.urls import reverse
from .models import Folder, Table, TableCell, FileMetadata
import json
import os

class FolderModelTest(TestCase):
    def setUp(self):
        self.folder = Folder.objects.create(index=1, name='Test Folder', link='http://example.com')

    def test_folder_creation(self):
        self.assertEqual(self.folder.name, 'Test Folder')
        self.assertEqual(self.folder.link, 'http://example.com')
        self.assertTrue(self.folder.visible)

    def test_folder_string_representation(self):
        self.assertEqual(str(self.folder), 'Test Folder')

class FileMetadataModelTest(TestCase):
    def setUp(self):
        self.folder = Folder.objects.create(index=1, name='Test Folder')
        self.metadata = FileMetadata.objects.create(folder=self.folder, file_type='text', size=100, last_modified='2024-01-01T00:00:00Z', icon_path='path/to/icon')

    def test_metadata_creation(self):
        self.assertEqual(self.metadata.folder, self.folder)
        self.assertEqual(self.metadata.file_type, 'text')
        self.assertEqual(self.metadata.size, 100)

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
        self.folder = Folder.objects.create(index=1, name='Local Folder', link='file:///path/to/local/folder', is_local_link=True)
        os.makedirs('/path/to/local/folder', exist_ok=True)
        with open('/path/to/local/folder/test.txt', 'w') as f:
            f.write('Test content')

    def tearDown(self):
        os.remove('/path/to/local/folder/test.txt')
        os.rmdir('/path/to/local/folder')

    def test_folder_content_view(self):
        response = self.client.get(reverse('explorer_view', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Local Folder')

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
        self.folder = Folder.objects.create(index=1, name='Invalid File Path', link='file:///invalid/path', is_local_link=True)

    def test_invalid_file_path(self):
        response = self.client.get(reverse('explorer_view', args=[self.folder.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No content found')

class FileActionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='File Action Folder', link='file:///path/to/folder', is_local_link=True)
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.test_dir.name, 'test.txt')
        with open(self.file_path, 'w') as f:
            f.write('Test content')

    def tearDown(self):
        self.test_dir.cleanup()

    def test_open_file_action(self):
        response = self.client.get(reverse('file_action'), {'action': 'open', 'path': self.file_path})
        self.assertEqual(response.status_code, 200)

    def test_download_file_action(self):
        response = self.client.get(reverse('file_action'), {'action': 'download', 'path': self.file_path})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="test.txt"')

class RenameFileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Rename File Folder', link='file:///path/to/folder', is_local_link=True)
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.test_dir.name, 'test.txt')
        with open(self.file_path, 'w') as f:
            f.write('Test content')

    def tearDown(self):
        self.test_dir.cleanup()

    def test_rename_file(self):
        new_name = 'renamed.txt'
        response = self.client.post(reverse('rename_file'), json.dumps({
            'file_id': self.file_path,
            'new_name': new_name
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(self.file_path), new_name)))

class DeleteFileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.folder = Folder.objects.create(index=1, name='Delete File Folder', link='file:///path/to/folder', is_local_link=True)
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.test_dir.name, 'test.txt')
        with open(self.file_path, 'w') as f:
            f.write('Test content')

    def tearDown(self):
        self.test_dir.cleanup()

    def test_delete_file(self):
        response = self.client.post(reverse('delete_file'), json.dumps({
            'file_id': self.file_path
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(os.path.exists(self.file_path))
