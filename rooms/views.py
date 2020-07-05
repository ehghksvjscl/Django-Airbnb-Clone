from django.shortcuts import render
from . import models
from math import ceil  # 올림하는 함수
from django.core.paginator import Paginator


def all_rooms(request):
    page = request.GET.get("page", 1)
    # 변수를 선언하고 all을 담으면 데이터 과부하가 되지 않는다 해당 변수를 사용할때 메모리에 올라간다.
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    print(rooms.object_list)
    return render(request, "rooms/home.html", {"rooms": rooms})

    # 페이지 랜더링 가장 단순한 방법
    # page = request.GET.get("page", 1)
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    # page_count = ceil(models.Room.objects.count() / page_size)
    # all_rooms = models.Room.objects.all()[offset:limit]
    # return render(
    #     request,
    #     "rooms/home.html",
    #     context={
    #         "rooms": all_rooms,
    #         "page": page,
    #         "page_count": page_count,
    #         "page_range": range(1, page_count + 1),
    #     },
    # )
