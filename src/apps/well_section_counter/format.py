# формат листа, плотность точек
def frmt(type, dpi=300):
    format = {
        "a4": (210, 297),
        "a3": (297, 420),
        "a2": (420, 594),
    }
    # из дюймов в мм
    dpi_mm = dpi / 25.4
    width = format[type][0] * dpi_mm
    height = format[type][1] * dpi_mm
    koef = width / format[type][0]
    return width, height, koef


# коэффициент пересчета мм -> % от общей ширины/высоты (2480/210 = 11,809 (1 мм в пикселях))
# 2480/100 = 24,8 пикселя в 1%, соответственно 1 мм = 11,809/24,8 = 0,4761% (по y)
# 3508/100 = 35,08 пикселя в 1%, соответственно 1 мм = 11,809/35,08 = 0,3366% (по x)
# общая высота рисунка (самой скважины) - 250 мм, названий столбцов - 25 мм
# mm_x = 0.004761
# mm_y = 0.003366
