from django import forms
from django.utils.translation import gettext_lazy as _
from apps.well_passport.models import WellPassport


class WellPassportCreateForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('', 'Первичный'),
        ('восстановленный', 'Восстановленный'),
    )
    # Заголовок "Общие данные"
    project_name = forms.CharField(
        label=_("Название проекта"),
        label_suffix="",
        initial="Проект 'Орел-1'",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    organization = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control', "class": "form-control",}),
        label=_("Выберите организацию-составителя паспорта"),
        label_suffix="",
        required=True,
    )
    well_number = forms.CharField(
        label=_("Номер скважины"),
        label_suffix="",
        required=True,
        help_text=_("Обозначение скважины на титуле"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("ГВК 0001"),
                "class": "form-control",
            }
        ),
    )
    passport_type = forms.ChoiceField(
        label=_("Тип паспорта"),
        initial='',
        choices=TYPE_CHOICES,
        widget=forms.Select(
        attrs={'class': 'form-control',}),
    )
    # Заголовок "Местоположение скважины"
    republic = forms.CharField(
        label=_("Республика"),
        label_suffix="",
        initial="Российская Федерация",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    region = forms.CharField(
        label=_("Область"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Московская область"),
                "class": "form-control",
            }
        ),
    )
    district = forms.CharField(
        label=_("Городской округ"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Ленинский"),
                "class": "form-control",
            }
        ),
    )
    location = forms.CharField(
        label=_("Местоположение"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("д. Ватутинки, дом 101"),
                "class": "form-control",
            }
        ),
    )
    well_owner = forms.CharField(
        label=_("Владелец скважины"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("ООО 'Моя оборона'"),
                "class": "form-control",
            }
        ),
    )
    mailing_adress = forms.CharField(
        label=_("Почтовый адрес владельца скважины"),
        label_suffix="",
        required=True,

        widget=forms.TextInput(
            attrs={
                "placeholder": _("364024, Чеченская республика, г. Грозны, р-н Ахматовский, ул. Назарбаева 116'"),
                "class": "form-control",
            }
        ),
    )
    NL = forms.CharField(
        label=_("Северная широта"),
        label_suffix="",
        required=True,
        help_text=_("десятичный формат, WGS-84 (EPSG:4326)"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("55.546558362"),
                "class": "form-control",
            }
        ),
    )
    SL = forms.CharField(
        label=_("Восточная долгота"),
        label_suffix="",
        required=True,
        help_text=_("десятичный формат, WGS-84 (EPSG:4326)"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("37.928814267"),
                "class": "form-control",
            }
        ),
    )
    ground_lvl = forms.FloatField(
        label=_("А.О. устья скважины"),
        label_suffix="",
        required=True,
        help_text=_("м"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("191.5"),
                "class": "form-control",
            }
        ),
    )
    well_type = forms.CharField(
        label=_("Тип скважины"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Артезианская"),
                "class": "form-control",
            }
        ),
    )
    well_purpose = forms.CharField(
        label=_("Назначение скважины"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Для хозяйственно-бытового водоснабжения"),
                "class": "form-control",
            }
        ),
    )
    # Заголовок "Технические данные по сооруженной скважине"
    drilling_method = forms.CharField(
        label=_("Способ бурения"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("вращательный"),
                "class": "form-control",
            }
        ),
    )
    rig = forms.CharField(
        label=_("Название буровой установки"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("УРБ 2А-2"),
                "class": "form-control",
            }
        ),
    )
    project_owner = forms.CharField(
        label=_("Наименование проектной организации"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("ТРЕСТ 'ПРОМБУРВОД'"),
                "class": "form-control",
            }
        ),
    )
    drilling_company = forms.CharField(
        label=_("Наименование буровой организации"),
        label_suffix="",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("ТРЕСТ 'ПРОМБУРВОД'"),
                "class": "form-control",
            }
        ),
    )
    start = forms.DateField(
        label=_("Начало буровых работ"),
        label_suffix="",
        required=True,
        widget=forms.SelectDateWidget(
            attrs={
                "class": "form-control",
            }
        ),
    )
    end = forms.DateField(
        label=_("Окончание буровых работ"),
        label_suffix="",
        required=True,
        widget=forms.SelectDateWidget(
            attrs={
                "class": "form-control",
            }
        ),
    )
    # Заголовок "Данные по ОФР в скважине"
    pump_power = forms.FloatField(
        label=_("Производительность насоса"),
        label_suffix="",
        help_text=_("м.куб/час"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.5,
                "placeholder": _("6.0"),
                "class": "form-control",
            }
        ),
    )
    pump_column = forms.FloatField(
        label=_("Диаметр водоподъемных труб"),
        label_suffix="",
        help_text=_("мм"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("50.0"),
                "class": "form-control",
            }
        ),
    )
    debit = forms.FloatField(
        label=_("Реальный дебит скважины"),
        label_suffix="",
        help_text=_("м.куб/час"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("50.0"),
                "class": "form-control",
            }
        ),
    )
    ##################################

    class Meta:
        model = WellPassport
        fields = (
            'well_number',
            'passport_type',
            'republic',
            'region',
            'district',
            'location',
            'well_owner',
            'mailing_address',
            'NL',
            'SL',
            'ground_level',
            'well_type',
            'well_purpose',
            'drilling_method',
            'rig',
            'project_owner',
            'drilling_company',
            'start',
            'end',
            'pump_power',
            'pump_column',
            'debit',
        )
