from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ServiceBooking, Vehicle


class VehicleViewTests(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.vehicle = Vehicle.objects.create(
			name='City ZX',
			brand='Honda',
			color='White',
			price='850000.00',
			year=2022,
			fuel_type='Petrol',
		)

	def test_vehicle_list_filters_by_search(self):
		response = self.client.get(reverse('vehicle_list'), {'search': 'Honda'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'City ZX')

	def test_invalid_price_filter_does_not_break_listing(self):
		response = self.client.get(reverse('vehicle_list'), {'price': 'not-a-price'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'City ZX')

	def test_services_nav_opens_separate_booking_page(self):
		response = self.client.get(reverse('vehicle_list'))

		self.assertContains(response, f'href="{reverse("service_booking")}"')
		self.assertNotContains(response, 'Book a Car Service')

		service_response = self.client.get(reverse('service_booking'))
		self.assertEqual(service_response.status_code, 200)
		self.assertContains(service_response, 'Book a Car Service')
		self.assertContains(service_response, 'No login required')

	def test_anyone_can_book_a_car_service_without_login(self):
		response = self.client.post(reverse('service_booking'), {
			'customer_name': 'Asha Patel',
			'phone': '9876543210',
			'car_model': 'Honda City',
			'registration_number': 'GJ01AB1234',
			'service_type': 'general',
			'preferred_date': '2026-10-15',
			'preferred_time': '10:30',
			'notes': 'Please check the brakes.',
		})

		self.assertRedirects(response, reverse('service_booking'))
		self.assertEqual(ServiceBooking.objects.count(), 1)
		self.assertEqual(ServiceBooking.objects.get().status, 'pending')

	def test_service_booking_rejects_past_date(self):
		response = self.client.post(reverse('service_booking'), {
			'customer_name': 'Asha Patel',
			'phone': '9876543210',
			'car_model': 'Honda City',
			'service_type': 'general',
			'preferred_date': '2020-01-01',
			'preferred_time': '10:30',
		})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(ServiceBooking.objects.count(), 0)
		self.assertContains(response, 'Choose today or a future date.')

	def test_missing_vehicle_returns_not_found(self):
		response = self.client.get(reverse('vehicle_detail', args=[9999]))

		self.assertEqual(response.status_code, 404)

	def test_selling_a_car_requires_login(self):
		response = self.client.get(reverse('sell_vehicle'))

		self.assertRedirects(
			response,
			f"{reverse('login')}?next={reverse('sell_vehicle')}",
		)

	def test_authenticated_user_can_list_a_car(self):
		user = User.objects.create_user(username='seller', password='StrongPass123!')
		self.client.force_login(user)

		response = self.client.post(reverse('sell_vehicle'), {
			'name': 'Civic RS',
			'brand': 'Honda',
			'color': 'Blue',
			'registration_number': 'ABC123',
			'kilometers': '12000',
			'price': '1800000.00',
			'year': '2023',
			'fuel_type': 'Petrol',
			'seller_name': 'Seller',
			'seller_phone': '9876543210',
		})

		self.assertRedirects(response, reverse('sell_vehicle'))
		self.assertTrue(Vehicle.objects.filter(name='Civic RS').exists())


class AuthenticationViewTests(TestCase):
	def test_signup_rejects_weak_password(self):
		response = self.client.post(reverse('signup'), {
			'username': 'new-user',
			'password': '123',
		})

		self.assertEqual(response.status_code, 200)
		self.assertFalse(User.objects.filter(username='new-user').exists())
		self.assertContains(response, 'too short')

	def test_logout_requires_post(self):
		user = User.objects.create_user(username='test-user', password='StrongPass123!')
		self.client.force_login(user)

		response = self.client.get(reverse('logout'))

		self.assertEqual(response.status_code, 405)
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_logout_works_with_post(self):
		user = User.objects.create_user(username='test-user', password='StrongPass123!')
		self.client.force_login(user)

		response = self.client.post(reverse('logout'))

		self.assertRedirects(response, reverse('vehicle_list'))
		self.assertNotIn('_auth_user_id', self.client.session)

	def test_login_respects_next_redirect(self):
		user = User.objects.create_user(username='test-seller', password='StrongPass123!')
		response = self.client.post(
			f"{reverse('login')}?next={reverse('sell_vehicle')}",
			{'username': 'test-seller', 'password': 'StrongPass123!'},
		)
		self.assertRedirects(response, reverse('sell_vehicle'))

	def test_authenticated_user_redirected_away_from_login_and_signup(self):
		user = User.objects.create_user(username='auth-user', password='StrongPass123!')
		self.client.force_login(user)

		login_resp = self.client.get(reverse('login'))
		self.assertRedirects(login_resp, reverse('vehicle_list'))

		signup_resp = self.client.get(reverse('signup'))
		self.assertRedirects(signup_resp, reverse('vehicle_list'))


class ValidationTests(TestCase):
	def test_sell_vehicle_rejects_negative_price(self):
		user = User.objects.create_user(username='seller2', password='StrongPass123!')
		self.client.force_login(user)

		response = self.client.post(reverse('sell_vehicle'), {
			'name': 'Civic RS',
			'brand': 'Honda',
			'color': 'Blue',
			'kilometers': '12000',
			'price': '-50000.00',
			'year': '2023',
			'fuel_type': 'Petrol',
			'seller_name': 'Seller',
			'seller_phone': '9876543210',
		})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Price must be greater than zero.')

	def test_sell_vehicle_rejects_unrealistic_year(self):
		user = User.objects.create_user(username='seller3', password='StrongPass123!')
		self.client.force_login(user)

		response = self.client.post(reverse('sell_vehicle'), {
			'name': 'Civic RS',
			'brand': 'Honda',
			'color': 'Blue',
			'kilometers': '12000',
			'price': '500000.00',
			'year': '1800',
			'fuel_type': 'Petrol',
			'seller_name': 'Seller',
			'seller_phone': '9876543210',
		})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'valid model year')

	def test_sell_vehicle_rejects_invalid_phone(self):
		user = User.objects.create_user(username='seller4', password='StrongPass123!')
		self.client.force_login(user)

		response = self.client.post(reverse('sell_vehicle'), {
			'name': 'Civic RS',
			'brand': 'Honda',
			'color': 'Blue',
			'kilometers': '12000',
			'price': '500000.00',
			'year': '2023',
			'fuel_type': 'Petrol',
			'seller_name': 'Seller',
			'seller_phone': 'invalid_phone',
		})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'valid 10-15 digit phone number')

	def test_service_booking_rejects_invalid_phone(self):
		response = self.client.post(reverse('service_booking'), {
			'customer_name': 'Asha Patel',
			'phone': 'not_a_phone',
			'car_model': 'Honda City',
			'service_type': 'general',
			'preferred_date': '2026-10-15',
			'preferred_time': '10:30',
		})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'valid 10-15 digit phone number')

