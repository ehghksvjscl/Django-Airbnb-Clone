from django.core.management.base import BaseCommand, no_translations
from rooms.models import Amenity

# amaneties seed 생성 python file
class Command(BaseCommand):
    help = "Amaneties Create Seed!"

    # def add_arguments(self, parser):
    # parser.add_argument("--number", help="your command test how many time?")

    @no_translations
    def handle(self, *args, **options):
        amaneties = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]

        # print(dir(Amenity))
        # print(dir(Amenity.objects))
        # print(dir(Amenity.objects.create))
        for a in amaneties:
            Amenity.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS(("Amenities created")))
        # time = options.get("number")
        # for t in range(0, int(time)):
        #     self.stdout.write(self.style.SUCCESS("your command"))
        # print(options.get("number")) # 뒤에 값 찾는법 get 함수 이용
        # print("your command 실행")
