from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class LikedItem(models.Model):
    # what user like what object
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 默认id是interger，如果是string会有限制
    content_object = GenericForeignKey()  # content_object是一个获取到的通用的实物，可以指向任何模型