from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class TaggedItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.select_related("tag").filter(
            content_type=content_type, object_id=obj_id
        )


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    object = TaggedItemManager()
    # What tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # 适合任何通用类型，通过type(content_type)和id(object_id)来指向任何模型
    # GenericForeignKey是一个特殊的外键，它可以指向任何模型
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # 默认id是interger，如果是string会有限制
    content_object = GenericForeignKey()  # content_object是一个获取到的通用的实物，可以指向任何模型
