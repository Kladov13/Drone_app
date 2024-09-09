import unittest
from app import app, start_video_stream
from flask import jsonify

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Выполняется перед всеми тестами, запускает приложение Flask и поток видео.
        """
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True

        # Запускаем поток видео в отдельном потоке
        import threading
        video_thread = threading.Thread(target=start_video_stream)
        video_thread.start()

    def test_index(self):
        """
        Тестирование главной страницы.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Drone Control Dashboard', response.data)

    def test_get_status(self):
        """
        Тестирование получения статуса дрона.
        """
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_update_position(self):
        """
        Тестирование обновления координат дрона.
        """
        response = self.client.post('/position', json={'coordinates': (10, 20)})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_update_height(self):
        """
        Тестирование обновления высоты дрона.
        """
        response = self.client.post('/height', json={'height': 100})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_update_velocity(self):
        """
        Тестирование обновления скорости дрона.
        """
        response = self.client.post('/velocity', json={'velocity': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_check_battery(self):
        """
        Тестирование проверки уровня заряда батареи.
        """
        response = self.client.get('/battery')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_return_to_base(self):
        """
        Тестирование возвращения дрона на базу.
        """
        response = self.client.post('/return_to_base')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
    unittest.main()
