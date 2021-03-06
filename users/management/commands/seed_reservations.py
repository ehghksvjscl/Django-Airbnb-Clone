from django.core.management.base import BaseCommand, no_translations
from users.models import User
from rooms.models import Room
from reservations.models import Reservation
from django_seed import Seed
from datetime import datetime, timedelta
import random

# lists seed 생성 python file

Name = "Reservations"


class Command(BaseCommand):
    help = f"{Name} Create Seed!"

    # commad 뒤에 옵션 값 설정 type,default, help message 등등 넣을ㄹ 수 있음.
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"how many user do you want to craete {Name}?",
        )

    @no_translations
    def handle(self, *args, **options):
        number = options.get("number", 1)

        # seed 생성
        seeder = Seed.seeder()
        # 파람 : class , 반복수 , 제외할 대상의 값{딕셔너리}

        users = User.objects.all()
        rooms = Room.objects.all()
        seeder.add_entity(
            Reservation,
            number,
            {
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
            },
        )
        # seed 실행
        seeder.execute()

        self.stdout.write(self.style.SUCCESS((f"{Name} created")))
