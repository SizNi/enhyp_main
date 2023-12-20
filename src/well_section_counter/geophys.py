import lasio
import matplotlib.pyplot as plt
import math
import numpy as np


# распознование и визуализация .las файлов
# массив названий
names = {
    "DEPT": "Глубина, м",
    "D": "Кавернометрия КМ, мм",
    "PZ": "Электрокартоаж Пз, Омм",
    "GZ": "Электрокаротаж Гз, Омм",
    "PS": "Электрокаротаж Пс, мВ",
    "GK": "Гамма-каротаж ГК, мкР/ч",
    "TM": "Термометрия ТМ, °С",
    "RM": "Резистивиметрия РМ, Омм",
    "KM": "Кавернометрия КМ, мм",
}

data_color_dict = {
    "PZ": "#0000ff",
    "GZ": "#ff0000",
    "PS": "#ff00ff",
    "TM": "#ff0080",
    "RM": "#800080",
    "RM_1": "#ff0000",
    "RM_2": "#ff8040",
    "RM_3": "#00ff00",
    "RM_4": "#0080ff",
    "GK": "#000000",
    "KM": "#008000",
    "D": "#008000",
}


def lac_read(way="well_section_counter/las/1.las"):
    # чтение файла
    las = lasio.read(way)
    # чтение ключей из файла
    keys = las.keys()
    # print(keys)
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
    # создание рисунка
    fig, ax1 = plt.subplots(figsize=(width_inch, height_inch))

    # задание оси глубины
    dept = las["DEPT"]
    ax1_max_y = math.ceil((dept[-1]) / 10) * 10
    ax1.set_ylim(0, ax1_max_y)
    ax1.invert_yaxis()
    # добавление текста с забоем скважины
    max_dept_label = f"Забой: {max(dept)} м"
    ax1.text(
        0.9,
        0.008,
        max_dept_label,
        ha="center",
        va="center",
        fontsize=axis_label_fontsize,
        color="black",
        transform=ax1.transAxes,
    )
    # отдельный цикл для задания границ горизонтальных осей для всех RM (у них должен быть единый масштаб, так что вынес отдельно)
    rm_data = []
    for key in keys:
        if key.startswith("RM"):
            data = las[key]
            valid_data = data[~np.isnan(data)]
            rm_data.extend(valid_data)
    if "RM" in keys:
        # Преобразуем в массив NumPy для удобства работы
        rm_data = np.array(rm_data)
        # Получаем среднее для всех RM
        mean = np.mean(rm_data)
        if mean >= 25:
            # Задаем отклонение в 10% от среднего значения
            threshold = 0.1 * mean
            # Фильтруем данные в стороны от среднего
            filtered_rm_data = rm_data[
                (rm_data >= mean - threshold) & (rm_data <= mean + threshold)
            ]
            # Задаем границы для горизонтальных осей для RM
            rm_min = 0
            rm_max = math.ceil(max(filtered_rm_data + 1) / 10) * 10
        else:
            rm_min = 0
            rm_max = 32
        # расчитываем расположение уровня ПВ - пока не работает
        data = las["RM"]
        valid_data = data[~np.isnan(data)]
        target_depth = np.interp(max(valid_data), las["RM"], las["DEPT"])
        print(max(valid_data))
        print(target_depth)
    # смещение осей
    offset = 0
    # цикл построения параметров
    for key in keys:
        if key == "DEPT":
            color = "None"
        else:
            color = data_color_dict[key]
        # получаем данные по ключам
        data = las[key]
        valid_data = data[~np.isnan(data)]
        ax = ax1.twiny()
        ax.plot(data, dept, color=color, label=key, linewidth=line)
        ax_min = min(valid_data)
        ax_max = max(valid_data)
        # выбор границы шкал для параметров
        if key.startswith("RM"):
            ax_max = rm_max
            ax_min = rm_min
        elif ax_max <= 20:
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
        elif ax_max <= 400:
            ax_max = 400
            ax_min = 0
            step = 12
        elif ax_max <= 800:
            ax_max = 800
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
        # Дополнение к смещеню горизонтальных осей
        if key == "DEPT":
            offset += 0
        else:
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
    fig.savefig(
        "well_section_counter/log.png",
        dpi=600,
        orientation="portrait",
    )


lac_read()
