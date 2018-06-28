reference = {'01': 0, '02': 31, '03': 60, '04': 91, '05': 120, '06': 151}
boudary = 15


def dateToNum(month, day):
    return reference[month] + int(day)


def getStatistics(inputFilePath, outputFilePath, isOffline):
    coupon_use = 0
    coupon_receive = 0

    above15_coupon_use = 0
    below15_coupon_use = 0

    if isOffline:
        coupon_id_idx = 2
    else:
        coupon_id_idx = 3

    fr = open(inputFilePath, 'r')
    cnt = 0

    for idx, line in enumerate(fr):
        if cnt == 0:
            cnt = 1
            print(line)
            continue
        temp = line.strip('\n').split(',')

        if temp[coupon_id_idx] != 'null':
            coupon_receive += 1

            if temp[6] != 'null':
                coupon_use += 1
                date_consumption = temp[6]
                date_received = temp[5]
                interval = dateToNum(date_consumption[4:6], date_consumption[6:]) - dateToNum(date_received[4:6],
                                                                                              date_received[6:])

                if interval > 15:
                    above15_coupon_use += 1
                else:
                    below15_coupon_use += 1

    fr.close()
    record_count = idx + 1

    fw = open(outputFilePath, 'w')
    fw.write('above15_coupon_use = ' + str(above15_coupon_use) + '\n')
    fw.write('below15_coupon_use = ' + str(below15_coupon_use) + '\n')
    fw.write('coupon_use = ' + str(coupon_use) + '\n')
    fw.write('coupon_receive = ' + str(coupon_receive) + '\n')
    fw.write('record_count = ' + str(record_count) + '\n')
    fw.write('above15_coupon_use / coupon_use = ' + str(above15_coupon_use / coupon_use) + '\n')
    fw.write('coupon_use / coupon_receive = ' + str(coupon_use / coupon_receive) + '\n')
    fw.write('coupon_receive / record_count = ' + str(coupon_receive / record_count) + '\n')
    fw.write('coupon_use / record_count = ' + str(coupon_use / record_count) + '\n')
    fw.close()


if __name__ == '__main__':
    inputFilePath = 'original_data/ccf_offline_stage1_train.csv'
    outputFilePath = 'original_data/ccf_offline_stage1_train_info.csv'

    getStatistics(inputFilePath, outputFilePath, isOffline=True)
