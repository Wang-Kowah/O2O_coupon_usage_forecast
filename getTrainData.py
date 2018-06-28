# coding:utf-8
from collections import defaultdict
import numpy as np

'''
训练集数据处理
'''

reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}


def dateToNum(month, day):
    return reference[month] + int(day)


def onlyRecordsWithCouponID(inputFilePath, outputFilePath):
    '''
    删除所有coupon_id为null的行，输出文件
    :param inputFilePath:  原始训练文件
    :param outputFilePath:  输出coupon_id为null的行
    :return:
    注：用pandas 可简单实现
    return indf[indf['Coupon_id']!='null']
    '''
    fr = open(inputFilePath, 'r')
    fr.readline()
    fw = open(outputFilePath, 'w')

    for line in fr.readlines():
        temp = line.strip('\n').split(',')

        if temp[2] != 'null':
            fw.write(line)

    fr.close()
    fw.close()


def processDiscountRate(inputFilePath, outputFilePath):
    '''
    将打折形式为 x:y 的压缩到【0，1】区间，变为折扣率
    :param inputFilePath:  输入含有coupon_id的表
    :param outputFilePath:  输出变换之后的表
    :return:
    '''
    fr = open(inputFilePath, 'r')
    fr.readline()
    fw = open(outputFilePath, 'w')
    for line in fr.readlines():

        temp = line.strip('\n').split(',')  # 分割数据
        symbolPos = temp[3].find(':')  # 判断是否有 : ，如果有继续处理。

        if symbolPos > 0:
            # 例如 x：y
            # 折扣率 = 1 - x/y
            discountRate = str(1 - float(temp[3][symbolPos + 1:]) / float(temp[3][:symbolPos]))

            # 写入新的行
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
    ''' pandas实现方式
    for i in a.index:
        tmp = a['Discount_rate'][i]
        symbolPos = tmp.find(':')
        if symbolPos > 0:
            a['Discount_rate'][i] = str(1 - float(tmp[symbolPos+1:]) / float(tmp[:symbolPos]))
    '''


def userDistanceTable(inputFilePath, outputFilePath):
    '''
    :param inputFilePath: 用户距离表
    :param outputFilePath:
    :return:
    '''
    userDist = defaultdict(list)
    fr = open(inputFilePath, 'r')
    cnt = 0
    for line in fr:
        if cnt == 0:
            cnt = 1
            print(line)
            continue
        temp = line.strip('\n').split(',')

        # temp[2] 和 temp[4] 不为空，把user的distance放入列表中去
        if temp[2] != 'null' and temp[4] != 'null':
            userDist[temp[0]].append(float(temp[4]))

    fr.seek(0)
    fw = open(outputFilePath, 'w')

    cnt = 0
    for line in fr:
        if cnt == 0:
            cnt = 1
            print(line)
            continue
        temp = line.strip('\n').split(',')
        userRecordNum = len(userDist[temp[0]])  # 用户使用优惠券的数量
        if userRecordNum > 0:
            newDist = str(sum(userDist[temp[0]]) / userRecordNum)  # 求平均距离
        else:
            newDist = str(5.5)  # 如果用户没有使用过任何优惠券，设置个默认值
        fw.write(temp[0] + ',' + newDist + '\n')
    fr.close()
    fw.close()


