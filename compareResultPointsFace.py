""" Сравнение ключевых анатомических точек с live и static изображений с погрешностью в 10% """

import numpy as np


def get_compare_points(facePointsStatic: list, facePointsLive: list) -> bool:
    """ Сравнение двух изображений по ключевым анатомическим точкам """
    distances = np.linalg.norm(facePointsStatic - facePointsLive, axis=1)
    avgValue = np.mean(distances) # среднее значение дистанций
    distancesDifference = abs(distances - avgValue)/avgValue # отклонение от среднего значения в %

    countDifferenceImportant = 0
    for DifferencePointValue in distancesDifference:
        if  DifferencePointValue <= 0.1: # если расстояние меньше 10%, то считаем, что разница минимальна
            countDifferenceImportant += 1
    if countDifferenceImportant/len(distancesDifference) >= 0.9: # если всего таких точек более 90%, то считаем за совпадение лиц (погрешность 10%)
        return True
    else:
        return False



