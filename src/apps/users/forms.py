from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class LoginUserForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        max_length=20,
        label_suffix="",
        required=True,
        help_text=_("Введите логин"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Имя пользователя"),
                "autofocus": True,
                "class": "form-control",
            }
        ),
        error_messages={"required": "Это поле обязательно для заполнения."},
    )
    password = forms.CharField(
        label=_("Пароль"),
        label_suffix="",
        max_length=100,
        required=True,
        help_text=_("введите пароль"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Пароль"),
                "class": "form-control",
            }
        ),
        error_messages={"required": "Это поле обязательно для заполнения."},
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "password")

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Неверное имя пользователя или пароль")


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        max_length=20,
        label_suffix="",
        required=True,
        help_text=_("Обязательное поле. " "Не более 20 символов."),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Имя пользователя"),
                "autofocus": True,
                "class": "form-control",
            }
        ),
        error_messages={"unique": _("Пользователь с таким именем" " уже есть")},
    )
    email = forms.EmailField(
        label=_("Электронная почта"),
        label_suffix="",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Электронная почта"),
                "class": "form-control",
            }
        ),
        error_messages={"unique": _("Данный email занят")},
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        label_suffix="",
        max_length=100,
        required=True,
        help_text=_("Ваш пароль должен содержать " "как минимум 3 символа."),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Пароль"),
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        label_suffix="",
        max_length=100,
        required=True,
        help_text=_("Для подтверждения введите," " пожалуйста, пароль ещё раз."),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Подтверждение " "пароля"),
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Имя пользователя"),
        label_suffix="",
        help_text=_("Обязательное поле. " "Не более 20 символов."),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Имя пользователя"),
                "autofocus": True,
                "class": "form-control",
            }
        ),
        error_messages={"unique": _("Пользователь с таким именем" " уже есть")},
    )
    email = forms.EmailField(
        label=_("Электронная почта"),
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Электронная почта"),
                "class": "form-control",
            }
        ),
        error_messages={"unique": _("Данный email занят")},
    )
    password1 = forms.CharField(
        label=_("Новый пароль"),
        label_suffix="",
        help_text=_("Ваш пароль должен содержать " "как минимум 3 символа."),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Пароль"),
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        label_suffix="",
        help_text=_("Для подтверждения введите," " пожалуйста, пароль ещё раз."),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Подтверждение " "пароля"),
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Сделайте поле password1 необязательным
        self.fields["password1"].required = False
        self.fields["password2"].required = False


class RecoveryUserForm(forms.Form):
    email = forms.EmailField(
        label=_("Введите емейл, указанный при регистрации"),
        help_text=_("Емейл должен был быть подтвержден"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Электронная почта"),
                "class": "form-control",
            }
        ),
    )


class SecondRecoveryUserForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Новый пароль"),
        label_suffix="",
        required=True,
        help_text=_("Ваш пароль должен содержать " "как минимум 3 символа."),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Пароль"),
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ("password",)
