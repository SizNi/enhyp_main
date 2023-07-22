from zso_counter.app import app_start
from apps.zso.models import Zso
import json
import numpy as np


# вытаскиваю перменные из бд, обрабатываю и отправляю в рассчетный моудль
def counter(zso_id):
    zso = Zso.objects.get(id=zso_id)
    k_f_min = zso.k_f_min
    k_f_max = zso.k_f_max
    i_min = zso.i_min
    i_max = zso.i_max
    alfa_min = zso.alfa_min
    alfa_max = zso.alfa_max
    m_min = zso.m_min
    m_max = zso.m_max
    por_min = zso.por_min
    por_max = zso.por_max
    type = zso.type
    iteration_count = zso.iteration_count
    n_x_skv = np.array(json.loads(zso.n_x_skv))
    n_y_skv = np.array(json.loads(zso.n_y_skv))
    n_x = zso.n_x
    n_y = zso.n_y
    d_t = zso.d_t
    n_step = zso.n_step
    b_size = zso.b_size
    q_main = np.array(json.loads(zso.debits))
    d_x = np.full(n_x, b_size)
    d_y = np.full(n_y, b_size)
    try:
        image, main_dataset = app_start(
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
        )
        return image, main_dataset
    except:
        return False
