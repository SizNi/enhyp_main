import lasio
import matplotlib.pyplot as plt
import math
import numpy as np

# массив цветов
colors = [
    "None",
    "blue",
    "green",
    "purple",
    "orange",
    "black",
    "brown",
    "red",
    "gray",
    "darkblue",
    "magenta",
    "teal",
    "lime",
    "indigo",
    "olive",
]
# массив названий
names = {
    "DEPT": "Глубина, м",
    "D": "Диаметр, мм",
    "PZ": "Электрокартоаж Пз, Омм",
    "GZ": "Электрокартоаж Гз, Омм",
    "PS": "Электрокартоаж Пс, мВ",
    "GK": "Гамма-каротаж ГК, мкР/ч",
    "TM": "Термометрия ТМ, °С",
    "RM": "Резистивиметрия РМ, Омм",
    "KM": "Кавернометрия КМ, мм",
}


def lac_read(way="well_section_counter/1.las"):
    # чтение файла
    las = lasio.read(way)
    # чтение ключей из файла
    keys = las.keys()
    print(keys)

    # задание размеров рисунка в мм
    width_mm = 100
    height_mm = 250
    # задание размеров шрифта для подписей осей и для подписей значений осей
    label_fontsize = 5
    axis_label_fontsize = 5
    # толщина линии
    line = 0.5
    # длина тиков
    tick_length = 2
    # расстояние между тиком и подписью
    pad = 1

    # Конвертация в дюймы
    width_inch = width_mm / 25.4
    height_inch = height_mm / 25.4

    fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))

    # словарь метод:цвет
    data_dict = dict(zip(keys, colors))
    # глубина
    dept = las["DEPT"]
    ax1_max_y = math.ceil((dept[-1]) / 10) * 10
    ax1.set_ylim(0, ax1_max_y)
    ax1.invert_yaxis()
    # смещение осей
    offset = 0

    for key, color in data_dict.items():
        data = las[key]
        valid_data = data[~np.isnan(data)]
        ax = ax1.twiny()
        ax.plot(data, dept, color=color, label=key, linewidth=line)
        print(key)
        ax_min = min(valid_data)
        ax_max = max(valid_data)
        # выбор границы шкал для параметров
        if ax_max <= 20:
            ax_max = math.ceil((ax_max + 1) / 2) * 2
            ax_min = math.floor((ax_min) / 2) * 2
            step = 2
        elif ax_max <= 50:
            ax_max = math.ceil((ax_max + 2) / 5) * 5
            ax_min = 0
            step = 3
        elif ax_max <= 100:
            ax_max = math.ceil((ax_max + 2) / 10) * 10
            ax_min = 0
            step = 4
        elif ax_max <= 150:
            ax_max = math.ceil((ax_max + 2) / 15) * 15
            ax_min = 0
            step = 6
        elif ax_max <= 200:
            ax_max = math.ceil((ax_max + 2) / 20) * 20
            ax_min = 0
            step = 8
        elif ax_max <= 300:
            ax_max = math.ceil((ax_max + 2) / 30) * 30
            ax_min = 0
            step = 10
        elif ax_max <= 400:
            ax_max = math.ceil((ax_max + 2) / 40) * 40
            ax_min = 0
            step = 12
        elif ax_max <= 500:
            ax_max = math.ceil((ax_max + 2) / 50) * 50
            ax_min = 0
            step = 14
        elif ax_max <= 800:
            ax_max = math.ceil((ax_max + 2) / 80) * 80
            ax_min = 0
            step = 20
        elif ax_max <= 1000:
            ax_max = math.ceil((ax_max + 2) / 1000) * 1000
            ax_min = 0
            step = 20
        # количество тиков и подгонка значения для кратности на количество тиков
        num_ticks = 8
        remainder = (ax_max - ax_min) % 8
        if remainder != 0:
            ax_max += 8 - remainder
        # задание лимитов шкал
        ax.set_xlim(ax_min, ax_max)
        # выбор количества тиков по шкалам
        tick_step = (ax_max - ax_min) // num_ticks
        # print(ax_max, ax_min, tick_step)
        if tick_step == 0:
            tick_step = 1
        ax.xaxis.set_ticks(range(ax_min, ax_max + 1, tick_step))
        ax.invert_yaxis()
        ax.spines["top"].set_position(("outward", offset))
        ax.spines["top"].set_color(color)
        # подписи осей
        if key in names or key.startswith("RM"):
            if key == "RM":
                label_name = names[key]
            elif key.startswith("RM"):
                label_name = "РМ "
                print(key[-1])
                if key[-1].isdigit():
                    label_name += f'{key[-1] + ", Омм"}'
            else:
                label_name = names[key]
        ax.set_xlabel(label_name, fontsize=label_fontsize, labelpad=pad * 2)
        ax.tick_params(
            axis="x",
            colors=color,
            labelsize=axis_label_fontsize,
            length=tick_length,
            pad=pad,
            direction="in",
        )
        ax.xaxis.set_label_position("top")
        ax.xaxis.label.set_color(color)
        ax.tick_params(width=0.5)
        ax.spines["top"].set_linewidth(0.5)
        ax.spines["bottom"].set_linewidth(0.5)
        ax.spines["left"].set_linewidth(0.5)
        ax.spines["right"].set_linewidth(0.5)
        offset += 15
    # параметры вертикальной оси
    ax.grid(True, linewidth=0.2)
    ax1.grid(True, linewidth=0.2)
    ax1.grid(which="minor", linewidth=0.1)
    ax1.set_yticks(np.arange(0, ax1_max_y + 1, step=step))
    ax1.set_yticks(np.arange(0, ax1_max_y + 1, step=step / 2), minor=True)
    ax1.tick_params(
        axis="y",
        which="both",
        direction="in",
        labelsize=axis_label_fontsize,
    )
    # перенос вправо делений оси глубины
    ax1.yaxis.tick_right()
    ax1.yaxis.set_label_position("right")
    ax1.set_xticks([])
    ax1.set_xticklabels([])
    fig.tight_layout()
    # установка рамок рисунка
    ax1.spines["top"].set_linewidth(0.5)
    ax1.spines["bottom"].set_linewidth(0.5)
    ax1.spines["left"].set_linewidth(0.5)
    ax1.spines["right"].set_linewidth(0.5)
    ax1.tick_params(width=0.5)
    # сохранение изображения
    fig.savefig("well_section_counter/log.png", dpi=600, orientation="portrait")


lac_read()
