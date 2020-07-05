from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.urls import reverse
from django.http import Http404
from django_countries import countries
from . import models
from math import ceil  # 올림하는 함수

# 페이지 랜더링 하는 fbv
def all_rooms(request):
    page = int(request.GET.get("page", 1))
    # 변수를 선언하고 all을 담으면 데이터 과부하가 되지 않는다 해당 변수를 사용할때 메모리에 올라간다.
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    # rooms = paginator.get_page(page) # 에러를 컨트롤 하고 싶지 않고 장고가 에러를 잡아주길 원하면 사용
    try:
        rooms = paginator.page(page)  # 페이지가 잘못 할당 되어 있을때 에러를 컨트롤 하고 싶다면 사용
        return render(request, "rooms/home.html", {"pages": rooms})
    except EmptyPage:
        return redirect("/")

    # rooms = paginator.page(1)

    # print(rooms.object_list)

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


# cbv
# https://ccbv.co.uk/ 사이트에서 cbv 속성 값을 볼수 있다. 여러개의 클래스로 있기 떄문에..
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # super()을 지우면 안된다.
        context["now"] = timezone.now()
        return context


# fbv
def room_detail(request, pk):
    # print("room_detail" end=""),print(pk)
    try:
        room = models.Room.objects.get(pk=pk)
    except models.Room.DoesNotExist:
        # 절대경로로 url 내보내기
        # return redirect("/")

        # 프로페션널 하게 리벌스 사용해서 namespace 찾아가기 자꾸 사용해서 손에 익히자
        # return redirect(reverse("core:home"))
        raise Http404()  # 404.html을 찾아가도록 만든다 꼭 템플릿 폴더 안에 있어여함

    return render(request, "rooms/detail.html", {"room": room})


# cbv
class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    # search에서 form의 input에서준 city,country,room_type 값 받아오기
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guets = int(request.GET.get("guets", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    super_host = request.GET.get("super_host", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    # print(f"{s_amenities}, {s_facilities}")

    # 앞글자 대문자 만들기
    room_types = models.RoomType.objects.all()

    # ManyToMany 가져오는 방법 rooms/search.html을 참고 하면서 보시오!
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()
    # print(request.GET)

    form = {
        "city": city,
        "s_room_type": room_type,
        "price": price,
        "guets": guets,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "super_host": super_host,
    }
    choices = {
        "countries": countries,
        "room_types": room_types,
        "country": country,
        "amenities": amenities,
        "facilities": facilities,
    }

    return render(request, "rooms/search.html", {**form, **choices})
