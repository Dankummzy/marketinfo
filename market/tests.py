import unittest
from market.models import CustomUser, MarketData, Alert, Category
from django.test import TestCase


class TestCustomUserModel(unittest.TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(email='admin@example.com', password='admin123')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class MarketDataIntegrationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='password123')
        self.category = Category.objects.create(name='Electronics')

    def test_market_data_creation(self):
        market_data = MarketData.objects.create(
            product_name='Laptop',
            price=1200.00,
            quantity=10,
            vendor_details='Vendor ABC',
            category=self.category,
            created_by=self.user
        )
        self.assertEqual(market_data.product_name, 'Laptop')
        self.assertEqual(market_data.price, 1200.00)
        self.assertEqual(market_data.created_by, self.user)

    def test_report_generation(self):
        response = self.client.get('/generate_report/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Laptop', response.content.decode())

if __name__ == '__main__':
    unittest.main()
