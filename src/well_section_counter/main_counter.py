import math
from well_section_counter.index_colours import colour, convertation
from well_section_counter.specks import speck
from well_section_counter.format import frmt
from well_section_counter.inclusion import inclus
from well_section_counter.fixtures import well_data_4
import drawSvg as draw
import textwrap


# размер листа А4 при плотности пикселей 300 dpi

width, height, koef = frmt("a4")


def main(well_dt, path="generated_cross.png"):
    well_depth = well_dt["well_data"]["well_depth"]
    d = draw.Drawing(width, height, origin=(0, 0), displayInline=False)
    # Подложка
    r = draw.Rectangle(0, 0, 210 * koef, 297 * koef, fill="white", stroke="black")
    d.append(r)
    # контур рисунка
    r = draw.Rectangle(
        10 * koef, 7 * koef, 198 * koef, 275 * koef, fill="white", stroke="black"
    )
    d.append(r)
    # создает заголовки таблиц
    header(d)
    # создает масштабную линейку
    scale(d, well_depth)
    # отрисовывает геологические слои
    layers(d, well_depth, well_dt)
    # отрисовывает все относящиеся к скважине
    well(d, well_dt)
    # d.savePng(path)
    return d.rasterize().asDataUri


# выбор масштаба (размер секции и количество секций)
def scaling(well_depth):
    sections = {50: 5, 100: 10, 200: 20, 300: 30, 400: 40, 500: 50}

    for depth, section in sections.items():
        if well_depth <= depth:
            section_numbers = round((well_depth + (section / 2) - 0.1) / section)
            return section, section_numbers

    raise ValueError("Глубина скважины превышает допустимую")


# Создание таблицы с наименованием столбцов
def header(d):
    # d x1, y1, x2, y2
    # создание заголовка таблицы (надо немного поправить перенос строк, для таблицы
    # можно сделать его вручную)
    rectangle(d, 10, 297 - 15, 12, -25, "Масштаб", "v")
    rectangle(d, 22, 297 - 15, 12, -25, "№ слоя", "v")
    rectangle(d, 34, 297 - 15, 12, -25, "Возраст", "v")
    rectangle(d, 46, 297 - 15, 30, -25, "Описание     пород", "h_head")
    rectangle(d, 76, 297 - 15, 30, -25, "Разрез   скважины", "h_head")
    rectangle(d, 106, 297 - 15, 45, -10, "Залегание слоя, м", "h_head")
    rectangle(d, 106, 297 - 25, 15, -15, "От", "h_head")
    rectangle(d, 121, 297 - 25, 15, -15, "До", "h_head")
    rectangle(d, 136, 297 - 25, 15, -15, "Мощность", "h_head")
    rectangle(d, 151, 297 - 15, 12, -25, "Уровень, м", "v")
    rectangle(d, 163, 297 - 15, 45, -10, "Конструкция скважины", "h_head")
    rectangle(d, 163, 297 - 25, 22.5, -15, "Диаметр, мм", "h_head")
    rectangle(d, 185.5, 297 - 25, 22.5, -15, "Глубина, м", "h_head")


# риусет масштабную линейку слева
def scale(d, well_depth):
    # выбираем масштаб и количество делений
    section, section_numbers = scaling(well_depth)
    # колчичество мм на секцию (вся шкала растягивается на 250 мм)
    mm_section = 250 / section_numbers
    y_start = 297 - 15 - 25 - mm_section
    for number in range(section_numbers):
        # строим прямоугольник
        # rectangle(d, 10, 297-15, 12, -25, 'Масштаб', 'v')
        r = draw.Rectangle(
            10 * koef,
            y_start * koef,
            12 * koef,
            mm_section * koef,
            fill="white",
            stroke="black",
        )
        d.append(r)
        # проводим линию для текста (совпадает с низом прямоугольника)
        p = draw.Lines(
            (10) * koef,
            (y_start + 1) * koef,
            (22) * koef,
            (y_start + 1) * koef,
            close=False,
            stroke="white",
        )
        text = str((number + 1) * section)
        d.append(draw.Text([text], 40, path=p, text_anchor="middle"))
        y_start -= mm_section
    # смещение по x: (12, 12, 12, 30, 30, 45, 12, 45)
    # отрисовка прямоугольников под уровень и конструкцию скважины
    rectangle(d, 151, 257, 12, -well_depth * (mm_section / section), "white", "f")
    rectangle(d, 163, 257, 22.5, -well_depth * (mm_section / section), "white", "f")
    rectangle(d, 185.5, 257, 22.5, -well_depth * (mm_section / section), "white", "f")


