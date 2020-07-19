from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView, View, UpdateView
from django.utils import timezone
from django.http import Http404
from django_countries import countries
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users import mixins as user_mixins
from django.contrib.messages.views import SuccessMessageMixin

from . import models, forms
from math import ceil  # 올림하는 함수

# 페이지 랜더링 하는 fbv
def all_rooms(request):
    page = int(request.GET.get("page", 1))

    # 변수를 선언하고 all을 담으면 데이터 과부하가 되지 않는다 해당 변수를 사용할때 메모리에 올라간다.
    room_list = models.Room.objects.all()
    # model = models.Room
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
# 이처럼 선언을 하면 html에서 object list나 page_obj 이러한 변수를 사용할 수 있다 ex) room_list.html
# ListView를 상속 받았기 때문에 room_list,html을 찾는다.
class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
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


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = rooms = models.Room.objects.filter(**filter_args).order_by(
                    "-created"
                )

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("pasge", 1)

                rooms = paginator.get_page(page)
                # print("Get으로 데이터 받는 형식, 검색조건 On")
                return render(
                    request, "rooms/searchform.html", {"form": form, "rooms": rooms}
                )
        else:
            form = forms.SearchForm()
            # print("빈폼으로 올때. 그냥 search페이지를 호출")

        return render(request, "rooms/searchform.html", {"form": form})


# def search(request):

# --------------------------------------------------------------------------------------

# search에서 form의 input에서준 city,country,room_type 값 받아오기
# city = request.GET.get("city", "Anywhere")
# city = str.capitalize(city)
# s_country = request.GET.get("country", "KR")
# room_type = int(request.GET.get("room_type", 0))
# price = int(request.GET.get("price", 0))
# guests = int(request.GET.get("guests", 0))
# bedrooms = int(request.GET.get("bedrooms", 0))
# beds = int(request.GET.get("beds", 0))
# baths = int(request.GET.get("baths", 0))
# instant = bool(request.GET.get("instant", False))
# superhost = bool(request.GET.get("superhost", False))
# s_amenities = request.GET.getlist("amenities")
# s_facilities = request.GET.getlist("facilities")
# # print(f"{s_amenities}, {s_facilities}")

# # 앞글자 대문자 만들기
# room_types = models.RoomType.objects.all()

# # ManyToMany 가져오는 방법 rooms/search.html을 참고 하면서 보시오!
# amenities = models.Amenity.objects.all()
# facilities = models.Facility.objects.all()
# # print(request.GET)

# form = {
#     "city": city,
#     "s_room_type": room_type,
#     "price": price,
#     "guests": guests,
#     "s_country": s_country,
#     "bedrooms": bedrooms,
#     "beds": beds,
#     "baths": baths,
#     "s_amenities": s_amenities,
#     "s_facilities": s_facilities,
#     "instant": instant,
#     "superhost": superhost,
# }
# choices = {
#     "countries": countries,
#     "room_types": room_types,
#     "amenities": amenities,
#     "facilities": facilities,
# }

# # Search 검색 조건 만들기
# # https://docs.djangoproject.com/en/3.0/ref/models/querysets/
# filter_args = {}
# if city != "Anywhere":
#     filter_args["city__startswith"] = city

# # 나라 조건
# filter_args["country"] = s_country

# # 방 타입 조건
# if room_type != 0:
#     filter_args["room_type__pk"] = room_type

# # 가격 조건
# if price != 0:
#     filter_args["price__lte"] = price

# # Guest 조건
# if guests != 0:
#     filter_args["guests__gte"] = guests

# # bedrooms 조건
# if bedrooms != 0:
#     filter_args["bedrooms__gte"] = bedrooms

# # beds 조건
# if beds != 0:
#     filter_args["beds__gte"] = beds

# # baths 조건
# if baths != 0:
#     filter_args["baths__gte"] = baths

# # instant 조건
# if instant is True:
#     filter_args["instant_book"] = True

# # superhost 조건
# if superhost is True:
#     filter_args["host__superhost"] = True

# # Amenitiy조건
# if len(s_amenities) > 0:
#     for s_amenitiy in s_amenities:
#         filter_args["amenities__pk"] = int(s_amenitiy)

# # Facilities 조건
# if len(s_facilities) > 0:
#     for s_facility in s_facilities:
#         filter_args["facilities__pk"] = int(s_facility)

# rooms = models.Room.objects.filter(**filter_args)
# print(bool(instant), bool(superhost))
# print(s_country)

# 개고생 하는 방법
# return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    # get_object는 cbv에서 쓰인다 우리는 model에 던지는건 Room 정보이지 Room의 어느 객체인지 모른다.
    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotoView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    # print(f"Should delete {photo_pk} from {room_pk}")
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "사진을 지울 수 없습니다.")
        else:
            print(room_pk, user.pk)
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "사진 삭제 완료")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        redirect(reversed("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "사진 정보 변경 완료"

    # url에서 room_pk를 찾아서 room.pk를 얻는 방법 예시
    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})
