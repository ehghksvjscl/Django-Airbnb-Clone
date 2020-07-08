from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamped Model Definition """

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        abstract = True
        # 애브스트랙트
