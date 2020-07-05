from django.urls import path
from . import views

app_name = "rooms"
# fbv
# urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
# cbv
urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]