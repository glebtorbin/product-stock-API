from http import HTTPStatus

from django.urls import include, path
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_get_urls(self):
        """
        Get urls.
        """
        urls = ['/api/stocks/', '/api/products/']
        for u in urls:
            response = self.client.get(u, format='json')
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(len(response.data), 0)

    def test_stock_create(self):
        """
        Stock create.
        """
        url = '/api/stocks/'
        cr_response = self.client.post(
            url, data={'title': 'stock1'}, format='json'
        )
        self.assertEqual(cr_response.status_code, HTTPStatus.CREATED)
        self.assertEqual(len(cr_response.data), 4)

        ch_response = self.client.get('/api/stock_status/1', format='json')
        self.assertEqual(ch_response.status_code, HTTPStatus.OK)
        self.assertEqual(ch_response.data, {'status': True})

        ch_response = self.client.post('/api/stock_status/1', format='json')
        self.assertEqual(ch_response.status_code, HTTPStatus.OK)
        self.assertEqual(
            ch_response.data, {'stock1 availability status': False}
        )
