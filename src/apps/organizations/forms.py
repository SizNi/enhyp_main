from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.organizations.models import Organization


class CreateOrganizationForm(forms.ModelForm):
    org_name = forms.CharField(
        label=_("Наименование организации"),
        max_length=100,
        label_suffix="",
        required=True,
        validators=[
            RegexValidator(
                regex=r"^(ООО|ИП|АО|ОАО|ЗАО)\s",
                message="Некорректное наименование организации",
                code="invalid_org_name",
            )
        ],
        help_text=_("Обязательное поле"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("ООО 'Ромашка'"),
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )

    inn = forms.CharField(
        label=_("ИНН"),
        min_length=10,
        max_length=12,
        label_suffix="",
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10,12}$",
                message="ИНН должен состоять из 10, 11 или 12 цифр.",
                code="invalid_inn",
            )
        ],
        help_text=_("ИНН в формате 10-12 цифр"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("ИНН"),
                "class": "form-control",
            }
        ),
    )

    address = forms.CharField(
        label=_("Адрес организации"),
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("г. Москва, ул. Лубянка, д. 10"),
                "class": "form-control",
            }
        ),
    )

    email = forms.EmailField(
        label=_("Электронная почта организации"),
        label_suffix="",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("info@organization.ru"),
                "class": "form-control",
            }
        ),
    )

    # валидатор номера телефона
    phone_val = RegexValidator(
        regex=r"^\+?\d{9,15}$", message="Введите правильный номер телефона."
    )
    # поле номера телефона
    phone = forms.CharField(
        label=_("Номер телефона"),
        validators=[phone_val],
        widget=forms.TextInput(
            attrs={
                "placeholder": "+71234567890",
                "class": "form-control",
            }
        ),
    )

    logo = forms.ImageField(
        label=_("Логотип"),
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "multiple": False,
                "class": "form-control",
            }
        ),
    )

    # проверка логотипа
    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            # Проверка размера
            max_size = 5 * 1024 * 1024  # 5 МБ
            if logo.size > max_size:
                raise ValidationError(
                    _("Размер логотипа превышает максимально допустимый размер (5 МБ).")
                )

            # Проверка расширения
            allowed_extensions = [".png", ".jpg", ".jpeg"]
            extension = str(logo.name).lower().split(".")[-1]
            if extension not in allowed_extensions:
                raise ValidationError(
                    _(
                        "Недопустимое расширение файла. Допустимы только файлы с расширениями .png, .jpg, .jpeg."
                    )
                )

        return logo

    class Meta:
        model = Organization
        fields = ["org_name", "inn", "address", "email", "phone", "logo"]
