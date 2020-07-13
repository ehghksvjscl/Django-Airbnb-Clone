from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data  # 비밀번호와 아이디가 맞았을 경우 clean data 리턴(아이디 비번)
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀렸습니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("유저가 없습니다."))


class SignUpForm(forms.ModelForm):
    # ModelForm은 내장된 save가 있어서 save를 따로 작성하지 않는다.
    # ModelForm은 model과 fields에 값을 넣어서 form을 표현한다.
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # first_name = forms.CharField(max_length=80)
    # last_name = forms.CharField(max_length=80)
    # email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(email=email)
    #         raise forms.ValidationError("이미 가입된 사용자가 있습니다.")
    #     except models.User.DoesNotExist:
    #         return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("비밀번호를 재확인 바랍니다.")
        else:
            return password

    # def save(self):
    # first_name = self.cleaned_data.get("first_name")
    # last_name = self.cleaned_data.get("last_name")
    # email = self.cleaned_data.get("email")
    # password = self.cleaned_data.get("password")

    # user = models.User.objects.create_user(email, email, password)
    # user.first_name = first_name
    # user.last_name = last_name
    # user.save()
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()  # 여기 세이브는 커밋 True로 만든다
