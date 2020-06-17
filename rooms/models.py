from django.db import models
from django_countries.fields import CountryField
from users import models as users_models
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    # DB정의
    name = models.CharField(max_length=80)

    # 추상화
    class Meta:
        abstract = True

    # 문자열
    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ Room Type Object Definition """

    class Meta:
        verbose_name_plural = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Object Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Object Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Object Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Objdect Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()

    # Photo가 위에 있는데도 아래에 있는 Room class를 사용하고 싶다면 문자열로 만들면 된다.
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    # DB정의
    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    adddress = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(users_models.User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    house_rules = models.ManyToManyField(HouseRule, blank=True)

    # Admin에 보여줄 텍스트 정의
    def __str__(self):
        return self.name
