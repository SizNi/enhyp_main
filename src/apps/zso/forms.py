from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.zso.models import Zso


class ZsoFirstCreateForm(forms.ModelForm):
    k_f_min = forms.FloatField(
        label=_("Минимальное значение коэффициента фильтрации"),
        label_suffix="",
        required=True,
        help_text=_("м/сут"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("1.2"),
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
    k_f_max = forms.FloatField(
        label=_("Максимальное значение коэффициента фильтрации"),
        label_suffix="",
        required=True,
        help_text=_("м/сут"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("8.5"),
                "class": "form-control",
            }
        ),
    )
    i_min = forms.FloatField(
        label=_("Минимальное значение уклона потока подземных вод"),
        label_suffix="",
        required=True,
        help_text=_("градусы"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.0001,
                "placeholder": _("0.0001"),
                "class": "form-control",
            }
        ),
    )
    i_max = forms.FloatField(
        label=_("Максимальное значение уклона потока подземных вод"),
        label_suffix="",
        required=True,
        help_text=_("градусы"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.0001,
                "placeholder": _("0.01"),
                "class": "form-control",
            }
        ),
    )
    alfa_min = forms.FloatField(
        label=_("Минимальное значение направления потока подземных вод"),
        label_suffix="",
        required=True,
        help_text=_("градусы от 0 до 360"),
        widget=forms.NumberInput(
            attrs={
                "step": 1.0,
                "placeholder": _("270"),
                "class": "form-control",
            }
        ),
    )
    alfa_max = forms.FloatField(
        label=_("Максимальное значение направления потока подземных вод"),
        label_suffix="",
        required=True,
        help_text=_("градусы от 0 до 360"),
        widget=forms.NumberInput(
            attrs={
                "step": 1.0,
                "placeholder": _("330"),
                "class": "form-control",
            }
        ),
    )
    m_min = forms.FloatField(
        label=_("Минимальное значение мощности водоносного пласта"),
        label_suffix="",
        required=True,
        help_text=_("метры"),
        widget=forms.NumberInput(
            attrs={
                "step": 1.0,
                "placeholder": _("5"),
                "class": "form-control",
            }
        ),
    )
    m_max = forms.FloatField(
        label=_("Максимальное значение мощности водоносного пласта"),
        label_suffix="",
        required=True,
        help_text=_("метры"),
        widget=forms.NumberInput(
            attrs={
                "step": 1.0,
                "placeholder": _("10"),
                "class": "form-control",
            }
        ),
    )
    por_min = forms.FloatField(
        label=_("Минимальное значение пористости водовмещающих пород"),
        label_suffix="",
        required=True,
        help_text=_("безразмерный"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("0.2"),
                "class": "form-control",
            }
        ),
    )
    por_max = forms.FloatField(
        label=_("Максимальное значение пористости водовмещающих пород"),
        label_suffix="",
        required=True,
        help_text=_("безразмерный"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("0.4"),
                "class": "form-control",
            }
        ),
    )
    well_numbers = forms.IntegerField(
        label=_("Количество скважин"),
        label_suffix="",
        required=True,
        min_value=1,
        max_value=10,
        help_text=_("штука"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("3"),
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Zso
        fields = [
            "k_f_min",
            "k_f_max",
            "i_min",
            "i_max",
            "alfa_min",
            "alfa_max",
            "m_min",
            "m_max",
            "por_min",
            "por_max",
            "well_numbers",
        ]


class ZsoSecondCreateForm(forms.ModelForm):
    debits = forms.FloatField(
        label=_("расход скважины"),
        label_suffix="",
        required=True,
        help_text=_("м.куб/сут"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("36.6"),
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Zso
        fields = [
            "debits",
        ]
