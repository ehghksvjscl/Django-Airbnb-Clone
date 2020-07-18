import os
import requests

from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.contrib import messages  # 메시지 실험

from . import forms, models

# CSRF는 Cross Site Request Forgery
# 사이트 간 요청 위조


class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "test@google.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)  # 로그인 인증 담기
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class LoginViewEZ(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(
            self.request, username=email, password=password
        )  # 로그인 인증 담기
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(
            self.request, username=email, password=password
        )  # 로그인 인증 담기
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.save()
        # to do: add sucess message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_PW")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            tokenjson = token_request.json()
            error = tokenjson.get("error", None)
            if error is not None:
                raise GithubException("권한 코드를 찾을 수 없습니다.")
            else:
                access_token = tokenjson.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    # print(profile_json)
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(f"{user.login_method}으로 로그인 해주세요")

                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"환영합니다. {user.first_name}")
                    return redirect(reverse("core:home"))
                    # if user is not None:
                    #     return redirect(reverse("users:login"))
                    # else:
                    #     models.User.objects.create(
                    #         first_name=name, email=email, bio=bio, username=email
                    #     )
                    #     login(request, user)
                    #     return redirect(reverse("core:home"))
                else:
                    raise GithubException("고객 정보를 얻을 수 없습니다.")
        else:
            raise GithubException("권한 코드를 얻을 수 없습니다.")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


# 카카오 로그인 연동
def kakao_login(request):
    app_key = os.environ.get("KAKAO_KEY")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_key}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        app_key = os.environ.get("KAKAO_KEY")
        code = request.GET.get("code")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_key}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        # print(token_json.json())
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("권한코드를 찾을 수 없습니다.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        # print(profile_request.json())
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email")
        if email is None:
            raise KakaoException("이메일을 꼭 선택해 주세요.")
        nickname = profile_json.get("properties").get("nickname")
        profile_image = profile_json.get("properties").get(
            "profile_image"
        )  # 이미지 가져와서 avater에 추가
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"{user.login_method}으로 로그인 해주세요")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
                username=email,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                print(profile_image)
                photo_request = requests.get(profile_image)  # byte 값으로 가져오기
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )  # bullshit파일을 django에서 처리하는 방법
        login(request, user)
        messages.success(request, f"환영합니다. {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))