# создание прямоугольника с текстом
def rectangle(d, x, y, x1, y1, text, direction):
    # f - заливать, h - с горизонтальным текстом, v - вертикальным, h_low - горизонтальный по низу
    # заготовка для добавления заливки
    if direction == "f":
        r = draw.Rectangle(
            x * koef, y * koef, x1 * koef, y1 * koef, fill=text, stroke="black"
        )
    else:
        r = draw.Rectangle(
            x * koef, y * koef, x1 * koef, y1 * koef, fill="white", stroke="black"
        )
    d.append(r)
    # создание переноса строки если надо
    if (
        direction != "f"
        and (len(text) <= x1 / 2.1 or direction == "v")
        and direction != "h_low"
        and direction != "h_head"
    ):
        # расположение текста в завимости от ориентации текста
        if direction == "v":
            p = draw.Lines(
                (x + x1 / 2 + 1) * koef,
                (y + y1) * koef,
                (x + x1 / 2 + 1) * koef,
                y * koef,
                close=False,
                stroke="black",
            )
        else:
            p = draw.Lines(
                (x) * koef,
                (y + y1 / 2 - 1) * koef,
                (x + x1) * koef,
                (y + y1 / 2 - 1) * koef,
                close=False,
                stroke="white",
            )
        d.append(draw.Text([text], 40, path=p, text_anchor="middle"))
    # Подпись глубины слоев
    elif direction == "h_low":
        p = draw.Lines(
            (x) * koef,
            (y + y1 + 1) * koef,
            (x + x1) * koef,
            (y + y1 + 1) * koef,
            close=False,
            stroke="white",
        )
        d.append(draw.Text([text], 40, path=p, text_anchor="middle"))
    # Название столбоцв для шапки
    elif direction == "h_head":
        # изменение шрифта в зависимости от размера блока в шапке
        if x1 >= 45:
            text_separate = 25
            text_size = 40
        elif x1 > 22.5 and x1 < 45:
            text_separate = 16
            text_size = 40
        elif x1 > 15 and x1 <= 22.5:
            text_separate = 16
            text_size = 30
        elif x1 <= 15:
            text_separate = 8
            text_size = 30
        number_str = len(
            textwrap.wrap(
                text, text_separate, break_long_words=False, break_on_hyphens=False
            )
        )
        # центирование блока текста в прямоугольнике в зависимости от количества строк
        if number_str == 1:
            central_koef = 6.2
        else:
            central_koef = 5
        # разбиение текста по строкам
        new_text = "\n".join(
            textwrap.wrap(
                text, text_separate, break_long_words=False, break_on_hyphens=False
            )
        )
        # Первоначальное положение строки
        start_text = y1 / 2 + (5 - central_koef) / 2 * number_str
        # расположение первоначальной строки (привязывается к линии)
        p = draw.Lines(
            (x) * koef,
            (y + start_text) * koef,
            (x + x1) * koef,
            (y + start_text) * koef,
            close=False,
            stroke="white",
        )
        d.append(draw.Text(new_text, text_size, path=p, text_anchor="middle"))
    elif direction == "h":
        text_separate = 18
        # изменение размера текста для маленьких блоков:
        if y - y1 <= 30:
            text_size = 20
            text_separate = 30
            central_koef = 4.5
            number_str = len(
                textwrap.wrap(
                    text, text_separate, break_long_words=False, break_on_hyphens=False
                )
            )
        else:
            number_str = len(
                textwrap.wrap(
                    text, text_separate, break_long_words=False, break_on_hyphens=False
                )
            )
            if number_str * 5 >= -0.8 * y1:
                text_size = 30
                # центирование блока текста в прямоугольнике
                if number_str == 1:
                    central_koef = 6.2
                else:
                    central_koef = 4
            elif number_str * 5 < -0.8 * y1:
                text_size = 30
                central_koef = 4
        # разбиение текста по строкам
        new_text = "\n".join(
            textwrap.wrap(
                text, text_separate, break_long_words=False, break_on_hyphens=False
            )
        )
        # Первоначальное положение строки
        start_text = y1 / 2 + (5 - central_koef) / 2 * number_str
        # расположение первоначальной строки (привязывается к линии)
        p = draw.Lines(
            (x) * koef,
            (y + start_text) * koef,
            (x + x1) * koef,
            (y + start_text) * koef,
            close=False,
            stroke="white",
        )
        d.append(draw.Text(new_text, text_size, path=p, text_anchor="middle"))


