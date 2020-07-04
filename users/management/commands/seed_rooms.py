from django.core.management.base import BaseCommand, no_translations
from django_seed import Seed
from django.contrib.admin.utils import flatten
from users import models as user_models
from rooms import models as room_models
import random

# user seed 생성 python file
class Command(BaseCommand):
    help = "Rooms Create Seed!"

    # commad 뒤에 옵션 값 설정 type,default, help message 등등 넣을ㄹ 수 있음.
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="how many user do you want to craete rooms?",
        )

    @no_translations
    def handle(self, *args, **options):
        number = options.get("number", 1)

        # seed 생성
        seeder = Seed.seeder()

        # 데이터가 많을 경우에는 all은 쓰지 말자!! 기본키 설정을 위해 선언
        all_user = user_models.User.objects.all()
        room_type = room_models.RoomType.objects.all()

        # 파람 : class , 반복수 , 제외할 대상의 값{딕셔너리}
        # 각각의 값들을 함수를 만들어 컨트롤 하는 것도 가능합니다.
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(room_type),
                "price": lambda x: random.randint(0, 300),
                "beds": lambda x: random.randint(0, 6),
                "bedrooms": lambda x: random.randint(0, 6),
                "baths": lambda x: random.randint(0, 6),
                "guests": lambda x: random.randint(0, 20),
            },
        )
        # seed 실행
        # 마지막

        """ 1 이상한 모양을 정리하고
            2 생성된 등록한 룸을 반복으로 돌리고
            3 기본키로 room을 찾고
            4 루프를 돌면서 3개 ~ 17까지 포토를 넣어준다.
        """
        create_photo = seeder.execute()
        # print(list(create_photo.values())[0])
        create_clean = flatten(list(create_photo.values())[0])
        # print(create_clean)
        for pk in create_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 17)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    file=f"/room_photos/{random.randint(1,31)}.webp",
                    room=room,
                )
        self.stdout.write(self.style.SUCCESS(("Rooms created")))
