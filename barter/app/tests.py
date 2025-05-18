from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.reverse import reverse

from .models import Product, ExchangeOffer


class ProductTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password="testpass1")
        self.post = Product.objects.create(title="Тестовое объявление",
                                           description="Описание",
                                           category="Электроника",
                                           condition="new",
                                           user=self.user
                                            )

    def test_create_post(self):
        post_count_before = Product.objects.count()
        Product.objects.create(title="Новое объявление", description="Тест", category="Транспорт", condition="used", user=self.user)
        post_count_after = Product.objects.count()
        self.assertEqual(post_count_after, post_count_before + 1)

    def test_edit_post(self):
        self.post.title = "Обновленное объявление"
        self.post.save()
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Обновленное объявление")

    def test_delete_post(self):
        post_count_before = Product.objects.count()
        self.post.delete()
        post_count_after = Product.objects.count()
        self.assertEqual(post_count_after, post_count_before - 1)

    def test_search_post(self):
        response = self.client.get(reverse('search_post') + "?q=Тестовое")
        self.assertContains(response, self.post.title)

class ExchangeTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user3", password="Navigator98765")
        self.user2 = User.objects.create_user(username="user4", password="Navigator987654")
        self.post1 = Product.objects.create(title="Товар 1", category="Электроника", condition="new", user=self.user1)
        self.post2 = Product.objects.create(title="Товар 2", category="Транспорт", condition="used", user=self.user2)
        self.offer = ExchangeOffer.objects.create(post_sender=self.post1,
                                                  post_receiver=self.post2,
                                                  sender=self.user1,
                                                  status="pending")
        self.completed_offer = ExchangeOffer.objects.create(post_sender=self.post1, post_receiver=self.post2, sender=self.user1,
                                                            status="accepted")

    def test_create_exchange(self):
        exchange_count_before = ExchangeOffer.objects.count()
        ExchangeOffer.objects.create(post_sender=self.post1, post_receiver=self.post2, sender=self.user1)
        exchange_count_after = ExchangeOffer.objects.count()
        self.assertEqual(exchange_count_after, exchange_count_before + 1)

    def test_update_exchange_status(self):
        self.offer.status = "accepted"
        self.offer.save()
        self.offer.refresh_from_db()
        self.assertEqual(self.offer.status, "accepted")

    def test_cancel_exchange_by_sender(self):
        exchange_count_before = ExchangeOffer.objects.count()
        self.offer.delete()
        exchange_count_after = ExchangeOffer.objects.count()
        self.assertEqual(exchange_count_after, exchange_count_before - 1)

    def test_hide_posts_after_exchange(self):
        self.offer.status = "accepted"
        self.offer.save()
        self.offer.post_sender.is_active = False
        self.offer.post_sender.save()
        self.offer.post_receiver.is_active = False
        self.offer.post_receiver.save()

        self.assertFalse(self.offer.post_sender.is_active)
        self.assertFalse(self.offer.post_receiver.is_active)

    def test_filter_active_exchanges(self):
        active_exchanges = ExchangeOffer.objects.filter(status="pending")
        self.assertEqual(active_exchanges.count(), 1)
        self.assertEqual(active_exchanges.first().status, "pending")

    def test_filter_completed_exchanges(self):
        completed_exchanges = ExchangeOffer.objects.filter(status="accepted")
        self.assertEqual(completed_exchanges.count(), 1)
        self.assertEqual(completed_exchanges.first().status, "accepted")

    def test_filter_declined_exchanges(self):
        self.completed_offer.status = "declined"
        self.completed_offer.save()
        declined_exchanges = ExchangeOffer.objects.filter(status="declined")
        self.assertEqual(declined_exchanges.count(), 1)
        self.assertEqual(declined_exchanges.first().status, "declined")
