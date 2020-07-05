from django.urls import path
from rooms import views as room_veiw

# fbv
# urlpatterns = [path("", room_veiw.all_rooms, name="home")]
# cbv
app_name = "home"
urlpatterns = [path("", room_veiw.HomeView.as_view(), name="home")]
