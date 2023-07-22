from zso_counter.main_counter import main
from zso_counter.map import front_map
from tqdm import tqdm
import numpy as np
from zso_counter.start_parameters import distribution_array
import json

"""
# количество итераций
iteration_count = 100
# размеры модели в блоках
n_x = n_y = 40
# координаты скважин
n_x_skv = np.array([20, 30, 25])
n_y_skv = np.array([20, 15, 20])
# размер блока
b_size = 10.0
# приращение
d_x = np.full(n_x, b_size)
d_y = np.full(n_y, b_size)
# временной шаг
d_t = 1
# количество временных шагов
n_step = 200
# тип распределения параметров
type = "random" """


def app_start(
    k_f_min,
    k_f_max,
    i_min,
    i_max,
    alfa_min,
    alfa_max,
    m_min,
    m_max,
    por_min,
    por_max,
    type,
    iteration_count,
    n_x_skv,
    n_y_skv,
    n_x,
    n_y,
    d_x,
    d_y,
    d_t,
    n_step,
    b_size,
    q_main,
):
    bar_main = tqdm(total=iteration_count, desc="Iteration")
    # формирование массива случайных коэффициентов для задачи параметров
    data = distribution_array(
        k_f_min,
        k_f_max,
        i_min,
        i_max,
        alfa_min,
        alfa_max,
        m_min,
        m_max,
        por_min,
        por_max,
        iteration_count,
        type,
    )
    # первый вызов функции и получение основного датасета
    main_df = main(n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step, data, 0, q_main)
    bar_main.update(1)
    for iter in range(1, iteration_count):
        new_df = main(
            n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step, data, iter, q_main
        )
        # приращение вероятностей
        main_df.Migration_front += new_df.Migration_front
        bar_main.update(1)
    bar_main.close()
    # переводим вероятности из единиц в проценты (округление до единицы)
    main_df.Migration_front = main_df.Migration_front * (100 / iteration_count)
    # сохраняем датасет на всякий
    main_df.to_csv("zso_counter/main_dataset.csv", index=False)
    # функция-визуализатор
    image = front_map(type, main_df, n_x_skv, n_y_skv, b_size, n_x, n_y)
    return image


if __name__ == "__main__":
    app_start()
