from django import forms
import os
from django.conf import settings
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
                message="Некорректное наименование организации. ООО 'Рога и Копыта' или ИП Иванов И.И.",
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
                message="ИНН должен состоять из 10-12 цифр.",
                code="invalid_inn",
            )
        ],
        help_text=_("ИНН в формате 10-12 цифр"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("7702455202"),
                "class": "form-control",
            }
        ),
    )

    address = forms.CharField(
        label=_("Адрес организации"),
        max_length=100,
        required=True,
        help_text=_("Адрес нужен для отображения в контактах в паспорте скважины"),
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
        error_messages={"unique": _("Введенный email занят.")},
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
    ceo_name = forms.CharField(
        label=_("ФИО генерально директора"),
        max_length=100,
        label_suffix="",
        required=True,
        help_text=_("Обязательное поле, будет отображено на титуле паспорта."),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("И.И. Иванов"),
                "class": "form-control",
            }
        ),
    )
    originator_position = forms.CharField(
        label=_("Должность составителя паспорта"),
        max_length=100,
        label_suffix="",
        required=True,
        help_text=_("Обязательное поле, будет отображено в конце паспорта."),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Гидрогеолог"),
                "class": "form-control",
            }
        ),
    )

    originator_name = forms.CharField(
        label=_("ФИО составителя паспорта"),
        max_length=100,
        label_suffix="",
        required=True,
        help_text=_("Обязательное поле, будет отображено в конце паспорта."),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("В.В. Ватутин"),
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
                "class": "form-control-file",
            }
        ),
    )

    class Meta:
        model = Organization
        fields = [
            "org_name",
            "inn",
            "address",
            "email",
            "phone",
            "ceo_name",
            "originator_position",
            "originator_name",
            "logo",
        ]


class UpdateOrganizationForm(forms.ModelForm):
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
        help_text=_(
            "Наименование организации с сокращенной организационно-правовой формой"
        ),
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
        help_text=_("Адрес нужен для отображения в контактах в паспорте скважины"),
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
        help_text=_("Телефон организации с кодом страны"),
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
        help_text=_(
            "Необязательное поле. Будет отображаться на титуле паспорта скважины"
        ),
        widget=forms.FileInput(attrs={"multiple": False, "class": "form-control-file"}),
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
            allowed_extensions = ["png", "jpg", "jpeg"]
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


class UpdateOrganizationLogoForm(forms.ModelForm):
    logo = forms.ImageField(
        label=_("Логотип"),
        required=False,
        help_text=_(
            "Необязательное поле. Будет отображаться на титуле паспорта скважины"
        ),
        widget=forms.FileInput(
            attrs={
                "multiple": False,
                "class": "form-control-file",
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
            allowed_extensions = ["png", "jpg", "jpeg"]
            extension = str(logo.name).lower().split(".")[-1]
            if extension not in allowed_extensions:
                raise ValidationError(
                    _(
                        "Недопустимое расширение файла. Допустимы только файлы с расширениями .png, .jpg, .jpeg."
                    )
                )
        organization = self.instance
        if organization.logo:
            # Получаем путь к файлу старого логотипа
            old_logo_path = os.path.join(settings.MEDIA_ROOT, str(organization.logo))

            # Проверяем, что файл существует, и удаляем его
            if os.path.isfile(old_logo_path):
                os.remove(old_logo_path)
        return logo

    class Meta:
        model = Organization
        fields = ["logo"]
