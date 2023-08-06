import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models
from generic_permissions.models import PermissionModelMixin, VisibilityModelMixin


def make_uuid():
    """Return a new random UUID value.

    This indirection is done for testing purposes, so test code can mock
    uuid.uuid4(). If we wouldn't do this, then the models would have a direct
    reference that doesn't get mocked away.

    We can't replace it with a lambda because Django Migrations can't handle them.
    """
    return uuid.uuid4()


class GWRLink(PermissionModelMixin, VisibilityModelMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=make_uuid, editable=False)
    eproid = models.CharField(max_length=255)
    local_id = models.CharField(max_length=255)
    context = JSONField(default=dict)

    class Meta:
        unique_together = (("eproid", "local_id"),)