# создание слоя
def layers(d, well_depth, dt):
    # выбираем масштаб
    data = dt["layers"]
    section, section_numbers = scaling(well_depth)
    # смещение по x: (12, 12, 12, 30, 30, 15, 15, 12, 22.5, 22.5)
    # деля 250 на округленную глубину скважины - получаем сколько в мм метров
    scale_m = 250 / (section_numbers * section)
    # стартовые положения.
    h_start = 0.0  # глубина
    y_start = 297 - 15 - 25  # смещение по y после добавления заголовков
    for elem in data:
        x_start = 10 + 12
        rectangle(
            d,
            x_start,
            y_start,
            12,
            -data[elem]["thick"] * scale_m,
            str(data[elem]["id"]),
            "h",
        )
        x_start += 12
        # ориентация для длинных индексов горизонтов
        if len(data[elem]["name"]) > 3:
            direction = "v"
        else:
            direction = "h"
        # приводим геологический индекс к нужному регистру
        low_index = convertation(data[elem]["name"])
        rectangle(
            d,
            x_start,
            y_start,
            12,
            -data[elem]["thick"] * scale_m,
            low_index,
            direction,
        )
        x_start += 12
        # преобразование отложений из кортежа в строку для описания разреза
        sediments_text = (", ".join(data[elem]["sediments"])).capitalize()
        if "interlayers" in data[elem] and data[elem]["interlayers"] != []:
            sediments_text += ". Прослои: " + ", ".join(data[elem]["interlayers"])
        # добавление вкраплений
        if "inclusions" in data[elem] and data[elem]["inclusions"] != []:
            sediments_text += ". Вкрапления: " + ", ".join(data[elem]["inclusions"])
        rectangle(
            d, x_start, y_start, 30, -data[elem]["thick"] * scale_m, sediments_text, "h"
        )
        x_start += 30
        layer_fill = colour(low_index)
        rectangle(
            d, x_start, y_start, 30, -data[elem]["thick"] * scale_m, layer_fill, "f"
        )
        # добавление вкраплений
        if "inclusions" in data[elem]:
            inclus(
                d,
                x_start,
                y_start,
                30,
                data[elem]["thick"] * scale_m,
                data[elem]["inclusions"],
            )
        # добавление прослоев
        if "interlayers" in data[elem]:
            speck(
                d,
                x_start,
                y_start,
                30,
                data[elem]["thick"] * scale_m,
                data[elem]["sediments"],
                data[elem]["interlayers"],
            )
        else:
            speck(
                d,
                x_start,
                y_start,
                30,
                data[elem]["thick"] * scale_m,
                data[elem]["sediments"],
                None,
            )
        x_start += 30
        # подумать как убрать подписи вниз (к низу прямоугольника)
        rectangle(
            d,
            x_start,
            y_start,
            15,
            -data[elem]["thick"] * scale_m,
            str(format(h_start, ".1f")),
            "h_low",
        )
        x_start += 15
        h_start += data[elem]["thick"]
        rectangle(
            d,
            x_start,
            y_start,
            15,
            -data[elem]["thick"] * scale_m,
            str(format(h_start, ".1f")),
            "h_low",
        )
        x_start += 15
        rectangle(
            d,
            x_start,
            y_start,
            15,
            -data[elem]["thick"] * scale_m,
            str(format(data[elem]["thick"], ".1f")),
            "h_low",
        )
        y_start -= data[elem]["thick"] * scale_m
        # завершение цикла отрисовки геологии


