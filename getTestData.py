# coding:utf-8
from collections import defaultdict

'''
    测试集预处理
'''


def processDiscountRate(inputFilePath, outputFilePath):
    '''
    将折扣率压缩在0-1区间，和训练集预处理函数一样
    :param inputFilePath:
    :param outputFilePath:
    :return:
    '''
    fr = open(inputFilePath, 'r')
    fr.readline()
    fw = open(outputFilePath, 'w')

    for line in fr.readlines():
        temp = line.strip('\n').split(',')
        symbolPos = temp[3].find(':')

        if symbolPos > 0:
            discountRate = str(1 - float(temp[3][symbolPos + 1:]) / float(temp[3][:symbolPos]))
            columnNum = len(temp)
            newLine = ''

            for i in range(columnNum):
                if i == 3:
                    newLine = newLine + discountRate
                else:
                    newLine = newLine + temp[i]
                if i < columnNum - 1:
                    newLine = newLine + ','
            fw.write(newLine + '\n')
        else:
            fw.write(line)
    fr.close()
    fw.close()


def processDistance(userDistanceTable, baseFilePath, outputFilePath):
    '''
    为训练样本在增加一列，即用户离商家的距离，和训练集的函数一致
    :param userDistanceTable: 训练集训练出来的表格，用户与商家的距离
    :param baseFilePath:
    :param outputFilePath:
    :return:
    '''
    table = dict()
    fr = open(userDistanceTable, 'r')

    for line in fr:
        temp = line.strip('\n').split(',')
        table[temp[0]] = temp[1]
    fr.close()

    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')

    for line in fr:
        temp = line.strip('\n').split(',')
        columnNum = len(temp)
        newLine = ''

        for i in range(columnNum):
            if i == 4 and temp[i] == 'null':
                if temp[0] not in table:  # 用户不再训练集里面，标记为5.5（1和10平均）
                    newLine = newLine + '5.5'
                else:
                    newLine = newLine + table[temp[0]]
            else:
                newLine = newLine + temp[i]
            if i < columnNum - 1:
                newLine = newLine + ','

        fw.write(newLine + '\n')

    fr.close()
    fw.close()


def addUserConsump(userConsumpTable, baseFilePath, outputFilePath):
    '''
    增加的用户之前消费券使用比例的列
    :param userConsumpTable:
    :param baseFilePath:
    :param outputFilePath:
    :return:
    '''
    table = dict()
    fr = open(userConsumpTable, 'r')

    for line in fr:
        temp = line.strip('\n').split(',')
        table[temp[0]] = temp[1]

    fr.close()

    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')

    for line in fr:
        temp = line.strip('\n').split(',')

        columnNum = len(temp)
        newLine = ''

        for i in range(columnNum):
            if i == 5:
                if temp[0] not in table:  #
                    newLine = newLine + '0' + ',' + temp[i]
                else:
                    newLine = newLine + table[temp[0]] + ',' + temp[i]
            else:
                newLine = newLine + temp[i]
            if i < columnNum - 1:
                newLine = newLine + ','
        fw.write(newLine + '\n')

    fr.close()
    fw.close()


def addMerchantConsump(merchantConsumpTable, baseFilePath, outputFilePath):
    '''
    增加了该商家历史的被消费信息
    （ 1. 商家消费券被使用的个数 / 所有消费券被使用的个数 （该商家消费券的热度）
       2.领取消费券的数量/商家发送消费券的数量/ （1-核销比例））
    :param merchantConsumpTable:
    :param baseFilePath:
    :param outputFilePath:
    :return:
    '''
    table = defaultdict(lambda: ['0', '0'])

    fr = open(merchantConsumpTable, 'r')

    for line in fr:
        temp = line.strip('\n').split(',')
        table[temp[0]][0] = temp[1]
        table[temp[0]][1] = temp[2]

    fr.close()

    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')
    # fw.write('User_id,Merchant_id,Coupon_id,Discount_rate,Distance,'
    #          '用户消费券使用比例'
    #          '商家消费券被使用的个数 / 所有消费券被使用的个数,'
    #          '领取消费券的数量/商家发送消费券的数量,'
    #          'Date_received')
    for line in fr:
        temp = line.strip('\n').split(',')
        columnNum = len(temp)
        newLine = ''
        for i in range(columnNum):
            if i == 6:
                newLine = newLine + table[temp[1]][0] + ',' + table[temp[1]][1] + ','
            newLine = newLine + temp[i]

            if i < columnNum - 1:
                newLine = newLine + ','
        fw.write(newLine + '\n')
    fr.close()
    fw.close()


if __name__ == '__main__':
    directory = 'original_data' + '/'
    offlineTestFilePath = directory + 'ccf_offline_stage1_test_revised.csv'
    offlineTestDiscountFilePath = directory + 'ccf_offline_stage1_test_discount.csv'
    userDistanceTableFilePath = directory + 'userDistanceTable.csv'
    offlineTestDistanceFilePath = directory + 'ccf_offline_stage1_test_distance.csv'
    userConsumpTableFilePath = directory + 'userConsumpTable.csv'
    offlineTestUserConsumpFilePath = directory + 'ccf_offline_stage1_test_userConsump.csv'
    merchantConsumpTableFilePath = directory + 'merchantConsumpTable.csv'
    offlineTestMerchantConsumpFilePath = directory + 'ccf_offline_stage1_test_merchantConsump.csv'
    twoMonthConsumpFilePath = directory + 'day_consumption.csv'

    processDiscountRate(offlineTestFilePath, offlineTestDiscountFilePath)
    processDistance(userDistanceTableFilePath, offlineTestDiscountFilePath, offlineTestDistanceFilePath)
    addUserConsump(userConsumpTableFilePath, offlineTestDistanceFilePath, offlineTestUserConsumpFilePath)
    addMerchantConsump(merchantConsumpTableFilePath, offlineTestUserConsumpFilePath, offlineTestMerchantConsumpFilePath)
