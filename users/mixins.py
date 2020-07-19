from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return (
            not self.request.user.is_authenticated
        )  # 권한이 없을떄만 handel_no_permission gogo

    def handle_no_permission(self):
        messages.error(self.request, "갈수 없는 페이지 입니다.")
        return redirect("core:home")


# 로그인이 안되어 있을시 이동 설정
class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")


class EmailLoginOnlyVeiw(UserPassesTestMixin):  #
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "갈수 없는 페이지 입니다.")
        return redirect("core:home")


# access 토큰이 없을떄 홈으로 보내는 기능을 대신함 (데코레이터랑 비슷)
