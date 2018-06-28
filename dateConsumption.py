# coding:utf-8
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}
January1st = 5


def dateToNum(month, day):
    return reference[month] + int(day)


def dateToDayOfWeek(month, day):
    result = (reference[month] + int(day) + January1st) % 7
    return result if result != 0 else 7


def getStatistics(inputFilePath, weekConsumpFilePath, monthConsumpFilePath, twoMonthConsumpFilePath, isOffline):
    '''
    :param inputFilePath: 原始数据
    :param weekConsumpFilePath: 周一到周日优惠券被使用情况
    :param monthConsumpFilePath: 每个月各天优惠券被使用的情况
    :param twoMonthConsumpFilePath: 每2个月的数据作为一组，2个月中优惠券各天被使用的情况
    :param isOffline:
    :return:
    '''
    weekConsump = defaultdict(lambda: 0)
    monthConsump = defaultdict(lambda: 0)
    twoMonthConsump = defaultdict(lambda: 0)

    if isOffline:
        coupon_id_idx = 2
    else:
        coupon_id_idx = 3

    fr = open(inputFilePath, 'r')
    fr.readline()
    for line in fr.readlines():
        temp = line.strip('\n').split(',')
        consumpDate = temp[6]

        if temp[coupon_id_idx] != 'null' and consumpDate != 'null':
            month = consumpDate[4:6]
            day = consumpDate[6:]
            dayOfWeek = str(dateToDayOfWeek(month, day))
            weekConsump[dayOfWeek] += 1
            monthConsump[day] += 1
            twoMonthConsump[dateToNum(month, day) % 60] += 1

    fr.close()

    sortedDayConsump = sorted(weekConsump)
    fw = open(weekConsumpFilePath, 'w')

    for key in sortedDayConsump:
        fw.write(key + ',' + str(weekConsump[key]) + '\n')

    fw.close()

    sortedMonthConsump = sorted(monthConsump)
    fw = open(monthConsumpFilePath, 'w')

    for key in sortedMonthConsump:
        fw.write(key + ',' + str(monthConsump[key]) + '\n')

    fw.close()

    sortedTwoMonthConsump = sorted(twoMonthConsump)
    fw = open(twoMonthConsumpFilePath, 'w')

    for key in sortedTwoMonthConsump:
        fw.write(str(key) + ',' + str(twoMonthConsump[key]) + '\n')

    fw.close()


def draw(inputFilePath):
    df = pd.read_csv(inputFilePath, header=None)
    df[1].plot()
    plt.show()


if __name__ == '__main__':
    inputFilePath = 'original_data/ccf_offline_stage1_train.csv'
    weekConsumpFilePath = 'original_data/week_consumption.csv'
    monthConsumpFilePath = 'original_data/month_consumption.csv'
    twoMonthConsumpFilePath = 'original_data/two_month_consump.csv'

    getStatistics(inputFilePath, weekConsumpFilePath, monthConsumpFilePath, twoMonthConsumpFilePath, isOffline=True)
    draw(twoMonthConsumpFilePath)
