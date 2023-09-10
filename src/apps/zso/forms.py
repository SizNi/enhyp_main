from django import forms
from django.utils.translation import gettext_lazy as _
from apps.zso.models import Zso


class ZsoFirstCreateForm(forms.ModelForm):
    project_name = forms.CharField(
        label=_("Название проекта"),
        max_length=100,
        label_suffix="",
        required=True,
        help_text=_("поможет в дальнейшем ориентироваться по собственным проектам"),
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
            }
        ),
    )
    k_f_min = forms.FloatField(
        label=_("Коэффициент фильтрации"),
        label_suffix="",
        required=True,
        help_text=_("м/сут"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("1.2"),
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
        label=_("Градиент потока подземных вод"),
        label_suffix="",
        min_value=0.0,
        max_value=1.0,
        required=True,
        help_text=_("м/м"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.0001,
                "placeholder": _("0.0001"),
                "class": "form-control",
            }
        ),
    )
    i_max = forms.FloatField(
        label=_("Максимальное значение градиента потока подземных вод"),
        label_suffix="",
        min_value=0.0,
        max_value=1.0,
        required=True,
        help_text=_("м/м"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.0001,
                "placeholder": _("0.01"),
                "class": "form-control",
            }
        ),
    )

    alfa_min = forms.FloatField(
        label=_("Направление потока подземных вод"),
        label_suffix="",
        required=True,
        min_value=0.0,
        max_value=360.0,
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
        min_value=0.0,
        max_value=360.0,
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
        label=_("Мощность водоносного пласта"),
        label_suffix="",
        required=True,
        help_text=_("м"),
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
        label=_("Пористость водовмещающих пород"),
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
        help_text=_("ед"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("3"),
                "class": "form-control",
            }
        ),
    )

    iteration_count = forms.IntegerField(
        label=_("Количество вероятностных итераций"),
        label_suffix="",
        required=True,
        min_value=1,
        max_value=200,
        help_text=_("ед"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("100"),
                "class": "form-control",
            }
        ),
    )
    b_size = forms.FloatField(
        label=_("Длина грани блока модели"),
        label_suffix="",
        required=True,
        help_text=_("м"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("10.0"),
                "class": "form-control",
            }
        ),
    )
    n_x = forms.IntegerField(
        label=_("Размер модели"),
        label_suffix="",
        required=True,
        min_value=1,
        max_value=200,
        help_text=_("блок"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("40"),
                "class": "form-control",
            }
        ),
    )
    n_y = forms.IntegerField(
        label=_("Размер модели по оси Y в блоках"),
        label_suffix="",
        required=True,
        min_value=1,
        max_value=200,
        help_text=_("блок"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("40"),
                "class": "form-control",
            }
        ),
    )
    d_t = forms.FloatField(
        label=_("Размер временного шага"),
        label_suffix="",
        required=True,
        help_text=_("сутки"),
        widget=forms.NumberInput(
            attrs={
                "step": 0.1,
                "placeholder": _("1.0"),
                "class": "form-control",
            }
        ),
    )
    n_step = forms.IntegerField(
        label=_("Количество временных шагов"),
        label_suffix="",
        required=True,
        min_value=1,
        max_value=400,
        help_text=_("ед"),
        widget=forms.NumberInput(
            attrs={
                "step": 1,
                "placeholder": _("200 для расчета ЗСО-II при временном шаге = 1"),
                "class": "form-control",
            }
        ),
    )
    DISTRIBUTION_TYPE = (
        ("random", "Случайное"),
        ("normal", "Нормальное"),
        ("lognormal", "Логнормальное"),
        ("uniform", "Равномерное"),
    )
    type = forms.ChoiceField(
        choices=DISTRIBUTION_TYPE,
        initial="random",
        label=_("Тип распределения параметров в интервале"),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    # валидатор
    def clean(self):
        cleaned_data = super().clean()
        k_f_min = cleaned_data.get("k_f_min")
        k_f_max = cleaned_data.get("k_f_max")
        i_min = cleaned_data.get("i_min")
        i_max = cleaned_data.get("i_max")
        alfa_min = cleaned_data.get("alfa_min")
        alfa_max = cleaned_data.get("alfa_max")
        m_min = cleaned_data.get("m_min")
        m_max = cleaned_data.get("m_max")
        por_min = cleaned_data.get("por_min")
        por_max = cleaned_data.get("por_max")
        if k_f_min and k_f_max:
            if float(k_f_min) > float(k_f_max):
                self.add_error(
                    "k_f_min",
                    "Минимальное значение коэффициента фильтрации должно быть меньше или равно максимальному значению.",
                )
        if i_min and i_max:
            if float(i_min) > float(i_max):
                self.add_error(
                    "i_min",
                    "Минимальное значение уклона должно быть меньше или равно максимальному значению.",
                )
        if alfa_min and alfa_max:
            if float(alfa_min) > float(alfa_max):
                self.add_error(
                    "alfa_min",
                    "Минимальное значение угла потока должно быть меньше или равно максимальному значению.",
                )
        if m_min and m_max:
            if float(m_min) > float(m_max):
                self.add_error(
                    "m_min",
                    "Минимальное значение мощности пласта должно быть меньше или равно максимальному значению.",
                )
        if por_min and por_max:
            if float(por_min) > float(por_max):
                self.add_error(
                    "por_min",
                    "Минимальное значение пористости должно быть меньше или равно максимальному значению.",
                )

    class Meta:
        model = Zso
        fields = [
            "project_name",
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
            "iteration_count",
            "b_size",
            "n_x",
            "n_y",
            "d_t",
            "n_step",
            "type",
        ]
