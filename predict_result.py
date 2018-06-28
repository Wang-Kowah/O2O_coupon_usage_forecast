#coding:utf-8
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
import time

# 训练集样本
# ('User_id, Merchant_id, Coupon_id, Discount_rate, Distance, '
#  '用户使用的消费券的数量/用户领取的消费券的数量, '
#  '某个商家消费券被使用的个数 / 所有消费券被使用的个数, '
#  '领取消费券的数量/商家发送消费券的数量, '
#  '消费券使用时间段的热度, '
#  '正负样本, '
#  'Date_received, Date')

# 测试集样本
# ('User_id,Merchant_id,Coupon_id,Discount_rate,Distance,'
#  '用户使用的消费券的数量/用户领取的消费券的数量,'
#  '商家消费券被使用的个数 / 所有消费券被使用的个数,'
#  '领取消费券的数量/商家发送消费券的数量,'
#  'Date_received')


def loadData(FilePath, is_train=False):
    x = []
    y = []
    CouponID = []
    f = open(FilePath, 'r')

    for line in f:
        temp = line.strip('\n').split(',')
        try:
            CouponID.append(temp[2])
            x.append([float(temp[0]), float(temp[1]), float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7])])
            if not is_train:
                y.append(float(temp[9]))
        except Exception as e:
            print(temp)
            print("Exception :", e)
    f.close()
    return x, y, CouponID


def getModel():
    x_train, y_train, _ = loadData('original_data/training.csv')
    start_time = time.time()
    clf = AdaBoostClassifier(base_estimator=LogisticRegression(class_weight='balanced'), n_estimators=50)
    clf.fit(x_train, y_train)
    print('Time for training model: ', time.time() - start_time)
    return clf


def getResult(model, x_test, filename, basefile):
    '''
    :param model: 分类器模型
    :param x_test: 测试集x
    :param filename: 输出文件名
    :param basefile: 训练集原始文件
    :return:
    '''
    predict = model.predict_proba(x_test)  # 计算概率
    print('predict: ', predict)
    fw = open(filename, 'w')
    fr = open(basefile, 'r')
    fr.readline()
    for index, line in enumerate(fr):
        temp = line.strip('\n').split(',')
        fw.write('%s,%s,%s,%s\n' % (temp[0], temp[2], temp[5], predict[index][1]))
    fw.close()


if __name__ == '__main__':
    model = getModel()
    x_test, _, _ = loadData('original_data/ccf_offline_stage1_test_merchantConsump.csv', True)
    getResult(model, x_test, 'original_data/result.csv', 'original_data/ccf_offline_stage1_test_revised.csv')