def processDistance(userDistanceTable, baseFilePath, outputFilePath):
    '''
    :param userDistanceTable:  用户距离平均值表
    :param baseFilePath:  输入带coupon_id的表格
    :param outputFilePath:  补全带coupon_id表格，用户距离为空，则置为平均距离
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
    cnt = 0
    for line in fr:
        if cnt == 0:
            cnt = 1
            continue
        temp = line.strip('\n').split(',')
        columnNum = len(temp)
        newLine = ''
        for i in range(columnNum):
            # 将所有空数据转换为用户距离的平均值
            if i == 4 and temp[i] == 'null':
                newLine = newLine + table[temp[0]]
            else:
                newLine = newLine + temp[i]

            if i < columnNum - 1:
                newLine = newLine + ','

        fw.write(newLine + '\n')
    fr.close()
    fw.close()


def userConsumpTable(inputFilePath, outputFilePath):
    '''
    :param inputFilePath: 原始训练数据
    :param outputFilePath:  用户使用的消费券的数量/用户领取的消费券的数量
    :return:
    '''
    userCouponInfo = defaultdict(lambda: [0, 0])  # 第一个值为用户使用消费券的数量，第二个领取数量

    fr = open(inputFilePath, 'r')
    fr.readline()
    for line in fr.readlines():
        temp = line.strip('\n').split(',')
        if temp[2] != 'null':
            userCouponInfo[temp[0]][0] += 1
            if temp[6] != 'null':
                userCouponInfo[temp[0]][1] += 1

    fr.close()
    fw = open(outputFilePath, 'w')

    for key in userCouponInfo:
        if userCouponInfo[key][0] != 0:
            ratio = str(userCouponInfo[key][1] / userCouponInfo[key][0])
        else:
            ratio = '0'
        fw.write(key + ',' + ratio + '\n')

    fw.close()


def addUserConsump(userConsumpTable, baseFilePath, outputFilePath):
    '''
    :param userConsumpTable: 用户的使用消费券的比例表
    :param baseFilePath: 模版文件
    :param outputFilePath: 用户的消费比例和距离的关系联合表
    :return:
    '''
    table = dict()
    fr = open(userConsumpTable, 'r')

    # 读取用户使用消费券的比例
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
                newLine = newLine + table[temp[0]] + ','  # 插入新的列
            newLine = newLine + temp[i]

            if i < columnNum - 1:
                newLine = newLine + ','

        fw.write(newLine + '\n')

    fr.close()
    fw.close()


def merchantConsumpTable(inputFilePath, outputFilePath):
    '''
    1.求商家优惠券： 某个商家消费券被使用的个数 / 所有消费券被使用的个数 （该商家消费券的热度）
    2.求 ： 领取消费券的数量/商家发送消费券的数量/ （1-核销比例）
    :param inputFilePath: 原始文件
    :param outputFilePath: 输出上面含有2个特征的文件
    :return:
    '''
    # 第一个数字：某商家消费券被消费的数量
    # 第二个数字：某商家发送消费券的数量
    # 第三个数字：某商家被领取消费券的数量
    merchantConsumpInfo = defaultdict(lambda: [0, 0, 0])

    totalRecordsNum = 0  # 所有记录中使用消费券消费的数量

    fr = open(inputFilePath, 'r')
    fr.readline()
    for line in fr.readlines():
        temp = line.strip('\n').split(',')

        if temp[6] != 'null':
            merchantConsumpInfo[temp[1]][0] += 1
            totalRecordsNum += 1

        if temp[2] != 'null':
            merchantConsumpInfo[temp[1]][1] += 1

            if temp[6] != 'null':
                merchantConsumpInfo[temp[1]][2] += 1

    fr.close()
    fw = open(outputFilePath, 'w')
    for merchant in merchantConsumpInfo:
        f1 = merchantConsumpInfo[merchant][0] / totalRecordsNum
        f2 = merchantConsumpInfo[merchant][2] / merchantConsumpInfo[merchant][1] if merchantConsumpInfo[merchant][
                                                                                        1] != 0 else 0
        fw.write(merchant + ',' + str(f1) + ',' + str(f2) + '\n')

    fw.close()


def addMerchantConsump(merchantConsumpTable, baseFilePath, outputFilePath):
    '''
    合并商户优惠券使用的信息的表格和用户优惠券使用信息的表格
    :param merchantConsumpTable:  商户优惠券信息
    :param baseFilePath:  用户优惠券信息，作为模版文件，增加新的列
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


def addHotPeriod(twoMonthConsump, baseFilePath, outputFilePath):
    '''
    增加消费券使用时间段的热度
    :param twoMonthConsump: 2个月为一个时间段，消费券各天被消费的信息
    :param baseFilePath: 用户商家优惠券信息（用户为模版）
    :param outputFilePath:
    :return:
    '''
    dayConsump = []

    fr = open(twoMonthConsump, 'r')

    for line in fr:
        temp = line.strip('\n').split(',')
        dayConsump.append((int(temp[0]), int(temp[1])))

    fr.close()

    points = np.array(dayConsump)
    x = points[:, 0]
    y = points[:, 1]
    z = np.polyfit(x, y, 8)
    f = np.poly1d(z)  # 2个月内各天被消费的数量与时间的曲线，x轴为0-59，y为消费数量
    x_new = list(range(0, 59))
    y_new = f(x_new)
    totalSum = sum(y_new)  # 消费总值
    fr = open(baseFilePath, 'r')
    fw = open(outputFilePath, 'w')

    for line in fr:
        temp = line.strip('\n').split(',')

        receiveDate = temp[8]  # 领取日期
        receiveDateNum = dateToNum(receiveDate[4:6], receiveDate[6:]) % 60  # 转数字
        accumuConsump = 0  # 该领取日期之后15天的消费数量
        for x_new in range(receiveDateNum, receiveDateNum + 15):
            if x_new >= 60:
                x_new = x_new % 60

            y_new = f(x_new)
            accumuConsump += y_new

        ratio = accumuConsump / totalSum

        columnNum = len(temp)
        newLine = ''

        for i in range(columnNum):
            if i == 8:
                newLine = newLine + str(ratio) + ','

            newLine = newLine + temp[i]

            if i < columnNum - 1:
                newLine = newLine + ','

        fw.write(newLine + '\n')


