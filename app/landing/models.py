from django.db import models
from .utils.constants import MAX_IMAGE_SIZE_BYTES
from .utils.models import SizeRestrictedImageField

class PictureDecoration(models.Model):
    avatar = SizeRestrictedImageField(max_upload_size=MAX_IMAGE_SIZE_BYTES, null=True, blank=True)
    is_active = models.BooleanField(default=True)



class PictureAction(models.Model):
    avatar = SizeRestrictedImageField(max_upload_size=MAX_IMAGE_SIZE_BYTES, null=True, blank=True)
    is_active = models.BooleanField(default=True)