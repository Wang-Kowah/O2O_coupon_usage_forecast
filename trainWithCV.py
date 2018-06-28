from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import PolynomialFeatures
from collections import defaultdict
from itertools import cycle
import matplotlib.pyplot as plt
import numpy as np
import random
import pydotplus
import time        

'''
    使用K-fold来交叉验证评估特征集和模型

    1. 加载数据
    2. 分割数据集合为k并依次验证
    第一：训练分类器
    第二：输出训练时间
    第三：输出训练相关参数
    第四： 输出分类器的性能
    第五： 绘制ROC曲线，预测平均AOC
'''
# ('User_id, Merchant_id, Coupon_id, Discount_rate, Distance, '
#  '用户使用的消费券的数量/用户领取的消费券的数量, '
#  '某个商家消费券被使用的个数 / 所有消费券被使用的个数, '
#  '领取消费券的数量/商家发送消费券的数量, '
#  '消费券使用时间段的热度, '
#  '正负样本, '
#  'Date_received, Date')

# ('User_id,Merchant_id,Coupon_id,Discount_rate,Distance,'
#  '用户使用的消费券的数量/用户领取的消费券的数量,'
#  '商家消费券被使用的个数 / 所有消费券被使用的个数,'
#  '领取消费券的数量/商家发送消费券的数量,'
#  'Date_received')


def loadData(trainFilePath):
    xTrain = []
    yTrain = []
    trainCouponID = []
    f = open(trainFilePath, 'r')
    # ('User_id, Merchant_id, Coupon_id, Discount_rate, Distance, '
    #  '用户使用的消费券的数量/用户领取的消费券的数量, '
    #  '某个商家消费券被使用的个数 / 所有消费券被使用的个数, '
    #  '领取消费券的数量/商家发送消费券的数量, '
    #  '消费券使用时间段的热度, '
    #  '正负样本, Date_received, Date')
    for line in f:
        temp = line.strip('\n').split(',')
        try:
            trainCouponID.append(temp[2])
            xTrain.append([float(temp[3]), float(temp[4]), float(temp[5]), float(temp[6]), float(temp[7]), float(temp[8])])
            yTrain.append(float(temp[9]))
        except Exception as e:
            print(temp)
            print("Exception :", e)
    f.close()
    return xTrain, yTrain, trainCouponID


def outputCVResults(classifier, x_test, y_test, couponID_test, cvIndex, color, directoryPath):
    predictProbas = classifier.predict_proba(x_test)  # 输出预测概率
    print(predictProbas[:, 1], '\n')
    print(y_test, '\n')

    fpr, tpr, tresholds = roc_curve(y_test, predictProbas[:, 1])
    roc_auc = auc(fpr, tpr, reorder=True)

    plt.plot(fpr, tpr, color=color, lw=2, label='ROC fold %d (area = %0.2f)' % (cvIndex, roc_auc))
    


def train(x, y, couponID, directoryPath):
    x = np.array(x)
    y = np.array(y)
    couponID = np.array(couponID)
    
    print('x:\n', x, '\n')
    print('y:\n', y, '\n')
    print('couponID:\n', couponID, '\n')

    cv = StratifiedKFold(n_splits=3)  # k折交叉验证
    #cv = KFold(n_splits=3)

    colors = cycle(['cyan', 'blue', 'darkorange', 'yellow', 'indigo', 'seagreen'])
    cvIndex = 0

    for (train_index, test_index), color in zip(cv.split(x, y), colors):
        cvIndex += 1
        x_train, x_test, y_train, y_test = x[train_index], x[test_index], y[train_index], y[test_index]
        couponID_test = couponID[test_index]

        print('train_index: %s\ntest_index: %s' % (train_index, test_index))
        print('couponID_test:\n', couponID_test, '\n')
        print('x_train:\n', x_train, '\n')
        print('x_test:\n', x_test, '\n')
        print('y_train:\n', y_train, '\n')
        print('y_test:\n', y_test, '\n')
        print('y_test.shape', str(y_test.shape), '\n')

        start_time = time.time()
        # 可以使用不同的分类器
        # clf = tree.DecisionTreeClassifier(max_depth=4, class_weight='balanced')  #
        # clf = RandomForestClassifier(max_depth=3, n_jobs=-1, class_weight='balanced')
        # clf = LogisticRegression(class_weight='balanced')
        clf = AdaBoostClassifier(base_estimator=LogisticRegression(class_weight='balanced'), n_estimators=50)
        clf.fit(x_train, y_train)
        print('Time for training model: ', time.time() - start_time, '\n')
        outputCVResults(clf, x_test, y_test, couponID_test, cvIndex, color, directoryPath)

    plt.plot([0, 1], [0, 1], color='k', lw=2, linestyle='--', label='Luck')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()


if __name__ == '__main__':
    directoryPath = 'original_data' + '/'
    trainFilePath = directoryPath+'training.csv'
    x, y, trainCouponID = loadData(trainFilePath)
    train(x, y, trainCouponID, directoryPath)