def markLabel(inputFilePath, outputFilePath):
    '''
    为样本打标记（正样本和付样本），输出最终训练样本
    :param inputFilePath: 含有商家用户对这个优惠券的使用信息，以及优惠券使用时间段的热度
    :param outputFilePath:
    :return:
    '''
    fr = open(inputFilePath, 'r')
    fw = open(outputFilePath, 'w')
    # fw.write('User_id, Merchant_id, Coupon_id, Discount_rate, Distance, '
    #          '用户使用的消费券的数量/用户领取的消费券的数量, '
    #          '某个商家消费券被使用的个数 / 所有消费券被使用的个数, '
    #          '领取消费券的数量/商家发送消费券的数量, '
    #          '消费券使用时间段的热度, '
    #          '正负样本, '
    #          'Date_received, Date')
    fr.readline()
    for line in fr.readlines():
        temp = line.strip('\n').split(',')
        consumpDate = temp[10]

        if temp[2] != 'null' and consumpDate != 'null':
            receiveDate = temp[9]

            # 15天内消费，为正样本,否则为负样本
            if dateToNum(consumpDate[4:6], consumpDate[6:]) - dateToNum(receiveDate[4:6], receiveDate[6:]) <= 15:
                label = '1'
            else:
                label = '0'

        else:
            label = '0'

        columnNum = len(temp)
        newLine = ''

        for i in range(columnNum):
            if i == 9:
                newLine = newLine + label + ','
            newLine = newLine + temp[i]

            if i < columnNum - 1:
                newLine = newLine + ','

        fw.write(newLine + '\n')
    fr.close()
    fw.close()


if __name__ == '__main__':
    directory = 'original_data/'
    offlineTrainFilePath = directory + 'ccf_offline_stage1_train.csv'
    offlineTrainCouponFilePath = directory + 'ccf_offline_stage1_train_coupon.csv'
    offlineTrainDiscountFilePath = directory + 'ccf_offline_stage1_train_discount.csv'
    userDistanceTableFilePath = directory + 'userDistanceTable.csv'
    offlineTrainDistanceFilePath = directory + 'ccf_offline_stage1_train_distance.csv'
    userConsumpTableFilePath = directory + 'userConsumpTable.csv'
    offlineTrainUserConsumpFilePath = directory + 'ccf_offline_stage1_train_userConsump.csv'
    merchantConsumpTableFilePath = directory + 'merchantConsumpTable.csv'
    offlineTrainMerchantConsumpFilePath = directory + 'ccf_offline_stage1_train_merchantConsump.csv'
    twoMonthConsumpFilePath = directory + 'two_month_consump.csv'
    offlineTrainHotPeriodFilePath = directory + 'ccf_offline_stage1_train_hotPeriod.csv'
    trainingSetFilePath = directory + 'training.csv'

    onlyRecordsWithCouponID(offlineTrainFilePath, offlineTrainCouponFilePath)
    processDiscountRate(offlineTrainCouponFilePath, offlineTrainDiscountFilePath)
    userDistanceTable(offlineTrainFilePath, userDistanceTableFilePath)
    processDistance(userDistanceTableFilePath, offlineTrainDiscountFilePath, offlineTrainDistanceFilePath)
    userConsumpTable(offlineTrainFilePath, userConsumpTableFilePath)
    addUserConsump(userConsumpTableFilePath, offlineTrainDistanceFilePath, offlineTrainUserConsumpFilePath)
    merchantConsumpTable(offlineTrainFilePath, merchantConsumpTableFilePath)
    addMerchantConsump(merchantConsumpTableFilePath, offlineTrainUserConsumpFilePath,
                       offlineTrainMerchantConsumpFilePath)
    addHotPeriod(twoMonthConsumpFilePath, offlineTrainMerchantConsumpFilePath, offlineTrainHotPeriodFilePath)
    markLabel(offlineTrainHotPeriodFilePath, trainingSetFilePath)
