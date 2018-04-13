import unittest

from app import app


class TestUpload(unittest.TestCase):

    app.config['TESTING'] = True

    def test_upload_client_negatif(self):
        client = app.test_client()

        data = dict(
            fileUpload=(open('file/test.png', 'rb'))
        )

        response = client.post('/scan/upload', content_type='multipart/form-data', data=data)

        self.assertEqual(response.status_code, 409 )

    def test_upload_client_positif(self):

        client = app.test_client()

        data = dict(
            fileUpload=(open('file/test.Pdf', 'rb'))
        )

        response = client.post('/scan/upload', content_type='multipart/form-data', data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
