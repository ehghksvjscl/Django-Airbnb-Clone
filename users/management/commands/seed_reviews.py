from django.core.management.base import BaseCommand, no_translations
from reviews.models import Review
from django_seed import Seed

# Review seed 생성 python file
class Command(BaseCommand):
    help = "Review Create Seed!"

    # commad 뒤에 옵션 값 설정 type,default, help message 등등 넣을ㄹ 수 있음.
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="how many user do you want to craete Reviews?",
        )

    @no_translations
    def handle(self, *args, **options):
        number = options.get("number", 1)

        # seed 생성
        seeder = Seed.seeder()
        # 파람 : class , 반복수 , 제외할 대상의 값{딕셔너리}
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        # seed 실행
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(("Review created")))
