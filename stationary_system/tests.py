from django.test import TestCase
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
