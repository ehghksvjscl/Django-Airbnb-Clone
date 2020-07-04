from django.core.management.base import BaseCommand, no_translations
from reviews.models import Review
from users.models import User
from rooms.models import Room
from django_seed import Seed
import random
from django.views.View import as_view

# Review seed 생성 python file
class Command(BaseCommand):
    help = "Review Create Seed!"

    # commad 뒤에 옵션 값 설정 type,default, help message 등등 넣을ㄹ 수 있음.
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="how many user do you want to craete Reviews?",
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
            Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )
        # seed 실행
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(("Reviews created")))
