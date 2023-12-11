import lasio
import matplotlib.pyplot as plt


def lac_read(way="maindir/src/well_section_counter/1.las"):
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
    line = 0.3

    # Конвертация в дюймы
    width_inch = width_mm / 25.4
    height_inch = height_mm / 25.4

    fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))
    # массив цветов
    colors = [
        "red",
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
    print(data_dict)
    # глубина
    dept = las["DEPT"]
    ax1.set_ylim(0, dept[-1])
    ax1.invert_yaxis()
    plt.grid(True)
    for key, color in data_dict.items():
        data = las[key]
        ax1.set_yticks([])
        ax1.set_yticklabels([])
        ax1.set_xticks([])
        ax1.set_xticklabels([])
        ax1.plot(data, dept, color=color, label=key, linewidth=line)

    fig.tight_layout()
    # сохранение изображения
    fig.savefig(
        "maindir/src/well_section_counter/log.png", dpi=300, orientation="portrait"
    )


lac_read()
