import scipy
import math

from scipy import integrate


def f(x):
    return math.exp((x**2 / 2) * (-1))


class LTENetwork:
    def __init__(self, l, z, c, s = None):
        self.setup_variant(l, z)
        self.setup_serving_zone_params(s)
        self.setup_cluster_params(c)
        self.setup_up_down_params()
        self.setup_pK()
        self.setup_sps_params()
        self.setup_telephony_load()
        self.calc_subs_per_slot()
        self.calc_bs_quant()
        self.calc_zone_radius()
        self.calc_summary_losses()
        self.calc_asbs_losses()

        # print("Object created successfully")
        
    def setup_variant(self, list_num, z_value : str):
        self.list_number = list_num                                             # Номер по списку
        zachetka_value = z_value                                                # Номер в зачетке

        if len(zachetka_value) != 1:
            self.n = int(zachetka_value.strip()[0])                             # Первая цифра зачетки
            self.m = int(zachetka_value.strip()[1])                             # Вторая цифра зачетки
        elif zachetka_value.strip() == "00" or zachetka_value.strip() == "0":   # Если последние цифры равны нулю, то n и m равны 0
            self.n = self.m = int(zachetka_value[0].strip())                       

        match self.list_number % 2:                                             # Количество радиоканалов на один сектор (по условию четный не четный вариант)
            case 0: self.nc = 2
            case 1: self.nc = 1

    def setup_serving_zone_params(self, square = None):
        self.s = 200 + 55 * self.list_number if square == None else square      # Площадь обслуживаемой зоны
        self.subscribers_quant = 115000 + 3500 * self.list_number               # Количество абонентов
        self.subscriber_activity = 0.022 + 0.0006 * self.list_number            # Активность абонентов
        self.call_block_prob = 0.02 - 0.0004 * self.list_number                 # Вероятность блокировки вызова

        self.channels_per_sector = 2 if self.list_number % 2 == 0 else 1        # Количество каналов на сектор

        self.na = 64                                                            # Число разговорных каналов
        self.fk = 1.4                                                           # Полоса частот на один канал

    def setup_cluster_params(self, cl_sz):
        self.sigma = 4 + 0.55 * self.list_number                                # Отклонение уровня сигнала в месте приема
        self.signal_noise = 9                                                   # Отношение сигнал шум
        self.available_prob = 8 + 0.25 * self.list_number                       # Допустимая вероятность невыполнения требований
        self.cluster_size = cl_sz                                               # Размер кластера
        self.sectors_quant = 6                                                  # Количество секторов
        self.nn = 52                                                            # Число каналов для трафика

    def setup_up_down_params(self):
        self.freq = 1.8e6                                                       # Диапазон частот

        self.bs_as_line_power = 8 + 0.3 * self.m * self.n                       # Мощность передатчика БС АС
        self.as_bs_line_power = 0.03 + 0.01 * self.m * self.n                   # Мощность передатчика АС БС

        self.bs_as_line_feeder_loss = 0.45 + 0.01 * self.m * self.n             # Потери в фидере БС АС
        self.bs_as_line_duplex_filter_loss = 2.4 + 0.02 * self.m * self.n       # Потери в дуплексном фильтре БС АС
        self.bs_as_line_duplexor_loss = 2.9 + 0.05 * self.m * self.n            # Потери в диплексоре БС АС
        self.bs_as_line_antenna_gain = 8.0 + 0.1 * self.m * self.n              # Коэффициент усиления антенны БС АС

        self.lines_sensitivity = -100 + 0.01 * self.m * self.n                  # Чувствительность приемника БС АС / АС БС
        self.building_loss = 6 + 0.02 * self.m * self.n                         # Потери при проникновении в здание
        self.subscriber_body_loss = 2.5 + 0.01 * self.m * self.n                # Потери в теле абонента
        self.needed_correction = 2.72                                           # Требуемая поправка

    def setup_pK(self):
        q = math.sqrt(3*self.cluster_size)
        betta = math.pow(q + 1, -4)
        x1 = ((10 * math.log10(1/betta) - self.signal_noise) /
              (math.sqrt(math.pow(self.sigma, 2) + math.pow(self.sigma, 2))))
        integral = integrate.quad(func=f, a=x1, b=math.inf)

        self.pK = ((1 / math.sqrt(math.pow(math.pi, 2))) * integral[0]) * 100   # Вероятность невыполнения условий по отношению сигнал шум

    def setup_sps_params(self):
        self.nk = self.sectors_quant * self.cluster_size * self.nc              # Общее число частотных каналов
        self.delta_f = self.nk * self.fk                                        # Минимально возможная полоса частот
        self.ns = self.na * self.nc                                             # Общее число разговорных каналов

    def setup_telephony_load(self):
        if self.call_block_prob <= math.sqrt(2 / (self.nn * math.pi)):          # Телефонная нагрузка (вариант 1)
            self.a = self.nn * (1 -
                                math.sqrt(1 -
                                          math.pow(self.call_block_prob *
                                                   math.sqrt(self.nn * math.pi / 2), 1 / self.nn)))
        elif self.call_block_prob > math.sqrt(2 / (self.nn * math.pi)):         # Телефонная нагрузка (вариант 2)
            self.a = (self.nn +
                      math.sqrt(math.pi/2 +
                                2 * self.nn * math.log(self.call_block_prob * math.sqrt(self.nn*math.pi / 2), math.e)) -
                                        math.sqrt(math.pi / 2))

    def calc_subs_per_slot(self):
        self.nab = (self.a * self.subscriber_activity) * self.sectors_quant     # Количество абонентов на ячейку

    def calc_bs_quant(self):
        self.bs_quant = self.subscribers_quant / self.nab                       # Количество базовых станций

    def calc_zone_radius(self):
        self.rc = math.sqrt((2 / 3 * math.sqrt(3)) * (self.s / self.bs_quant))  # Радиус зоны покрытия одной БС

    def calc_summary_losses(self):
        self.z = self.building_loss + self.subscriber_body_loss + self.needed_correction                                    # Запас мощности

        self.p_bs_izl = (self.bs_as_line_power + self.bs_as_line_antenna_gain +
                       self.bs_as_line_feeder_loss + self.bs_as_line_duplex_filter_loss + self.bs_as_line_duplexor_loss)    # Изотропно излучаемая мощность БС

        self.p_as_izl = (self.as_bs_line_power + self.bs_as_line_antenna_gain +
                       self.bs_as_line_feeder_loss + self.bs_as_line_duplex_filter_loss + self.bs_as_line_duplexor_loss)    # Изотропно излучаемая мощность АС

        self.pch = -174 + 10 * math.log10(1.4) + 9 - 98.2                                                                   # Чувствительность приемника
        self.pmin = (self.pch - self.bs_as_line_antenna_gain +
                     self.bs_as_line_duplex_filter_loss + self.bs_as_line_duplexor_loss)                                    # Необходимая мощность сигнала для приема в 50% случаев

        self.bs_sum_loss = self.p_bs_izl - self.pmin - self.z                                                               # Суммарные потери БС АС
        self.as_sum_loss = self.p_as_izl - self.pmin - self.z                                                               # Суммарные потери АС БС

    def calc_asbs_losses(self):
        f = 1375            # Частота радиосигнала
        hprd = 50           # Высота передающей антенны
        hprm = 5            # Высота приемной антенны
        d = self.rc         # Расстояние между антеннами

        a_hprd_selsk = (1.1 * math.log10(f) - 0.7) * hprm - (1.56 * math.log10(f) - 0.8)                                    # Поправочный коэффициент для сельской местности
        lg_selsk = (46.3 + 33.91 * math.log10(f) - 13.821 * math.log10(hprd) - a_hprd_selsk +
                    (44.9 - 6.55 * math.log10(hprd)) * math.log10(d))                                                       # Среднее затухание в городе для сельской местности
        self.l_selsk = lg_selsk - 4.78 * pow(math.log10(f), 2) + 17.33 * math.log10(f) - 40.94                              # Среднее затухание в сельской местности

        a_hprd_prig_small_medium = (1.1 * math.log10(f) - 0.7) * hprm - (1.56 * math.log10(f) - 0.8)                        # Поправочный коэффициент для пригорода маленького/среднего города
        lg_prig_small_medium = (46.3 + 33.91 * math.log10(f) - 13.821 * math.log10(hprd) - a_hprd_prig_small_medium +
                   (44.9 - 6.55 * math.log10(hprd)) * math.log10(d))                                                        # Среднее затухание в городе для пригорода маленького/среднего города
        self.l_prig_small_medium = lg_prig_small_medium - 2 * pow(math.log10(f / 28), 2) - 5.4                              # Среднее затухание в пригороде маленького/среднего города

        a_hprd_prig_big = 3.2 * pow(math.log10(11.75 * hprm), 2) - 4.97                                                     # Поправочный коэффициент для пригорода большого города
        lg_prig_big = (46.3 + 33.91 * math.log10(f) - 13.821 * math.log10(hprd) - a_hprd_prig_big +
                       (44.9 - 6.55 * math.log10(hprd)) * math.log10(d))                                                    # Среднее затухание в городе для пригорода большого города
        self.l_prig_big = lg_prig_big - 2 * pow(math.log10(f / 28), 2) - 5.4                                                # Среднее затухание в пригороде большого города

        a_hprd_city_small_medium = (1.1 * math.log10(f) - 0.7) * hprm - (1.56 * math.log10(f) - 0.8)                        # Поправочный коэффициент для мальенького/среднего города
        self.l_city_small_medium = (46.3 + 33.91 * math.log10(f) - 13.821 * math.log10(hprd) - a_hprd_city_small_medium +
                                (44.9 - 6.55 * math.log10(hprd)) * math.log10(d))                                           # Среднее затухание в маленьком/среднем городе

        a_hprd_city_big = 3.2 * pow(math.log10(11.75 * hprm), 2) - 4.97                                                     # Поправочный коэффициент для большого города
        self.l_city_big = (46.3 + 33.91 * math.log10(f) - 13.821 * math.log10(hprd) - a_hprd_city_big +
                           (44.9 - 6.55 * math.log10(hprd)) * math.log10(d) + 3)                                            # Среднее затухание в большом городе