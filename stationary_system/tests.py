from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from stationary_system.models.activity import Activity


class DeletePendingActivityTests(TestCase):
    def test_customer_can_delete_their_pending_activity(self):
        user = get_user_model().objects.create_user(
            username="delete-test",
            password="test-password",
        )
        activity = Activity.objects.create(
            activity_id="delete-test-activity",
            activity_type="printing",
            costs=0,
            user=user,
            status="pending",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("delete_pending_activity", args=[activity.activity_id])
        )

        self.assertRedirects(
            response,
            reverse("customer_activity_history"),
            fetch_redirect_response=False,
        )
        self.assertFalse(Activity.objects.filter(pk=activity.pk).exists())


class PublicSeoEndpointTests(TestCase):
    def test_favicon_url_serves_stationary_png(self):
        response = self.client.get("/favicon.ico")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/png")
        self.assertTrue(response["Cache-Control"].startswith("public"))
        self.assertEqual(b"".join(response.streaming_content)[:8], b"\x89PNG\r\n\x1a\n")

    @override_settings(ALLOWED_HOSTS=["wis-stationary.onrender.com"])
    def test_sitemap_lists_only_the_public_homepage(self):
        response = self.client.get(
            "/sitemap.xml",
            secure=True,
            HTTP_HOST="wis-stationary.onrender.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "<loc>https://wis-stationary.onrender.com/</loc>",
        )
        self.assertNotContains(response, "/customer/dashboard/")

    def test_robots_txt_points_to_sitemap_and_excludes_private_routes(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "Sitemap: https://wis-stationary.onrender.com/sitemap.xml")
        self.assertContains(response, "Disallow: /customer/")
        self.assertContains(response, "Disallow: /stationary/")

    def test_public_homepage_has_search_metadata(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="description"')
        self.assertContains(
            response,
            '<link rel="canonical" href="https://wis-stationary.onrender.com/">',
            html=True,
        )