def well(d, well_dt):
    data = well_dt["well_data"]
    # масштаб
    section, section_numbers = scaling(data["well_depth"])
    scale_m = 250 / (section_numbers * section)
    # стартовый диаметр внутренней колонны
    d_start = (30 / 2) / (len(data["columns"])) + 2 * len(data["columns"])
    for elem in data["columns"]:
        column = data["columns"][elem]
        y_start = 257 - column["from"] * scale_m
        x_start = 76 + (30 - d_start) / 2
        # добавление интервалов фильтра
        if column["type"] == "фильтровая":
            rectangle(
                d,
                x_start,
                y_start,
                d_start,
                (column["from"] - column["till"]) * scale_m,
                "white",
                "f",
            )
            # отрисовка конструкции и глубин для колонн
            p = draw.Lines(
                163 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                185.5 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                close=False,
                stroke="black",
            )
            text = "Ф.К. " + str(column["D"])
            d.append(draw.Text(text, 40, path=p, text_anchor="middle"))
            p = draw.Lines(
                185.5 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                208 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                close=False,
                stroke="black",
            )
            d.append(draw.Text(str(column["till"]), 40, path=p, text_anchor="middle"))
            p = draw.Lines(
                163 * koef,
                (257 - column["till"] * scale_m) * koef,
                208 * koef,
                (257 - column["till"] * scale_m) * koef,
                close=False,
                stroke="black",
            )
            d.append(p)
            filter = column["filter"]
            for f_elem in filter:
                # отрисовка градиента фильтра и интервалов
                gradient = draw.LinearGradient(
                    x_start * koef,
                    (257 - filter[f_elem]["from"] * scale_m) * koef,
                    (x_start + d_start) * koef,
                    (257 - filter[f_elem]["from"] * scale_m) * koef,
                )
                gradient.addStop(0, "#bdc4ff", 1)
                gradient.addStop(1, "#0315b5", 0)
                rectangle(
                    d,
                    x_start,
                    257 - filter[f_elem]["from"] * scale_m,
                    d_start,
                    (filter[f_elem]["from"] - filter[f_elem]["till"]) * scale_m,
                    gradient,
                    "f",
                )
        # построение открытого ствола
        elif column["type"] == "О.С.":
            r = draw.Rectangle(
                x_start * koef,
                y_start * koef,
                d_start * koef,
                (column["from"] - column["till"]) * scale_m * koef,
                fill="white",
                fill_opacity=0.8,
                stroke="blue",
                stroke_dasharray="5, 5",
            )
            d.append(r)
            p = draw.Lines(
                163 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                185.5 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                close=False,
                stroke="black",
            )
            text = "О.С. " + str(column["D"])
            d.append(draw.Text(text, 40, path=p, text_anchor="middle"))
            p = draw.Lines(
                185.5 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                208 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                close=False,
                stroke="white",
            )
            d.append(draw.Text(str(column["till"]), 40, path=p, text_anchor="middle"))
        elif column["type"] == "обсадная":
            rectangle(
                d,
                x_start,
                y_start,
                d_start,
                (column["from"] - column["till"]) * scale_m,
                "white",
                "f",
            )
            # добавление данных по диаметру обсадных колонн
            p = draw.Lines(
                163 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                185.5 * koef,
                (257 - column["till"] * scale_m + 1) * koef,
                close=False,
                stroke="white",
            )
            d.append(draw.Text(str(column["D"]), 40, path=p, text_anchor="middle"))
            p = draw.Lines(
                163 * koef,
                (257 - column["till"] * scale_m) * koef,
                185.5 * koef,
                (257 - column["till"] * scale_m) * koef,
                close=False,
                stroke="black",
            )
            d.append(p)
            # добавление данных по глубинам
            p = draw.Lines(
                185.5 * koef,
                (y_start - (column["till"] - column["from"]) * scale_m + 1) * koef,
                208 * koef,
                (y_start - (column["till"] - column["from"]) * scale_m + 1) * koef,
                close=False,
                stroke="white",
            )
            d.append(draw.Text(str(column["till"]), 40, path=p, text_anchor="middle"))
            p = draw.Lines(
                185.5 * koef,
                (y_start - (column["till"] - column["from"]) * scale_m) * koef,
                208 * koef,
                (y_start - (column["till"] - column["from"]) * scale_m) * koef,
                close=False,
                stroke="black",
            )
            d.append(p)
        d_start -= 2
    # статический уровень
    if well_dt["well_data"]["static_lvl"]:
        st_lvl = well_dt["well_data"]["static_lvl"]
        p = draw.Lines(
            158 * koef,
            (257 - st_lvl * scale_m + 4) * koef,
            158 * koef,
            (257 - st_lvl * scale_m + 30) * koef,
            close=False,
            stroke="white",
        )
        d.append(draw.Text("С.У. " + str(st_lvl), 40, path=p, text_anchor="start"))
        p = draw.Lines(
            151 * koef,
            (257 - st_lvl * scale_m) * koef,
            163 * koef,
            (257 - st_lvl * scale_m) * koef,
            close=False,
            stroke="#00a8f0",
            stroke_width=5,
        )
        d.append(p)
    # динамический уровень
    if well_dt["well_data"]["dynamic_lvl"]:
        dn_lvl = well_dt["well_data"]["dynamic_lvl"]
        p = draw.Lines(
            158 * koef,
            (257 - dn_lvl * scale_m - 25) * koef,
            158 * koef,
            (257 - dn_lvl * scale_m - 1) * koef,
            close=False,
            stroke="white",
        )
        d.append(draw.Text("Д.У. " + str(dn_lvl), 40, path=p, text_anchor="middle"))
        p = draw.Lines(
            151 * koef,
            (257 - dn_lvl * scale_m) * koef,
            163 * koef,
            (257 - dn_lvl * scale_m) * koef,
            close=False,
            stroke="#001eff",
            stroke_width=5,
        )
        d.append(p)

    # насос
    if well_dt["well_data"]["pump_type"]:
        # диаметр насоса задается по той же формуле,
        # что и диаметр каждой последующей колонны
        x_start = 76 + (30 - d_start) / 2
        rectangle(
            d,
            x_start,
            257 - well_dt["well_data"]["pump_depth"] * scale_m,
            d_start,
            8,
            "#7a8aff",
            "f",
        )
        p = draw.Lines(
            76 * koef,
            (257 - well_dt["well_data"]["pump_depth"] * scale_m - 2) * koef,
            106 * koef,
            (257 - well_dt["well_data"]["pump_depth"] * scale_m - 2) * koef,
            close=False,
            stroke="white",
        )
        d.append(
            draw.Text(
                str(well_dt["well_data"]["pump_depth"]),
                20,
                path=p,
                text_anchor="middle",
            )
        )
        # водоподъемная труба
        p = draw.Lines(
            91 * koef,
            (257 - well_dt["well_data"]["pump_depth"] * scale_m + 8) * koef,
            91 * koef,
            257 * koef,
            close=False,
            stroke="#7a8aff",
            stroke_width=5,
        )
        d.append(p)
        # название насоса
        p = draw.Lines(
            90 * koef,
            (257 - well_dt["well_data"]["pump_depth"] * scale_m + 10) * koef,
            90 * koef,
            257 * koef,
            close=False,
            stroke="white",
        )
        d.append(
            draw.Text(
                str(well_dt["well_data"]["pump_type"]), 20, path=p, text_anchor="left"
            )
        )
