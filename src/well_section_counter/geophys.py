import lasio
import matplotlib.pyplot as plt
import math
import numpy as np


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
    # массив цветов
    colors = [
        "None",
        "blue",
        "green",
        "purple",
        "orange",
        "cyan",
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
    # словарь метод:цвет
    data_dict = dict(zip(keys, colors))
    # глубина
    dept = las["DEPT"]
    ax1.set_ylim(0, dept[-1])
    ax1.invert_yaxis()
    plt.grid(True)
    # смещение осей
    offset = 0

    for key, color in data_dict.items():
        data = las[key]
        valid_data = data[~np.isnan(data)]
        ax = ax1.twiny()
        ax.plot(data, dept, color=color, label=key, linewidth=line)
        print(key)
        # задание лимитов шкал
        ax.set_xlim(0, math.ceil(max(valid_data) + 0.1 * max(valid_data)))
        ax.invert_yaxis()
        ax.spines["top"].set_position(("outward", offset))
        ax.spines["top"].set_color(color)
        ax.set_xlabel(key, fontsize=label_fontsize, labelpad=pad * 2)
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
        offset += 15
        # ax.set_xticks([])
        # ax.set_xticklabels([])
    # параметры вертикальной оси
    ax1.set_yticks(np.arange(0, dept[-1] + 1, step=10))
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

    # сохранение изображения
    fig.savefig("well_section_counter/log.png", dpi=300, orientation="portrait")


lac_read()
