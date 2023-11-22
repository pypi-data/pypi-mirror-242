"""Model serializers for the nautobot_device_onboarding REST API."""
# pylint: disable=duplicate-code
from rest_framework import serializers

from nautobot.core.api.serializers import NotesSerializerMixin, ValidatedModelSerializer
from nautobot.dcim.models import Location

from nautobot_device_onboarding.models import OnboardingTask
from nautobot_device_onboarding.utils.credentials import Credentials


class OnboardingTaskSerializer(NotesSerializerMixin, ValidatedModelSerializer):
    """Serializer for the OnboardingTask model."""

    username = serializers.CharField(
        required=False,
        write_only=True,
        help_text="Device username",
    )

    password = serializers.CharField(
        required=False,
        write_only=True,
        help_text="Device password",
    )

    secret = serializers.CharField(
        required=False,
        write_only=True,
        help_text="Device secret password",
    )

    location = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        required=True,
        slug_field="name",
    )

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = OnboardingTask

        fields = [
            "id",
            "location",
            "ip_address",
            "username",
            "password",
            "secret",
            "port",
            "timeout",
            "role",
            "device_type",
            "platform",
            "created_device",
            "status",
            "failed_reason",
            "message",
            "object_type",
        ]

        extra_kwargs = {"location": {"required": True}}

        read_only_fields = ["id", "created_device", "status", "failed_reason", "message", "object_type"]

    def validate(self, data):
        """Custom Validate class to remove credential fields."""
        attrs = data.copy()
        username = attrs.pop("username", "")
        password = attrs.pop("password", "")
        secret = attrs.pop("secret", "")

        self.credentials = Credentials(  # pylint: disable=attribute-defined-outside-init
            username=username,
            password=password,
            secret=secret,
        )

        return super().validate(attrs)
