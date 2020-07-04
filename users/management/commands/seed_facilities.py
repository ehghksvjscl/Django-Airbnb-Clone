from django.core.management.base import BaseCommand, no_translations
from rooms.models import Facility

# amaneties seed 생성 python file
class Command(BaseCommand):
    help = "Fecilities Create Seed!"

    # def add_arguments(self, parser):
    # parser.add_argument("--number", help="your command test how many time?")

    @no_translations
    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        # print(dir(Amenity))
        # print(dir(Amenity.objects))
        # print(dir(Amenity.objects.create))
        for a in facilities:
            Facility.objects.create(name=a)

        self.stdout.write(self.style.SUCCESS(("Facilities created")))
        # time = options.get("number")
        # for t in range(0, int(time)):
        #     self.stdout.write(self.style.SUCCESS("your command"))
        # print(options.get("number")) # 뒤에 값 찾는법 get 함수 이용
        # print("your command 실행")
