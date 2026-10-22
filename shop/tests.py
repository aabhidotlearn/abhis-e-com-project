from django.test import TestCase
from django.urls import reverse

from shop.models.category import Category
from shop.models.product import Product


class ProductApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.laptops = Category.objects.create(name="Laptops")
        cls.phones = Category.objects.create(name="Phones")
        cls.laptop = Product.objects.create(
            name="Travel laptop",
            category=cls.laptops,
            image="",
            desc="Lightweight computer for work and travel.",
            price=1200,
        )
        cls.phone = Product.objects.create(
            name="Everyday phone",
            category=cls.phones,
            image="img/phone.jpeg",
            desc="A phone with a long-lasting battery.",
            price=500,
        )

    def test_product_list_returns_json_product_data(self):
        response = self.client.get(reverse("api_products"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response.json()["count"], 2)
        product = response.json()["results"][0]
        self.assertEqual(product["name"], "Everyday phone")
        self.assertEqual(product["category"]["name"], "Phones")
        self.assertEqual(product["image_url"], "http://testserver/media/img/phone.jpeg")
        self.assertEqual(product["detail_url"], reverse("product_detail", args=[self.phone.pk]))

    def test_product_search_and_category_filter_can_be_combined(self):
        response = self.client.get(
            reverse("api_products"),
            {"q": "travel", "category": self.laptops.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item["id"] for item in response.json()["results"]], [self.laptop.pk])

    def test_product_list_can_sort_by_price(self):
        response = self.client.get(reverse("api_products"), {"ordering": "price_desc"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [item["price"] for item in response.json()["results"]],
            [1200, 500],
        )

    def test_invalid_api_parameters_return_json_errors(self):
        category_response = self.client.get(reverse("api_products"), {"category": "unknown"})
        ordering_response = self.client.get(reverse("api_products"), {"ordering": "-price"})

        self.assertEqual(category_response.status_code, 400)
        self.assertIn("error", category_response.json())
        self.assertEqual(ordering_response.status_code, 400)
        self.assertIn("error", ordering_response.json())

    def test_product_detail_returns_json_404_for_missing_product(self):
        response = self.client.get(reverse("api_product_detail", args=[99999]))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Product not found"})

    def test_category_endpoint_returns_categories(self):
        response = self.client.get(reverse("api_categories"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["results"],
            [
                {"id": self.laptops.pk, "name": "Laptops"},
                {"id": self.phones.pk, "name": "Phones"},
            ],
        )


class StorefrontTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Tablets")
        cls.product = Product.objects.create(
            name="Study tablet",
            category=cls.category,
            image="",
            desc="Tablet for school.",
            price=300,
        )

    def test_homepage_contains_search_sort_and_server_rendered_products(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="product-search"')
        self.assertContains(response, 'id="product-sort"')
        self.assertContains(response, self.product.name)
        self.assertContains(response, reverse("api_products"))

    def test_invalid_category_on_homepage_does_not_crash(self):
        response = self.client.get(reverse("home"), {"category": "not-a-number"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_homepage_search_sort_and_category_are_shareable(self):
        response = self.client.get(
            reverse("home"),
            {"q": "school", "category": self.category.pk, "ordering": "price_desc"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="school"')
        self.assertContains(response, 'value="price_desc" selected')
        self.assertContains(response, self.product.name)
