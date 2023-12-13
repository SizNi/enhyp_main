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
        "pink",
        "gray",
        "yellow",
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

    for key, color in data_dict.items():
        data = las[key]
        valid_data = data[~np.isnan(data)]
        ax = ax1.twiny()
        ax.plot(data, dept, color=color, label=key, linewidth=line)
        print(key)
        ax.set_xlim(0, math.ceil(max(valid_data)+0.1 * max(valid_data)))
        print(math.ceil(max(valid_data)+0.1 * max(valid_data)))
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_xticklabels([])
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
    # округление оси глубины
    # ax1.yaxis.set_major_locator(plt.MultipleLocator(10))
    """    ax1.spines["left"].set_position(("outward", -10))
    ax1.spines["left"].set_linewidth(0.5)
    ax1.spines["left"].set_color("black")"""
    fig.tight_layout()

    # сохранение изображения
    fig.savefig("well_section_counter/log.png", dpi=300, orientation="portrait")


lac_read()
