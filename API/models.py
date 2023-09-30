from django.db import models
import uuid

class GeneratedUUID(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
