from django.core.management.base import BaseCommand, no_translations
from users.models import User
from rooms.models import Room
from lists.models import List
from django_seed import Seed
from django.contrib.admin.utils import flatten
import random

# lists seed 생성 python file

Name = "List"


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
            List, number, {"user": lambda x: random.choice(users),},
        )
        # seed 실행
        created = seeder.execute()
        created_clean = flatten(list(created.values()))

        # *to_add에 대해서 알아야함.
        for pk in created_clean:
            list_model = List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            # for a in to_add:
            #     print((a))
            # print(*to_add)
            list_model.rooms.add(*to_add)  # 전체 요소를
        self.stdout.write(self.style.SUCCESS((f"{Name} created")))
